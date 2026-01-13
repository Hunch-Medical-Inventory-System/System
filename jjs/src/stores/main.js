import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// Auth Store
export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)

  const login = (username, password) => {
    // In production, this would be an API call
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

// Inventory Store
export const useInventoryStore = defineStore('inventory', () => {
  const inventory = ref([])
  const logs = ref([])
  const alerts = ref([])

  const fetchInventory = async () => {
    // Will be replaced with actual API call
    // For now, return empty array
    inventory.value = []
    return []
  }

  const fetchLogs = async () => {
    // Will be replaced with actual API call
    logs.value = []
    return []
  }

  const fetchAlerts = async () => {
    // Will be replaced with actual API call
    alerts.value = []
    return []
  }

  const checkOutItem = async (itemId, quantity, purpose) => {
    // Will be replaced with actual API call
    console.log(`Checking out item ${itemId}, quantity: ${quantity}, purpose: ${purpose}`)
    return true
  }

  return {
    inventory,
    logs,
    alerts,
    fetchInventory,
    fetchLogs,
    fetchAlerts,
    checkOutItem
  }
})