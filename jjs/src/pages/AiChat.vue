<template>
  <v-container fluid class="ai-assistant-container">
    <v-row class="fill-height">
      <v-col cols="12" class="h-100">
        <v-card class="ai-chat-card h-100">
          <!-- Header -->
          <div class="chat-header">
            <div class="d-flex align-center">
              <div class="ai-icon-container mr-3">
                <v-icon size="28" color="primary">mdi-brain</v-icon>
              </div>
              <div>
                <h2 class="text-h6 font-weight-bold">MedLLaMA Assistant</h2>
                <div class="d-flex align-center">
                  <v-chip size="x-small" :color="connectionStatus.color" class="mr-2" label>
                    <v-icon size="12" class="mr-1">mdi-circle</v-icon>
                    {{ connectionStatus.text }}
                  </v-chip>
                </div>
              </div>
            </div>

            <div class="header-actions">
              <v-tooltip text="Clear conversation" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" icon @click="clearConversation" variant="text" size="small">
                    <v-icon>mdi-broom</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </div>
          </div>

          <!-- Messages -->
          <div ref="messagesContainer" class="messages-container">
            <div
              v-for="message in messages"
              :key="message.id"
              :class="['message-bubble', message.role]"
            >
              <div class="message-role-indicator">
                <v-avatar size="24" :color="message.role === 'user' ? 'primary' : 'accent'">
                  <v-icon size="14" color="white">
                    {{ message.role === 'user' ? 'mdi-account' : 'mdi-robot' }}
                  </v-icon>
                </v-avatar>
              </div>

              <div class="message-content">
                <div class="message-text">
                  <pre v-if="message.role === 'assistant'" class="ai-response">{{ message.content }}</pre>
                  <div v-else class="user-message">{{ message.content }}</div>
                </div>

                <div class="message-meta">
                  <span class="timestamp">{{ formatTimestamp(message.timestamp) }}</span>
                </div>
              </div>
            </div>

            <div v-if="isLoading" class="typing-indicator">
              <div class="typing-dots">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>

          <!-- Input -->
          <div class="input-section">
            <div class="input-wrapper">
              <v-textarea
                ref="messageInput"
                v-model="userMessage"
                placeholder="Type your medical or inventory query..."
                variant="solo-filled"
                rows="1"
                auto-grow
                hide-details
                :disabled="isLoading"
                @keydown.enter.exact.prevent="sendMessage"
                class="message-input"
                flat
                bg-color="secondary-dark"
              >
                <template v-slot:append-inner>
                  <v-btn
                    icon
                    :color="userMessage.trim() ? 'primary' : 'disabled'"
                    :disabled="!userMessage.trim() || isLoading"
                    @click="sendMessage"
                    size="small"
                    class="send-btn"
                  >
                    <v-icon>{{ isLoading ? 'mdi-loading mdi-spin' : 'mdi-send' }}</v-icon>
                  </v-btn>
                </template>
              </v-textarea>
            </div>

            <div class="quick-actions">
              <v-chip
                v-for="action in quickActions"
                :key="action.label"
                variant="tonal"
                size="small"
                @click="executeQuickAction(action)"
                class="quick-action-chip"
                :prepend-icon="action.icon"
              >
                {{ action.label }}
              </v-chip>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useInventoryStore } from '@/stores/main'

/**
 * MEDLLAMA2 over Ollama
 * Make sure you have:
 *   ollama pull medllama2:latest
 *   ollama serve
 */
const OLLAMA = {
  defaultModel: 'medllama2:latest',
  temperature: 0.7,
  numPredict: 2000,
  baseUrls: ['http://localhost:11434', 'http://127.0.0.1:11434', '/ollama']
}

const userMessage = ref('')
const messages = ref([])
const isLoading = ref(false)
const messagesContainer = ref(null)
const messageInput = ref(null)

const inventoryStore = useInventoryStore()

const connectionState = ref({ ok: false, baseUrl: null, modelFound: null, error: null })

const connectionStatus = computed(() => {
  if (connectionState.value.ok) return { color: 'success', text: 'Connected' }
  if (connectionState.value.error) return { color: 'error', text: 'Not reachable' }
  return { color: 'warning', text: 'Checking…' }
})

const quickActions = computed(() => [
  { label: 'Inventory Summary', icon: 'mdi-clipboard-list', action: 'inventorySummary' },
  { label: 'Expiry Report', icon: 'mdi-calendar-clock', action: 'expiryReport' },
  { label: 'Drug Info', icon: 'mdi-pill', action: 'drugInfo' },
  { label: 'Usage Analytics', icon: 'mdi-chart-line', action: 'analytics' }
])

