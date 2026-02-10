<template>
  <div class="chat-container">
    <!-- Header -->
    <div class="chat-header">
      <div class="header-content">
        <h1 class="chat-title">JJs V2AI Assistant</h1>
        <v-btn
          color="primary"
          variant="flat"
          size="small"
          class="clear-btn"
          @click="clearChat"
          prepend-icon="mdi-delete-sweep"
        >
          Clear Chat
        </v-btn>
      </div>
      <div class="chat-subtitle">
        Ask questions about medical inventory, drug interactions, or pharmaceutical information
      </div>
    </div>

    <!-- Messages Container -->
    <v-card class="messages-card">
      <div class="messages-container" ref="messagesContainer">
        <!-- Welcome Message -->
        <div v-if="!messages.length" class="welcome-message">
          <div class="welcome-icon">
            <v-icon color="primary" size="64">mdi-robot-happy</v-icon>
          </div>
          <h3 class="welcome-title">Welcome to the JJs V2 MedAI Assistant</h3>
          <p class="welcome-text">
            I'm here to help you with medical inventory management, 
            drug information, and pharmaceutical queries.
          </p>
          <div class="suggestions">
            <v-chip
              v-for="(suggestion, i) in suggestions"
              :key="i"
              class="suggestion-chip"
              variant="outlined"
              @click="useSuggestion(suggestion)"
            >
              {{ suggestion }}
            </v-chip>
          </div>
        </div>

        <!-- Chat Messages -->
        <div v-else class="messages-list">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message-wrapper"
            :class="msg.role"
          >
            <div class="message-content">
              <div class="message-header">
                <div class="message-avatar">
                  <v-icon v-if="msg.role === 'user'" color="#4A6CF7">mdi-account</v-icon>
                  <v-icon v-else color="#4A6CF7">mdi-robot</v-icon>
                </div>
                <div class="message-role">
                  {{ msg.role === 'user' ? 'You' : 'MedLlama2' }}
                </div>
                <div class="message-time">
                  {{ formatMessageTime(msg.timestamp) }}
                </div>
              </div>
              <div class="message-text" v-html="formatMessage(msg.content)"></div>
            </div>
          </div>
          
          <!-- Loading Indicator -->
          <div v-if="isLoading" class="loading-indicator">
            <div class="typing-dots">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
            <span class="loading-text">JJs V2 is thinking...</span>
          </div>
        </div>
      </div>
    </v-card>

    <!-- Input Area -->
    <v-card class="input-card">
      <div class="input-container">
        <v-textarea
          v-model="userInput"
          class="message-input"
          variant="outlined"
          placeholder="Type your medical or inventory question here..."
          rows="2"
          auto-grow
          hide-details
          @keydown.enter.exact.prevent="sendMessage"
          :loading="isLoading"
          :disabled="isLoading"
        >
          <template v-slot:append-inner>
            <v-btn
              color="primary"
              variant="flat"
              :loading="isLoading"
              :disabled="!userInput.trim() || isLoading"
              @click="sendMessage"
              class="send-btn"
              size="small"
            >
              <v-icon>mdi-send</v-icon>
            </v-btn>
          </template>
        </v-textarea>
        
        <div class="input-hints">
          <v-icon size="16" color="#8E8E93">mdi-information</v-icon>
          <span>Press Enter to send • Shift+Enter for new line</span>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'

/* ---------------- CORE STATE ---------------- */

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const messagesContainer = ref(null)

/* ---------------- CREW / DB CONTEXT ---------------- */
/*
  🔌 These will later be populated from your DB (Supabase, etc.)
  For now, placeholders that already work with the AI.
*/

const crewContext = ref({
  role: 'Crew Medical Technician',
  clearance: 'Level 2',
  environment: 'Orbital / Space Station',
})

const inventoryContext = ref({
  criticalSupplies: [
    'Ibuprofen',
    'Epinephrine',
    'Insulin',
    'Saline',
  ],
})

/* ---------------- SUGGESTIONS ---------------- */

const suggestions = ref([
  'Ibuprofen storage status',
  'Insulin refrigeration check',
  'Low-level diagnostic: fever',
  'Critical inventory warnings'
])

/* ---------------- FORMATTERS ---------------- */

const formatMessage = (content) => {
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

const formatMessageTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

/* ---------------- UI HELPERS ---------------- */

const clearChat = () => {
  messages.value = []
}

const useSuggestion = (suggestion) => {
  userInput.value = suggestion
  sendMessage()
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop =
        messagesContainer.value.scrollHeight
    }
  })
}

