<template>
  <v-container fluid class="fill-height login-bg">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card
          class="pa-8 login-card"
          elevation="12"
        >
          <div class="text-center mb-8">
            <v-icon
              size="64"
              color="primary"
              class="mb-4"
            >
              mdi-medication
            </v-icon>
            <h1 class="gradient-text text-h3 font-weight-bold mb-2">
              JJs 2.0
            </h1>
            <p class="text-body-1 text-medium-emphasis">
              Medical Inventory Intelligence Platform
            </p>
          </div>

          <v-form @submit.prevent="handleLogin" ref="loginForm">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              :rules="[v => !!v || 'Username is required']"
              class="mb-4"
            />

            <v-text-field
              v-model="password"
              label="Password"
              prepend-inner-icon="mdi-lock"
              variant="outlined"
              :type="showPassword ? 'text' : 'password'"
              :rules="[v => !!v || 'Password is required']"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              class="mb-6"
            />

            <v-btn
              type="submit"
              color="primary"
              size="x-large"
              block
              :loading="loading"
              class="mt-2"
            >
              <v-icon start>mdi-login</v-icon>
              Login to Dashboard
            </v-btn>

            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              class="mt-4"
            >
              {{ error }}
            </v-alert>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/main'

const router = useRouter()
const authStore = useAuthStore()
const loginForm = ref(null)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  const { valid } = await loginForm.value.validate()
  
  if (!valid) return
  
  loading.value = true
  error.value = ''
  
  try {
    const success = authStore.login(username.value, password.value)
    
    if (success) {
      router.push('/')
    } else {
      error.value = 'Invalid credentials'
    }
  } catch (err) {
    error.value = 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-bg {
  background: var(--primary-dark);
  position: relative;
  overflow: hidden;
}

.login-bg::before {
  content: '';
  position: absolute;
  width: 300%;
  height: 300%;
  background: radial-gradient(
    circle,
    rgba(74, 108, 247, 0.1) 0%,
    transparent 70%
  );
  animation: pulse 8s ease-in-out infinite alternate;
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(1); }
  100% { transform: translate(-50%, -50%) scale(1.2); }
}

.login-card {
  background: var(--secondary-dark) !important;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(10px);
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), var(--accent-glow) !important;
}
</style>