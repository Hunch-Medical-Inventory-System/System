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
                <h2 class="text-h6 font-weight-bold">JJ — Medical Assistant</h2>
                <div class="d-flex align-center">
                  <v-chip size="x-small" :color="serverOnline ? 'success' : 'error'" class="mr-2" label>
                    <v-icon size="12" class="mr-1">mdi-circle</v-icon>
                    {{ serverOnline ? 'Connected' : 'Offline' }}
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

            <!-- Typing indicator -->
            <div v-if="isLoading" class="message-bubble assistant">
              <div class="message-role-indicator">
                <v-avatar size="24" color="accent">
                  <v-icon size="14" color="white">mdi-robot</v-icon>
                </v-avatar>
              </div>
              <div class="message-content">
                <div class="typing-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>

          <!-- Input -->
          <div class="input-section">
            <div class="input-wrapper">
              <v-textarea
                ref="messageInput"
                v-model="userMessage"
                placeholder="Ask about inventory, medications, expiry dates..."
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
                @click="executeQuickAction(action.prompt)"
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
import { ref, onMounted, nextTick, watch } from 'vue'

const API_BASE = 'http://127.0.0.1:8080'

// --------------------------------------------------
// State
// --------------------------------------------------

const userMessage       = ref('')
const messages          = ref([])
const isLoading         = ref(false)
const serverOnline      = ref(false)
const messagesContainer = ref(null)
const messageInput      = ref(null)

const quickActions = [
  { label: 'Expiring Soon',      icon: 'mdi-calendar-clock',  prompt: 'Which items are expiring within the next 30 days? List them.' },
  { label: 'Expired Items',      icon: 'mdi-alert-circle',    prompt: 'List all expired items currently in the inventory.' },
  { label: 'Low Stock',          icon: 'mdi-package-variant',  prompt: 'Which items are running low on stock (under 50 units)?' },
  { label: 'Inventory Summary',  icon: 'mdi-clipboard-list',  prompt: 'Give me a full summary of the current inventory status.' },
]

// --------------------------------------------------
// Helpers
// --------------------------------------------------

const formatTimestamp = (ts) =>
  new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value)
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  })
}

const addMessage = (content, role) => {
  messages.value.push({
    id: Date.now() + Math.random(),
    content,
    role,
    timestamp: new Date().toISOString()
  })
  scrollToBottom()
  localStorage.setItem('jj_conversation', JSON.stringify(messages.value))
}

// --------------------------------------------------
// API
// --------------------------------------------------

const checkHealth = async () => {
  try {
    const res = await fetch(`${API_BASE}/api/health`)
    serverOnline.value = res.ok
  } catch {
    serverOnline.value = false
  }
}

const sendMessage = async () => {
  const content = userMessage.value.trim()
  if (!content || isLoading.value) return

  addMessage(content, 'user')
  userMessage.value = ''
  isLoading.value   = true

  // Pass last 8 messages as history (excluding the one we just added)
  const history = messages.value
    .slice(-9, -1)
    .map(m => ({ role: m.role, content: m.content }))

  try {
    const res = await fetch(`${API_BASE}/api/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: content,
        history,
        model: 'medllama2:latest'
      })
    })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || `Server error ${res.status}`)
    }

    const data = await res.json()
    addMessage(data.response, 'assistant')

  } catch (err) {
    addMessage(`⚠️ ${err.message}`, 'assistant')
  } finally {
    isLoading.value = false
    nextTick(() => messageInput.value?.focus())
  }
}

const executeQuickAction = (prompt) => {
  userMessage.value = prompt
  sendMessage()
}

const clearConversation = () => {
  messages.value = []
  localStorage.removeItem('jj_conversation')
  addMessage("Hello! I'm JJ, your medical inventory assistant. Ask me about stock levels, expiry dates, or anything medical.", 'assistant')
}

// --------------------------------------------------
// Init
// --------------------------------------------------

onMounted(async () => {
  await checkHealth()

  const saved = localStorage.getItem('jj_conversation')
  if (saved) {
    try { messages.value = JSON.parse(saved) } catch { /* ignore */ }
  }

  if (!messages.value.length) {
    addMessage("Hello! I'm JJ, your medical inventory assistant. Ask me about stock levels, expiry dates, or anything medical.", 'assistant')
  }

  scrollToBottom()
  nextTick(() => messageInput.value?.focus())
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
  border-radius: 10px;
  padding: 12px;
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

.message-text {
  line-height: 1.5;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

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

.message-meta {
  display: flex;
  justify-content: flex-end;
  font-size: 0.7rem;
  opacity: 0.7;
}

/* Typing dots inside message bubble */
.typing-dots {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 0;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--primary-light);
  border-radius: 50%;
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

.message-input { border-radius: 10px; }

.message-input :deep(.v-field__field) { padding: 10px 14px; }

.send-btn {
  background: var(--primary-gradient);
  color: white !important;
}

.quick-actions {
  display: flex;
  gap: 6px;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

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
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40%           { transform: scale(1); }
}

.messages-container::-webkit-scrollbar { width: 6px; }
.messages-container::-webkit-scrollbar-track { background: var(--surface-dark); }
.messages-container::-webkit-scrollbar-thumb { background: var(--primary-light); border-radius: 3px; }
.messages-container::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>