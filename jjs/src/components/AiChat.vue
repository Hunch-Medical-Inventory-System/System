<template>
  <div id="ai-chat" class="page">
    <div class="page-header">
      <h2>AI Assistant</h2>
      <p>Get help with inventory management and medical queries</p>
    </div>
    
    <div class="chat-container">
      <div class="chat-header">
        <h3><i class="fas fa-robot"></i> JJs - Your Medical Inventory Assistant</h3>
      </div>
      <div class="chat-messages" ref="chatMessages">
        <div class="message bot">
          Hello! I'm the JJs bot, your medical inventory assistant. How can I help you today?
        </div>
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.sender]"
        >
          {{ message.text }}
        </div>
      </div>
      <div class="chat-input">
        <input 
          type="text" 
          v-model="userMessage" 
          @keypress.enter="sendMessage"
          placeholder="Type your message here..."
        >
        <button @click="sendMessage">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AiChat',
  props: {
    inventory: Array,
    logs: Array
  },
  data() {
    return {
      messages: [],
      userMessage: ''
    }
  },
  methods: {
    sendMessage() {
      if (!this.userMessage.trim()) return
      
      // Add user message
      this.messages.push({
        text: this.userMessage,
        sender: 'user'
      })
      
      const message = this.userMessage
      this.userMessage = ''
      
      // Scroll to bottom
      this.$nextTick(() => {
        this.scrollToBottom()
      })
      
      // Simulate AI response after delay
      setTimeout(() => {
        const response = this.generateAIResponse(message)
        this.messages.push({
          text: response,
          sender: 'bot'
        })
        
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }, 1000)
    },
    scrollToBottom() {
      const container = this.$refs.chatMessages
      container.scrollTop = container.scrollHeight
    },
    generateAIResponse(message) {
      const lowerMessage = message.toLowerCase()
      
      if (lowerMessage.includes('inventory') || lowerMessage.includes('stock')) {
        return `Currently, there are ${this.inventory.length} items in the locker.`
      } else if (lowerMessage.includes('expir') || lowerMessage.includes('warn')) {
        const warningItems = this.inventory.filter(item => {
          const expiryDate = new Date(item.expiryDate)
          const today = new Date()
          const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
          return daysUntilExpiry <= 30
        })
        return `There are ${warningItems.length} items that need attention. Check the "Expired & Warnings" page for details.`
      } else if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
        return "Hello! How can I assist you with the medical inventory today?"
      } else if (lowerMessage.includes('nfc') || lowerMessage.includes('scan')) {
        return "To use the NFC scanner, go to the NFC Scanner page and click 'Start NFC Scan'. Then place the medication near your device."
      } else if (lowerMessage.includes('add') || lowerMessage.includes('new')) {
        return "To add a new medication, use the NFC scanner with a new medication or manually add it through the system administration."
      } else if (lowerMessage.includes('log') || lowerMessage.includes('history')) {
        return `There are ${this.logs.length} log entries in the system. You can view them on the "Logs" page.`
      } else if (lowerMessage.includes('help')) {
        return "I can help you with: checking inventory levels, finding expiring items, understanding NFC scanner usage, and viewing system logs."
      } else {
        return "I'm here to help with medical inventory management. You can ask me about stock levels, expiring items, or how to use the NFC scanner."
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.chat-header {
  padding: 20px;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
}

.chat-header h3 {
  display: flex;
  align-items: center;
}

.chat-header i {
  margin-right: 10px;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.message {
  max-width: 80%;
  padding: 12px 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  line-height: 1.5;
}

.message.bot {
  align-self: flex-start;
  background-color: #f8f9fa;
  border-top-left-radius: 0;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  border-top-right-radius: 0;
}

.chat-input {
  display: flex;
  padding: 15px;
  border-top: 1px solid #e0e0e0;
}

.chat-input input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  margin-left: 10px;
  padding: 12px 20px;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

@media (max-width: 576px) {
  .chat-container {
    height: 400px;
  }
}
</style>