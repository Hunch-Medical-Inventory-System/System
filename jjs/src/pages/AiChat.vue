<template>
  <v-container fluid class="ai-assistant-container">
    <v-row class="fill-height">
      <v-col cols="12" class="h-100">
        <!-- Main Chat Container -->
        <v-card class="ai-chat-card h-100">
          <!-- Chat Header -->
          <div class="chat-header">
            <div class="d-flex align-center">
              <div class="ai-icon-container mr-3">
                <v-icon size="28" color="primary">mdi-brain</v-icon>
              </div>
              <div>
                <h2 class="text-h6 font-weight-bold">MedLLaMA Assistant</h2>
                <div class="d-flex align-center">
                  <v-chip
                    size="x-small"
                    :color="connectionStatus.color"
                    class="mr-2"
                    label
                  >
                    <v-icon size="12" class="mr-1">mdi-circle</v-icon>
                    {{ connectionStatus.text }}
                  </v-chip>
                </div>
              </div>
            </div>
            
            <div class="header-actions">
              <v-tooltip text="Clear conversation" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon
                    @click="clearConversation"
                    variant="text"
                    size="small"
                  >
                    <v-icon>mdi-broom</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </div>
          </div>

          <!-- Chat Messages Area -->
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

            <!-- Typing Indicator -->
            <div v-if="isLoading" class="typing-indicator">
              <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>

          <!-- Input Area -->
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

            <!-- Quick Actions -->
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

const MEDLLAMA_CONFIG = {
  apiBaseUrl: 'https://your-medllama-api.com/v1',
  apiKey: 'your-api-key-here',
  defaultModel: 'medllama-2-13b',
  maxTokens: 2000,
  temperature: 0.7
}

const userMessage = ref('')
const messages = ref([])
const isLoading = ref(false)
const messagesContainer = ref(null)
const messageInput = ref(null)

const inventoryStore = useInventoryStore()

const connectionStatus = computed(() => {
  return {
    color: 'success',
    text: 'Connected'
  }
})

const quickActions = computed(() => [
  { label: 'Inventory Summary', icon: 'mdi-clipboard-list', action: 'inventorySummary' },
  { label: 'Expiry Report', icon: 'mdi-calendar-clock', action: 'expiryReport' },
  { label: 'Drug Info', icon: 'mdi-pill', action: 'drugInfo' },
  { label: 'Usage Analytics', icon: 'mdi-chart-line', action: 'analytics' }
])

const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const addMessage = (content, role) => {
  const message = {
    id: Date.now() + Math.random(),
    content,
    role,
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(message)
  scrollToBottom()
  
  localStorage.setItem('medllama_conversation', JSON.stringify(messages.value))
}

const buildContext = () => {
  const context = {
    systemPrompt: `You are MedLLaMA, a specialized medical AI assistant. Provide accurate, evidence-based medical information and inventory insights.`,
    
    inventoryContext: inventoryStore?.inventory?.length > 0 ? {
      summary: {
        totalItems: inventoryStore.inventory.length,
        lowStock: inventoryStore.inventory.filter(item => item.quantity < (item.reorderLevel || 50)).length,
        expiringSoon: inventoryStore.inventory.filter(item => {
          if (!item.expiryDate) return false
          const daysUntilExpiry = Math.ceil((new Date(item.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))
          return daysUntilExpiry <= 30
        }).length
      },
      categories: [...new Set(inventoryStore.inventory.map(item => item.category).filter(Boolean))],
      criticalItems: inventoryStore.inventory.filter(item => item.isCritical)
    } : null,
    
    conversationHistory: messages.value.slice(-10).map(msg => ({
      role: msg.role,
      content: msg.content
    }))
  }
  
  return context
}

const sendMessage = async () => {
  const content = userMessage.value.trim()
  if (!content || isLoading.value) return

  addMessage(content, 'user')
  userMessage.value = ''
  
  isLoading.value = true
  
  try {
    const context = buildContext()
    
    const requestPayload = {
      model: MEDLLAMA_CONFIG.defaultModel,
      messages: [
        {
          role: 'system',
          content: context.systemPrompt
        },
        ...context.conversationHistory,
        {
          role: 'user',
          content: content,
          context: context.inventoryContext
        }
      ],
      max_tokens: MEDLLAMA_CONFIG.maxTokens,
      temperature: MEDLLAMA_CONFIG.temperature
    }
    
    const response = await callMedLLaMAAPI(requestPayload)
    
    addMessage(response.content, 'assistant')
    
  } catch (error) {
    console.error('MedLLaMA API Error:', error)
    addMessage(`Error: ${error.message}. Please try again.`, 'assistant')
  } finally {
    isLoading.value = false
    nextTick(() => {
      if (messageInput.value) {
        messageInput.value.focus()
      }
    })
  }
}

const callMedLLaMAAPI = async (payload) => {
  const response = await fetch(`${MEDLLAMA_CONFIG.apiBaseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${MEDLLAMA_CONFIG.apiKey}`
    },
    body: JSON.stringify(payload)
  })
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  
  const data = await response.json()
  return {
    content: data.choices[0].message.content,
    model: data.model
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
      userMessage.value = 'Search for detailed drug information and interactions'
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
  addMessage(
    'Hello! JJ, your medical AI assistant. How can I help you today?',
    'assistant'
  )
}

onMounted(() => {
  const saved = localStorage.getItem('medllama_conversation')
  if (saved) {
    messages.value = JSON.parse(saved)
  } else {
    addMessage(
      'Hello! I am JJ, your medical AI assistant. How can I help you today?',
      'assistant'
    )
  }
  scrollToBottom()
  
  nextTick(() => {
    if (messageInput.value) {
      messageInput.value.focus()
    }
  })
})

watch(messages, scrollToBottom, { deep: true })
</script>

<style scoped>
.ai-assistant-container {
  height: calc(100vh - 64px);
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
  padding: 0;
}

.h-100 {
  height: 100%;
}

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

.header-actions {
  display: flex;
  gap: 8px;
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

.message-bubble.user {
  flex-direction: row-reverse;
}

.message-role-indicator {
  margin: 0 10px;
}

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

.user-message {
  white-space: pre-wrap;
}

.message-meta {
  display: flex;
  justify-content: flex-end;
  font-size: 0.7rem;
  opacity: 0.7;
}

.timestamp {
  font-size: 0.65rem;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: var(--surface-dark);
  border-radius: 10px;
  margin-bottom: 1rem;
}

.typing-dots {
  display: flex;
  margin-right: 12px;
}

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

.input-wrapper {
  position: relative;
}

.message-input {
  background: var(--surface-dark);
  border-radius: 10px;
}

.message-input :deep(.v-field__field) {
  padding: 10px 14px;
}

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

.quick-action-chip:hover {
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: var(--surface-dark);
}

.messages-container::-webkit-scrollbar-thumb {
  background: var(--primary-light);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: var(--accent);
}
</style>