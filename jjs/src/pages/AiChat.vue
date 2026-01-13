<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mb-8">
          <h1 class="gradient-text text-h3 font-weight-bold mb-2">
            AI Assistant
          </h1>
          <p class="text-body-1 text-medium-emphasis">
            Get intelligent help with inventory management and medical queries
          </p>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="10" lg="8" class="mx-auto">
        <v-card class="gradient-card">
          <v-toolbar color="surface" density="compact">
            <v-toolbar-title class="d-flex align-center">
              <v-icon color="primary" class="mr-2">mdi-robot</v-icon>
              <span class="font-weight-bold">JJs AI Assistant</span>
            </v-toolbar-title>
            <v-spacer />
            <v-btn
              icon
              @click="clearChat"
              size="small"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-toolbar>

          <div ref="chatContainer" class="chat-messages pa-4">
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="['message', message.sender]"
            >
              <div class="message-content">
                {{ message.content }}
              </div>
              <div class="message-time text-caption text-medium-emphasis mt-1">
                {{ message.timestamp }}
              </div>
            </div>

            <div
              v-if="loading"
              class="message bot"
            >
              <div class="d-flex align-center">
                <v-progress-circular
                  indeterminate
                  size="20"
                  width="2"
                  color="primary"
                  class="mr-3"
                />
                <span>Thinking...</span>
              </div>
            </div>
          </div>

          <v-divider />

          <div class="pa-4">
            <v-form @submit.prevent="sendMessage">
              <v-textarea
                v-model="userInput"
                placeholder="Ask me anything about your inventory..."
                variant="outlined"
                rows="2"
                auto-grow
                hide-details
                :disabled="loading"
                @keydown.enter.exact.prevent="sendMessage"
                class="mb-3"
              >
                <template v-slot:append-inner>
                  <v-btn
                    icon
                    color="primary"
                    type="submit"
                    :disabled="!userInput.trim() || loading"
                    size="small"
                  >
                    <v-icon>mdi-send</v-icon>
                  </v-btn>
                </template>
              </v-textarea>

              <div class="d-flex flex-wrap gap-2 mt-3">
                <v-chip
                  v-for="suggestion in suggestions"
                  :key="suggestion"
                  variant="tonal"
                  size="small"
                  @click="useSuggestion(suggestion)"
                  class="cursor-pointer"
                >
                  {{ suggestion }}
                </v-chip>
              </div>
            </v-form>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/main'

const inventoryStore = useInventoryStore()
const userInput = ref('')
const messages = ref([])
const loading = ref(false)
const chatContainer = ref(null)

const suggestions = computed(() => [
  'Show inventory summary',
  'What items are expiring soon?',
  'How do I use the NFC scanner?',
  'Check stock levels',
  'Generate inventory report'
])

const formatTime = () => {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const addMessage = (content, sender) => {
  messages.value.push({
    content,
    sender,
    timestamp: formatTime()
  })
  
  // Auto-scroll to bottom
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  const message = userInput.value.trim()
  if (!message || loading.value) return

  addMessage(message, 'user')
  userInput.value = ''
  loading.value = true

  try {
    // Prepare context for AI
    const context = {
      inventory: inventoryStore.inventory,
      alerts: inventoryStore.alerts,
      logs: inventoryStore.logs,
      userMessage: message
    }

    // This is where you would integrate with MedLLaMA
    // For now, we'll use a placeholder
    const aiResponse = await getAIResponse(context)
    addMessage(aiResponse, 'bot')
  } catch (error) {
    addMessage('Sorry, I encountered an error. Please try again.', 'bot')
    console.error('AI Error:', error)
  } finally {
    loading.value = false
  }
}

const getAIResponse = async (context) => {
  // Placeholder for MedLLaMA integration
  // In production, replace this with actual API call to MedLLaMA
  
  const { inventory, alerts, logs, userMessage } = context
  const lowerMessage = userMessage.toLowerCase()

  // Basic responses for demo
  if (lowerMessage.includes('inventory') || lowerMessage.includes('stock')) {
    const lowStock = inventory?.filter(item => item.quantity < 50).length || 0
    return `Inventory Summary:
• Total items: ${inventory?.length || 0}
• Low stock items (<50 units): ${lowStock}
• Items requiring attention: ${alerts?.length || 0}

I can provide more detailed analysis. What specific information do you need?`
  } else if (lowerMessage.includes('expir') || lowerMessage.includes('warn')) {
    return `I can help you track expiring medications. Connect me to your inventory system for real-time expiry monitoring and automated alerts.`
  } else if (lowerMessage.includes('nfc') || lowerMessage.includes('scan')) {
    return `The NFC scanner allows you to:
1. Quickly check out medications by scanning their NFC tags
2. Automatically update inventory levels
3. Track medication usage in real-time
4. Generate usage reports

Make sure NFC is enabled on your device for optimal performance.`
  } else if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    return `Hello! I'm your JJs AI Assistant. I can help you with:
• Inventory management and analysis
• Expiry date tracking
• Usage pattern insights
• Report generation
• Medication information

How can I assist you with your medical inventory today?`
  } else {
    return `I'm here to help with medical inventory management. For more specific medical queries, I can be connected to MedLLaMA for specialized medical knowledge.

You can ask me about:
• Current inventory status
• Expiring medications
• Usage patterns and analytics
• System configuration
• Best practices for inventory management

What would you like to know?`
  }
}

const useSuggestion = (suggestion) => {
  userInput.value = suggestion
  sendMessage()
}

const clearChat = () => {
  messages.value = []
  addMessage(
    'Hello! I\'m your JJs AI Assistant. I can help you with inventory management, expiry tracking, and medical queries. How can I assist you today?',
    'bot'
  )
}

onMounted(() => {
  // Initialize with welcome message
  addMessage(
    'Hello! I\'m your JJs AI Assistant. I can help you with inventory management, expiry tracking, and medical queries. How can I assist you today?',
    'bot'
  )
})
</script>

<style scoped>
.chat-messages {
  height: 400px;
  overflow-y: auto;
  background: var(--tertiary-dark);
}

.message {
  max-width: 70%;
  margin-bottom: 16px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  line-height: 1.6;
}

.message.user {
  margin-left: auto;
  background: var(--accent-gradient);
  color: white;
  border-top-right-radius: 4px;
}

.message.bot {
  background: var(--card-dark);
  border: 1px solid var(--border-color);
  border-top-left-radius: 4px;
}

.message-time {
  font-size: 0.75rem;
}

.cursor-pointer {
  cursor: pointer;
}
</style>