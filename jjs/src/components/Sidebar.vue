<template>
  <div :class="['sidebar', { active: isMobileMenuActive }]">
    <ul class="nav-links">
      <li 
        v-for="item in navItems" 
        :key="item.id"
        :class="{ active: activePage === item.id }"
        @click="handleNavigation(item.id)"
      >
        <a href="#">
          <i :class="item.icon"></i> 
          <span>{{ item.label }}</span>
        </a>
      </li>
      <li @click="$emit('logout')">
        <a href="#">
          <i class="fas fa-sign-out-alt"></i> 
          <span>Logout</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    isMobileMenuActive: Boolean,
    activePage: String
  },
  data() {
    return {
      navItems: [
        { id: 'home', label: 'Home', icon: 'fas fa-home' },
        { id: 'locker', label: 'In-Locker', icon: 'fas fa-cube' },
        { id: 'logs', label: 'Logs', icon: 'fas fa-clipboard-list' },
        { id: 'expired', label: 'Expired & Warnings', icon: 'fas fa-exclamation-triangle' },
        { id: 'scanner', label: 'NFC Scanner', icon: 'fas fa-qrcode' },
        { id: 'ai-chat', label: 'AI Chat', icon: 'fas fa-robot' }
      ]
    }
  },
  methods: {
    handleNavigation(page) {
      this.$emit('change-page', page)
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f8f9fa;
  padding: 20px 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.nav-links {
  list-style: none;
}

.nav-links li {
  padding: 15px 25px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-links li:hover {
  background-color: rgba(74, 108, 247, 0.1);
}

.nav-links li.active {
  background-color: rgba(74, 108, 247, 0.2);
  border-left: 4px solid #4a6cf7;
}

.nav-links a {
  color: #333333;
  text-decoration: none;
  display: flex;
  align-items: center;
  font-size: 1rem;
}

.nav-links i {
  margin-right: 15px;
  font-size: 1.2rem;
  color: #4a6cf7;
}

@media (max-width: 992px) {
  .sidebar {
    width: 70px;
  }
  
  .nav-links span {
    display: none;
  }
  
  .nav-links li {
    padding: 15px;
    text-align: center;
  }
  
  .nav-links i {
    margin-right: 0;
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 70px;
    left: 0;
    height: calc(100vh - 70px);
    transform: translateX(-100%);
    z-index: 100;
  }
  
  .sidebar.active {
    transform: translateX(0);
  }
}
</style>