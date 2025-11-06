<!-- pages/Login.vue -->
<template>
  <v-container fluid class="login-container">
    <v-row justify="center" align="center" class="h-100">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="login-card" elevation="12">
          <v-card-item class="text-center pa-6">
            <v-card-title class="text-h4 font-weight-bold">
              <span class="primary--text">JJs</span>
              <span class="secondary--text"> 2.0</span>
            </v-card-title>
            <v-card-subtitle class="text-h6">
              Medical Inventory System
            </v-card-subtitle>
          </v-card-item>

          <v-card-text class="pa-6">
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="credentials.username"
                label="Username"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                class="mb-4"
                :error-messages="errors.username"
                required
              />

              <v-text-field
                v-model="credentials.password"
                label="Password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                type="password"
                class="mb-4"
                :error-messages="errors.password"
                required
              />

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
              >
                Login
              </v-btn>
            </v-form>

            <v-alert
              v-if="loginError"
              type="error"
              class="mt-4"
            >
              {{ loginError }}
            </v-alert>

            <v-alert
              type="info"
              class="mt-4"
            >
              <strong>Demo Credentials:</strong><br>
              Username: demo<br>
              Password: demo
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const loginError = ref('')
const credentials = reactive({
  username: '',
  password: ''
})
const errors = reactive({
  username: '',
  password: ''
})

const validateForm = () => {
  let valid = true
  errors.username = ''
  errors.password = ''

  if (!credentials.username) {
    errors.username = 'Username is required'
    valid = false
  }

  if (!credentials.password) {
    errors.password = 'Password is required'
    valid = false
  }

  return valid
}

const handleLogin = async () => {
  if (!validateForm()) return

  loading.value = true
  loginError.value = ''

  const result = await authStore.login(credentials)
  
  if (result.success) {
    router.push('/')
  } else {
    loginError.value = result.error || 'Login failed'
  }
  
  loading.value = false
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #4a6cf7, #8a2be2);
}

.h-100 {
  height: 100%;
}

.login-card {
  border-radius: 12px;
}
</style>