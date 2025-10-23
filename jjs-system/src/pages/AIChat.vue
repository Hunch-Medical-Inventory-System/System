<!-- pages/AIChat.vue -->
<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>AI Assistant</v-card-title>
              <v-card-subtitle>Get help with inventory management and medical queries</v-card-subtitle>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-card class="chat-container">
            <v-card-item class="chat-header">
              <v-card-title>
                <v-icon start>mdi-robot</v-icon>
                JJs - Your Medical Inventory Assistant
              </v-card-title>
            </v-card-item>

            <v-card-text class="chat-messages" ref="messagesContainer">
              <div 
                v-for="(message, index) in messages" 
                :key="index"
                :class="['message', message.type]"
              >
                {{ message.text }}
              </div>
              
              <div v-if="loading" class="message bot">
                <v-progress-circular indeterminate size="20" class="mr-2" />
                Thinking...
              </div>
            </v-card-text>

            <v-card-text class="chat-input">
              <v-text-field
                v-model="userMessage"
                placeholder="Type your message here..."
                variant="outlined"
                hide-details
                @keypress.enter="sendMessage"
                :loading="loading"
              >
                <template v-slot:append>
                  <v-btn 
                    color="primary" 
                    @click="sendMessage"
                    :disabled="!userMessage.trim() || loading"
                  >
                    <v-icon>mdi-send</v-icon>
                  </v-btn>
                </template>
              </v-text-field>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Quick Actions -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>Quick Questions</v-card-title>
            </v-card-item>
            <v-card-text>
              <v-chip-group>
                <v-chip
                  v-for="question in quickQuestions"
                  :key="question"
                  variant="outlined"
                  @click="userMessage = question; sendMessage()"
                >
                  {{ question }}
                </v-chip>
              </v-chip-group>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

const messages = ref([
  { type: 'bot', text: "Hello! I'm the JJs bot, your medical inventory assistant. How can I help you today?" }
])
const userMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)

const quickQuestions = [
  'How many items are in stock?',
  'What items are expiring soon?',
  'Show me low stock items',
  'How do I use the NFC scanner?',
  'What are the recent activities?'
]

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  if (!userMessage.value.trim() || loading.value) return

  const message = userMessage.value.trim()
  userMessage.value = ''
  
  // Add user message
  messages.value.push({ type: 'user', text: message })
  scrollToBottom()
  
  // Show loading
  loading.value = true
  scrollToBottom()
  
  try {
    // Simulate AI response - Replace with actual TinyLlama API call
    const response = await generateAIResponse(message)
    messages.value.push({ type: 'bot', text: response })
  } catch (error) {
    messages.value.push({ 
      type: 'bot', 
      text: "I'm sorry, I encountered an error. Please try again later." 
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

const generateAIResponse = async (message) => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000))
  
  const lowerMessage = message.toLowerCase()
  
  // Inventory queries
  if (lowerMessage.includes('inventory') || lowerMessage.includes('stock') || lowerMessage.includes('how many')) {
    return `Currently, there are ${inventoryStore.inventory.length} items in the locker. ${inventoryStore.expiringItems.length} items are expiring soon and ${inventoryStore.inventory.filter(item => item.quantity < 10).length} items have low stock.`
  }
  
  // Expiry queries
  if (lowerMessage.includes('expir') || lowerMessage.includes('warn') || lowerMessage.includes('soon')) {
    if (inventoryStore.expiringItems.length > 0) {
      const itemsList = inventoryStore.expiringItems.slice(0, 3).map(item => 
        `${item.name} (expires ${new Date(item.expiryDate).toLocaleDateString()})`
      ).join(', ')
      return `There are ${inventoryStore.expiringItems.length} items expiring soon: ${itemsList}${inventoryStore.expiringItems.length > 3 ? ' and more...' : ''}. Check the "Expired & Warnings" page for details.`
    } else {
      return "Great news! No items are expiring soon. All inventory items have sufficient shelf life remaining."
    }
  }
  
  // Low stock queries
  if (lowerMessage.includes('low') || lowerMessage.includes('stock')) {
    const lowStock = inventoryStore.inventory.filter(item => item.quantity < 10)
    if (lowStock.length > 0) {
      const itemsList = lowStock.slice(0, 3).map(item => 
        `${item.name} (${item.quantity} left)`
      ).join(', ')
      return `There are ${lowStock.length} items with low stock: ${itemsList}${lowStock.length > 3 ? ' and more...' : ''}. Consider restocking these items soon.`
    } else {
      return "All items have sufficient stock levels. No low stock warnings at this time."
    }
  }
  
  // NFC scanner help
  if (lowerMessage.includes('nfc') || lowerMessage.includes('scan')) {
    return "To use the NFC scanner: 1) Go to the NFC Scanner page, 2) Click 'Start NFC Scan', 3) Place the medication near your device, 4) Follow the prompts to check out or add the item. Make sure your device supports NFC and you've granted browser permissions."
  }
  
  // Logs and activities
  if (lowerMessage.includes('log') || lowerMessage.includes('history') || lowerMessage.includes('recent') || lowerMessage.includes('activity')) {
    return `There are ${inventoryStore.logs.length} log entries in the system. The most recent activities include checkouts, additions, and updates to inventory items. You can view the complete history on the "Logs" page.`
  }
  
  // Add item help
  if (lowerMessage.includes('add') || lowerMessage.includes('new')) {
    return "To add a new medication: 1) Use the NFC scanner with a new medication tag, or 2) Go to the In-Locker page and click 'Add First Item' or the plus button, 3) Fill in the medication details including name, category, quantity, and expiry date."
  }
  
  // Greetings
  if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
    return "Hello! I'm here to help you manage your medical inventory. You can ask me about stock levels, expiring items, how to use features, or any other inventory-related questions!"
  }
  
  // Default response
  return "I'm here to help with medical inventory management. You can ask me about:\n• Current stock levels and low inventory\n• Expiring medications\n• How to use the NFC scanner\n• Recent system activities\n• Adding new items to inventory\n\nWhat would you like to know?"
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-container {
  height: 500px;
  display: flex;
  flex-direction: column;
}

.chat-header {
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
}

.message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}

.message.bot {
  align-self: flex-start;
  background-color: #f5f5f5;
  border-top-left-radius: 4px;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  border-top-right-radius: 4px;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
}

@media (max-width: 768px) {
  .chat-container {
    height: 400px;
  }
  
  .message {
    max-width: 90%;
  }
}
</style>