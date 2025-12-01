<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-logo">
        <h1>JJs 2.0</h1>
        <p>Medical Inventory System</p>
      </div>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="username"
            placeholder="Enter your username" 
            required
          >
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password"
            placeholder="Enter your password" 
            required
          >
        </div>
        <button type="submit" class="login-btn">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    handleSubmit() {
      if (this.username && this.password) {
        const user = {
          username: this.username,
          role: 'DEMO'
        }
        localStorage.setItem('currentUser', JSON.stringify(user))
        this.$emit('login', user)
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #4a6cf7, #8a2be2);
  padding: 20px;
}

.login-box {
  background-color: white;
  border-radius: 10px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.login-logo {
  text-align: center;
  margin-bottom: 30px;
}

.login-logo h1 {
  font-size: 2.2rem;
  color: #4a6cf7;
}

.login-logo p {
  color: #666666;
  margin-top: 5px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1rem;
  transition: border 0.3s;
}

.form-group input:focus {
  border-color: #4a6cf7;
  outline: none;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.login-btn:hover {
  opacity: 0.9;
}

@media (max-width: 576px) {
  .login-box {
    padding: 30px 20px;
  }
}
</style>