const formatTimestamp = (timestamp) =>
  new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const addMessage = (content, role) => {
  const msg = { id: Date.now() + Math.random(), content, role, timestamp: new Date().toISOString() }
  messages.value.push(msg)
  scrollToBottom()
  localStorage.setItem('medllama_conversation', JSON.stringify(messages.value))
}

/**
 * Sanitizes assistant output:
 * - removes leading "Response:"
 * - removes everything from "(Level X)" onward
 * - removes trailing rubric/citation blocks like "[2] ..."
 */
const sanitizeAssistantOutput = (text) => {
  if (!text) return ''

  let out = String(text).replace(/\r\n/g, '\n')

  // Remove leading "Response:"
  out = out.replace(/^\s*response\s*:\s*/i, '')

  // Cut everything after "(Level X)" (case-insensitive)
  out = out.replace(/\s*\(level\s*\d+\).*$/is, '')

  // If there's a trailing bracket reference section, remove it
  out = out.replace(/\n?\s*\[\d+\]\s*[\s\S]*$/m, '')

  return out.trim()
}

const buildContext = () => {
  const inventory = inventoryStore?.inventory ?? []

  const inventoryContext =
    inventory.length > 0
      ? {
          summary: {
            totalItems: inventory.length,
            lowStock: inventory.filter((item) => item.quantity < (item.reorderLevel || 50)).length,
            expiringSoon: inventory.filter((item) => {
              if (!item.expiryDate) return false
              const daysUntilExpiry = Math.ceil(
                (new Date(item.expiryDate) - new Date()) / (1000 * 60 * 60 * 24)
              )
              return daysUntilExpiry <= 30
            }).length
          },
          categories: [...new Set(inventory.map((item) => item.category).filter(Boolean))],
          criticalItems: inventory.filter((item) => item.isCritical)
        }
      : null

  return {
    systemPrompt:
      'You are MedLLaMA2 running locally via Ollama. Provide accurate, evidence-based medical information and inventory insights. Respond with ONLY the answer text. Do not include "Response:", levels, grading rubrics, or reference blocks.',
    inventoryContext,
    conversationHistory: messages.value.slice(-10).map((m) => ({ role: m.role, content: m.content }))
  }
}

const tryOllama = async (path, options) => {
  let lastError = null
  for (const baseUrl of OLLAMA.baseUrls) {
    try {
      const res = await fetch(`${baseUrl}${path}`, options)
      return { res, baseUrl }
    } catch (e) {
      lastError = e
    }
  }
  throw lastError || new Error('Unable to reach Ollama.')
}

