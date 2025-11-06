// src/services/auth.js
export const authService = {
  async login({ email, password }) {
    if (email === 'test@example.com' && password === '1234') {
      return {
        user: { id: 1, name: 'Test User', email },
        token: 'fake-jwt-token'
      }
    } else {
      throw new Error('Invalid email or password')
    }
  },

  async register(userData) {
    console.log('Registered user:', userData)
    return { message: 'User registered successfully' }
  },

  logout() {
    // optional backend logout logic
  }
}
