import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)

  const login = (username, password) => {
    if (username && password) {
      user.value = {
        username,
        role: 'Medical Administrator',
        avatar: username.charAt(0).toUpperCase()
      }
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    }
    return false
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('user')
    router.push('/login')
  }

  const initialize = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
  }

  return { user, isAuthenticated, login, logout, initialize }
})