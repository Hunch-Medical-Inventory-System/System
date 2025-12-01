<template>
  <div id="app">
    <!-- Login Page -->
    <Login 
      v-if="!isLoggedIn" 
      @login="handleLogin"
    />
    
    <!-- Main Application -->
    <div v-else class="app-container">
      <Header 
        :user="currentUser"
        @toggle-mobile-menu="toggleMobileMenu"
      />
      
      <div class="nav-container">
        <Sidebar 
          :is-mobile-menu-active="isMobileMenuActive"
          :active-page="activePage"
          @change-page="changePage"
          @logout="handleLogout"
        />
        
        <div class="main-content">
          <!-- Dashboard Page -->
          <Dashboard 
            v-if="activePage === 'home'"
            :inventory="inventory"
            :logs="logs"
          />
          
          <!-- In-Locker Page -->
          <Locker 
            v-if="activePage === 'locker'"
            :inventory="inventory"
            @use-item="useItem"
            @dispose-item="disposeItem"
          />
          
          <!-- Logs Page -->
          <Logs 
            v-if="activePage === 'logs'"
            :logs="logs"
          />
          
          <!-- Expired & Warnings Page -->
          <Warnings 
            v-if="activePage === 'expired'"
            :inventory="inventory"
            @use-item="useItem"
            @dispose-item="disposeItem"
          />
          
          <!-- NFC Scanner Page -->
          <Scanner 
            v-if="activePage === 'scanner'"
            :inventory="inventory"
            @checkout-item="useItem"
            @add-item="addItem"
          />
          
          <!-- AI Chat Page -->
          <AiChat 
            v-if="activePage === 'ai-chat'"
            :inventory="inventory"
            :logs="logs"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Login from '@/components/Login.vue'
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import Dashboard from '@/components/Dashboard.vue'
import Locker from '@/components/Locker.vue'
import Logs from '@/components/Logs.vue'
import Warnings from '@/components/Warnings.vue'
import Scanner from '@/components/Scanner.vue'
import AiChat from '@/components/AiChat.vue'

export default {
  name: 'App',
  components: {
    Login,
    Header,
    Sidebar,
    Dashboard,
    Locker,
    Logs,
    Warnings,
    Scanner,
    AiChat
  },
  data() {
    return {
      isLoggedIn: false,
      currentUser: null,
      activePage: 'home',
      isMobileMenuActive: false,
      inventory: JSON.parse(localStorage.getItem('inventory')) || [],
      logs: JSON.parse(localStorage.getItem('logs')) || []
    }
  },
  created() {
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      this.currentUser = JSON.parse(savedUser)
      this.isLoggedIn = true
    }
  },
  methods: {
    handleLogin(user) {
      this.currentUser = user
      this.isLoggedIn = true
      this.addLog('System', 'Login', `${user.username} logged in`)
    },
    handleLogout() {
      this.addLog('System', 'Logout', `${this.currentUser.username} logged out`)
      this.currentUser = null
      this.isLoggedIn = false
      localStorage.removeItem('currentUser')
    },
    changePage(page) {
      this.activePage = page
      this.isMobileMenuActive = false
    },
    toggleMobileMenu() {
      this.isMobileMenuActive = !this.isMobileMenuActive
    },
    addLog(user, action, details, item = null) {
      const now = new Date()
      const timestamp = `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`
      
      this.logs.push({
        timestamp,
        user,
        action,
        item,
        details
      })
      
      localStorage.setItem('logs', JSON.stringify(this.logs))
    },
    useItem(item, quantity = 1) {
      const itemIndex = this.inventory.findIndex(i => i.id === item.id)
      
      if (itemIndex !== -1) {
        if (this.inventory[itemIndex].quantity >= quantity) {
          this.inventory[itemIndex].quantity -= quantity
          
          if (this.inventory[itemIndex].quantity === 0) {
            this.inventory.splice(itemIndex, 1)
          }
          
          this.saveInventory()
          this.addLog(this.currentUser.username, 'Check Out', `Quantity: ${quantity}`, item.name)
        }
      }
    },
    disposeItem(item) {
      const itemIndex = this.inventory.findIndex(i => i.id === item.id)
      
      if (itemIndex !== -1) {
        this.inventory.splice(itemIndex, 1)
        this.saveInventory()
        this.addLog(this.currentUser.username, 'Dispose', 'Item disposed', item.name)
      }
    },
    addItem(item) {
      this.inventory.push(item)
      this.saveInventory()
      this.addLog(this.currentUser.username, 'Add', `New item added: ${item.name}`, item.name)
    },
    saveInventory() {
      localStorage.setItem('inventory', JSON.stringify(this.inventory))
    },
    getItemStatus(item) {
      const expiryDate = new Date(item.expiryDate)
      const today = new Date()
      const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
      
      if (daysUntilExpiry < 0) {
        return { class: 'expired', text: 'Expired' }
      } else if (daysUntilExpiry <= 30) {
        return { class: 'warning', text: 'Expiring Soon' }
      } else {
        return { class: 'ok', text: 'OK' }
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.nav-container {
  display: flex;
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: #ffffff;
  overflow-y: auto;
}
</style>