/* ---------------- SYSTEM PROMPT ---------------- */
/*
  🚀 This is the KEY upgrade:
  - Short answers
  - Space context
  - Crew-only tone
  - Low-level diagnostics
*/

const systemPrompt = () => `
You are JJs V2AI, a space-mission medical and inventory assistant. 

CONTEXT:
- Environment: ${crewContext.value.environment}
- Crew Role: ${crewContext.value.role}
- Clearance: ${crewContext.value.clearance}

RULES:
- Responses MUST be concise.
- Prefer bullet points or numbered steps.
- Assume crew member has medical training.
- Perform low-level diagnostics only (no speculation).
- Flag missing or critical inventory issues.
- No emojis. No filler. No disclaimers.

AVAILABLE INVENTORY:
${inventoryContext.value.criticalSupplies.join(', ')}

If unsure, ask ONE short clarifying question.
`

/* ---------------- MAIN CHAT LOGIC ---------------- */

async function sendMessage() {
  const input = userInput.value.trim()
  if (!input || isLoading.value) return

  const userMessage = {
    role: 'user',
    content: input,
    timestamp: new Date().toISOString(),
  }

  messages.value.push(userMessage)
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const payloadMessages = [
      { role: 'system', content: systemPrompt() },
      ...messages.value.map(({ role, content }) => ({ role, content })),
    ]

    const res = await fetch('/ollama/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'medllama2',
        messages: payloadMessages,
        temperature: 0.2,        // 🔒 tighter, factual
        max_tokens: 300,         
        stream: false,
      }),
    })

    if (!res.ok) {
      throw new Error(`Ollama error ${res.status}`)
    }

    const data = await res.json()
    const reply = data.choices[0].message.content

    messages.value.push({
      role: 'assistant',
      content: reply,
      timestamp: new Date().toISOString(),
    })
  } catch (err) {
    console.error('Chat error:', err)
    messages.value.push({
      role: 'assistant',
      content:
        'Connection failure. Verify Ollama service and model availability.',
      timestamp: new Date().toISOString(),
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

/* ---------------- WATCHERS ---------------- */

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  scrollToBottom()
})
</script>


<style scoped>
.chat-container {
  height: 100vh;
  background: linear-gradient(135deg, #0A0E17 0%, #1A1F2E 100%);
  padding: 24px;
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

.messages-card {
  background: #1A1F2E;
  border: 1px solid #2D3447;
  border-radius: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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

.message-wrapper.user {
  align-self: flex-end;
  max-width: 80%;
}

.message-wrapper.assistant {
  align-self: flex-start;
  max-width: 80%;
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
  font-size: 14px;
  color: #FFFFFF;
  line-height: 1.6;
  word-wrap: break-word;
}

.message-text strong {
  color: #4A6CF7;
}

.message-text em {
  color: #8E8E93;
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
  gap: 4px;
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

.input-container {
  padding: 20px;
}

.message-input {
  background: #2D3447;
  border-radius: 8px;
}

.message-input :deep(.v-field__outline) {
  border-color: rgba(74, 108, 247, 0.3) !important;
}

.message-input :deep(.v-field__input) {
  color: #FFFFFF !important;
  font-size: 14px;
}

.message-input :deep(.v-field__append-inner) {
  align-self: flex-end;
  padding-bottom: 8px;
}

.send-btn {
  min-width: 40px !important;
  height: 40px !important;
}

.input-hints {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 12px;
  color: #8E8E93;
}

/* Custom scrollbar */
.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-container::-webkit-scrollbar-track {
  background: #2D3447;
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #4A6CF7;
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #3A5BD6;
}

/* Responsive */
@media (max-width: 960px) {
  .chat-container {
    padding: 16px;
  }
  
  .chat-title {
    font-size: 24px;
  }
  
  .messages-container {
    max-height: calc(100vh - 240px);
    padding: 16px;
  }
  
  .message-wrapper.user,
  .message-wrapper.assistant {
    max-width: 90%;
  }
}

@media (max-width: 600px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .clear-btn {
    align-self: flex-end;
  }
  
  .message-wrapper.user,
  .message-wrapper.assistant {
    max-width: 95%;
  }
  
  .suggestions {
    justify-content: flex-start;
  }
}
</style>