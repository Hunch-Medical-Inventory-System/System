// src/stores/auth.js
import { defineStore } from 'pinia'
import { authService } from '@/services/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
  }),

  actions: {
    async login(credentials) {
      try {
        const response = await authService.login(credentials)
        this.user = response.user
        this.token = response.token
        this.isAuthenticated = true

        localStorage.setItem('token', response.token)
        localStorage.setItem('user', JSON.stringify(response.user))

        return { success: true }
      } catch (error) {
        return { success: false, error: error.message }
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false

      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    initialize() {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')

      if (token && user) {
        this.token = token
        this.user = JSON.parse(user)
        this.isAuthenticated = true
      } else {
        this.token = null
        this.user = null
        this.isAuthenticated = false
      }
    },
  },
})
