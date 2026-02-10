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
            <span class="loading-text">JJs V2 is thinking...</span>
          </div>
        </div>
      </div>
    </v-card>

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
      messagesContainer.value.scrollTop =
        messagesContainer.value.scrollHeight
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
  overflow: hidden;
}

.chat-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.chat-title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(90deg, #4A6CF7 0%, #8A2BE2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.chat-subtitle {
  font-size: 14px;
  color: #8E8E93;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.messages-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: calc(100vh - 280px);
}

.welcome-message {
  text-align: center;
  padding: 60px 20px;
}

.welcome-icon {
  margin-bottom: 24px;
}

.welcome-title {
  font-size: 24px;
  font-weight: 600;
  color: #FFFFFF;
  margin-bottom: 12px;
}

.welcome-text {
  font-size: 16px;
  color: #8E8E93;
  max-width: 600px;
  margin: 0 auto 32px;
  line-height: 1.6;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  max-width: 800px;
  margin: 0 auto;
}

.suggestion-chip {
  background: rgba(74, 108, 247, 0.1) !important;
  border-color: rgba(74, 108, 247, 0.3) !important;
  color: #4A6CF7 !important;
  cursor: pointer;
  transition: all 0.3s ease;
}

.suggestion-chip:hover {
  background: rgba(74, 108, 247, 0.2) !important;
  transform: translateY(-2px);
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-wrapper {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-bubble.user {
  flex-direction: row-reverse;
}

.message-role-indicator {
  margin: 0 10px;
}

.message-content {
  background: #2D3447;
  border-radius: 12px;
  padding: 16px;
  position: relative;
}

.message-wrapper.user .message-content {
  background: linear-gradient(135deg, rgba(74, 108, 247, 0.15) 0%, rgba(138, 43, 226, 0.15) 100%);
  border: 1px solid rgba(74, 108, 247, 0.3);
}

.message-wrapper.assistant .message-content {
  border: 1px solid rgba(74, 108, 247, 0.1);
}

.message-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
}

.message-avatar {
  width: 28px;
  height: 28px;
  background: rgba(74, 108, 247, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-role {
  font-size: 14px;
  font-weight: 600;
  color: #4A6CF7;
}

.message-time {
  font-size: 12px;
  color: #8E8E93;
  margin-left: auto;
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

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #2D3447;
  border-radius: 12px;
  border: 1px solid rgba(74, 108, 247, 0.1);
  max-width: 200px;
  align-self: flex-start;
}

.typing-dots {
  display: flex;
  margin-right: 12px;
}

.dot {
  width: 8px;
  height: 8px;
  background: #4A6CF7;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.loading-text {
  font-size: 14px;
  color: #8E8E93;
  font-weight: 500;
}

.input-card {
  background: #1A1F2E;
  border: 1px solid #2D3447;
  border-radius: 12px;
  margin-top: 16px;
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