const checkOllamaConnection = async () => {
  connectionState.value = { ok: false, baseUrl: null, modelFound: null, error: null }

  try {
    const { res, baseUrl } = await tryOllama('/api/tags', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Ollama /api/tags failed: ${res.status} ${text}`)
    }

    const data = await res.json()
    const names = (data?.models || []).map((m) => m?.name).filter(Boolean)
    const modelFound = names.includes(OLLAMA.defaultModel)

    connectionState.value = { ok: true, baseUrl, modelFound, error: null }

    if (!modelFound) {
      addMessage(
        `⚠️ Connected to Ollama at ${baseUrl}, but model "${OLLAMA.defaultModel}" is not installed.\n\nRun:\nollama pull ${OLLAMA.defaultModel}\n\nInstalled models:\n${names.join('\n') || '(none found)'}`,
        'assistant'
      )
    }
  } catch (e) {
    connectionState.value = { ok: false, baseUrl: null, modelFound: null, error: e?.message || String(e) }
  }
}

const ollamaChat = async ({ model, messages, temperature, num_predict }) => {
  const payload = {
    model,
    messages,
    stream: false,
    options: {
      temperature: temperature ?? OLLAMA.temperature,
      num_predict: num_predict ?? OLLAMA.numPredict
    }
  }

  // Prefer the known-good baseUrl once connected; otherwise try them all
  if (connectionState.value.ok && connectionState.value.baseUrl) {
    const res = await fetch(`${connectionState.value.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Ollama chat failed: ${res.status} ${text}`)
    }
    const data = await res.json()
    return data?.message?.content ?? ''
  }

  const { res } = await tryOllama('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Ollama chat failed: ${res.status} ${text}`)
  }

  const data = await res.json()
  return data?.message?.content ?? ''
}

const sendMessage = async () => {
  const content = userMessage.value.trim()
  if (!content || isLoading.value) return

  addMessage(content, 'user')
  userMessage.value = ''
  isLoading.value = true

  try {
    const context = buildContext()

    const messagesForModel = [
      { role: 'system', content: context.systemPrompt },
      ...(context.inventoryContext
        ? [{ role: 'system', content: `Inventory context (JSON):\n${JSON.stringify(context.inventoryContext, null, 2)}` }]
        : []),
      ...context.conversationHistory,
      { role: 'user', content }
    ]

    const raw = await ollamaChat({
      model: OLLAMA.defaultModel,
      messages: messagesForModel,
      temperature: OLLAMA.temperature,
      num_predict: OLLAMA.numPredict
    })

    const cleaned = sanitizeAssistantOutput(raw)
    addMessage(cleaned || 'Sorry — I did not receive a usable response from the model.', 'assistant')
  } catch (err) {
    console.error('Ollama Error:', err)
    addMessage(`Error: ${err?.message || 'Unknown error'}. Please try again.`, 'assistant')
  } finally {
    isLoading.value = false
    nextTick(() => messageInput.value?.focus())
  }
}

const executeQuickAction = (action) => {
  switch (action.action) {
    case 'inventorySummary':
      userMessage.value = 'Provide a comprehensive inventory summary'
      break
    case 'expiryReport':
      userMessage.value = 'Generate a report of medications expiring in the next 30 days'
      break
    case 'drugInfo':
      userMessage.value = 'Provide detailed drug information, including common interactions and contraindications'
      break
    case 'analytics':
      userMessage.value = 'Show usage patterns and inventory optimization suggestions'
      break
  }
  sendMessage()
}

const clearConversation = () => {
  messages.value = []
  localStorage.removeItem('medllama_conversation')
  addMessage('Hello! I am JJ, your medical AI assistant. How can I help you today?', 'assistant')
}

onMounted(async () => {
  const saved = localStorage.getItem('medllama_conversation')
  if (saved) {
    try {
      messages.value = JSON.parse(saved)
    } catch {
      messages.value = []
    }
  }

  if (messages.value.length === 0) {
    addMessage('Hello! I am JJ, your medical AI assistant. How can I help you today?', 'assistant')
  }

  scrollToBottom()
  nextTick(() => messageInput.value?.focus())

  await checkOllamaConnection()
})

watch(messages, scrollToBottom, { deep: true })
</script>

<style scoped>
.ai-assistant-container {
  height: calc(100vh - 64px);
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
  padding: 0;
}

.h-100 { height: 100%; }

.ai-chat-card {
  background: var(--card-dark);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  background: linear-gradient(90deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.ai-icon-container {
  background: var(--accent-gradient);
  border-radius: 10px;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-actions { display: flex; gap: 8px; }

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  background: var(--tertiary-dark);
  min-height: 0;
}

.message-bubble {
  display: flex;
  margin-bottom: 1rem;
  animation: fadeIn 0.3s ease-out;
}

.message-bubble.user { flex-direction: row-reverse; }
.message-role-indicator { margin: 0 10px; }

.message-content {
  max-width: 75%;
  background: var(--surface-dark);
  border-radius: 10px;
  padding: 12px;
  position: relative;
}

.message-bubble.user .message-content {
  background: var(--accent-gradient);
  color: white;
  border-top-right-radius: 4px;
}

.message-bubble.assistant .message-content {
  background: var(--card-dark);
  border: 1px solid var(--border-color);
  border-top-left-radius: 4px;
}

.message-text { line-height: 1.5; margin-bottom: 0.25rem; font-size: 0.9rem; }

.ai-response {
  white-space: pre-wrap;
  font-family: inherit;
  font-size: 0.9rem;
  color: var(--text-primary);
  margin: 0;
  padding: 0;
  line-height: 1.5;
}

.user-message { white-space: pre-wrap; }

.message-meta { display: flex; justify-content: flex-end; font-size: 0.7rem; opacity: 0.7; }
.timestamp { font-size: 0.65rem; }

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: var(--surface-dark);
  border-radius: 10px;
  margin-bottom: 1rem;
}

.typing-dots { display: flex; margin-right: 12px; }

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--primary-light);
  border-radius: 50%;
  margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

.input-section {
  background: var(--card-dark);
  border-top: 1px solid var(--border-color);
  padding: 1rem 1.5rem;
  flex-shrink: 0;
}

.input-wrapper { position: relative; }
.message-input { background: var(--surface-dark); border-radius: 10px; }
.message-input :deep(.v-field__field) { padding: 10px 14px; }

.send-btn { background: var(--primary-gradient); color: white !important; }

.quick-actions { display: flex; gap: 6px; margin-top: 0.75rem; flex-wrap: wrap; }

.quick-action-chip {
  background: var(--surface-dark) !important;
  border: 1px solid var(--border-color) !important;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8rem;
  height: 28px;
}

.quick-action-chip:hover { transform: translateY(-1px); }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.messages-container::-webkit-scrollbar { width: 6px; }
.messages-container::-webkit-scrollbar-track { background: var(--surface-dark); }
.messages-container::-webkit-scrollbar-thumb { background: var(--primary-light); border-radius: 3px; }
.messages-container::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
