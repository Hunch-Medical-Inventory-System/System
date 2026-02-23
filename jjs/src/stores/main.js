import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)

  const API_BASE = "http://localhost:5000/api"

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email, password) => {
    loading.value = true
    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      })

      if (!res.ok) throw new Error("Login failed")

      const data = await res.json()

      token.value = data.token
      user.value = data.user

      localStorage.setItem("token", data.token)

      return true
    } catch (err) {
      console.error("Login error:", err)
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem("token")
  }

  const fetchUser = async () => {
    if (!token.value) return

    try {
      const res = await fetch(`${API_BASE}/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })

      if (!res.ok) throw new Error("Failed to fetch user")

      user.value = await res.json()
    } catch (err) {
      console.error("User fetch error:", err)
      logout()
    }
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    logout,
    fetchUser
  }
})