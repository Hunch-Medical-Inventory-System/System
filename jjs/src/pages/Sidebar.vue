<template>
  <div class="sidebar-glass" :class="{ 'collapsed': isCollapsed }">
    <!-- Glass Header -->
    <div class="glass-header">
      <div class="brand-glow" @click="toggleSidebar">
        <div class="brand-icon">
          <v-icon size="28" color="white">mdi-heart-pulse</v-icon>
        </div>
        <div class="brand-text" v-if="!isCollapsed">
          <span class="brand-name">JJS Medical</span>
          <span class="brand-tagline">Intelligent Inventory</span>
        </div>
      </div>
      <div class="header-actions">
        <v-btn
          icon
          size="small"
          variant="text"
          @click="toggleSidebar"
          class="glass-toggle"
        >
          <v-icon v-if="!isCollapsed">mdi-arrow-left</v-icon>
          <v-icon v-else>mdi-menu</v-icon>
        </v-btn>
      </div>
    </div>

    <!-- Navigation Glass -->
    <div class="nav-glass">
      <!-- Primary Navigation -->
      <div class="nav-section">
        <div class="nav-label" v-if="!isCollapsed">Navigation</div>
        <div class="nav-list">
          <router-link 
            to="/dashboard" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/dashboard' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-view-dashboard-outline</v-icon>
            </div>
            <span class="nav-glass-text" v-if="!isCollapsed">Dashboard</span>
            <div class="nav-glass-badge" v-if="$route.path === '/dashboard'">
              <div class="badge-pulse"></div>
            </div>
          </router-link>

          <router-link 
            to="/inventory" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/inventory' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-medical-bag</v-icon>
            </div>
            <span class="nav-glass-text" v-if="!isCollapsed">Inventory</span>
            <div class="nav-glass-badge" v-if="isCollapsed && inventoryCount > 0">
              <span class="badge-count">{{ inventoryCount }}</span>
            </div>
          </router-link>

          <router-link 
            to="/locker" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/locker' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-shield-lock-outline</v-icon>
            </div>
            <span class="nav-glass-text" v-if="!isCollapsed">Secure Locker</span>
          </router-link>

          <router-link 
            to="/logs" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/logs' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-history</v-icon>
            </div>
            <span class="nav-glass-text" v-if="!isCollapsed">Activity Logs</span>
          </router-link>
        </div>
      </div>

      <!-- Tools Section -->
      <div class="nav-section">
        <div class="nav-label" v-if="!isCollapsed">Tools</div>
        <div class="nav-list">
          <router-link 
            to="/nfc-scanner" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/nfc-scanner' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-nfc-tap</v-icon>
            </div>
            <span class="nav-glass-text" v-if="!isCollapsed">NFC Scanner</span>
          </router-link>

          <router-link 
            to="/ai-chat" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/ai-chat' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-brain</v-icon>
            </div>
            <span class="nav-glass-text" v-if="!isCollapsed">AI Assistant</span>
            <div class="nav-glass-badge" v-if="isCollapsed">
              <div class="badge-ai"></div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Admin Section -->
      <div class="nav-section" v-if="!isCollapsed && user.role === 'admin'">
        <div class="nav-label">Administration</div>
        <div class="nav-list">
          <router-link 
            to="/reports" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/reports' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-chart-box-outline</v-icon>
            </div>
            <span class="nav-glass-text">Analytics</span>
          </router-link>

          <router-link 
            to="/users" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/users' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-account-multiple-outline</v-icon>
            </div>
            <span class="nav-glass-text">Users</span>
          </router-link>

          <router-link 
            to="/settings" 
            class="nav-glass-item" 
            :class="{ 'active': $route.path === '/settings' }"
          >
            <div class="nav-glass-icon">
              <v-icon size="20">mdi-cog-outline</v-icon>
            </div>
            <span class="nav-glass-text">Settings</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Glass Footer -->
    <div class="glass-footer" v-if="!isCollapsed">
      <div class="user-card">
        <div class="user-avatar-glow">
          <div class="avatar-initials">{{ getUserInitials(user.name) }}</div>
          <div class="avatar-status" :class="{ 'online': user.online }"></div>
        </div>
        <div class="user-info">
          <div class="user-name">{{ user.name }}</div>
          <div class="user-role">{{ user.role }}</div>
        </div>
        <v-btn
          icon
          size="small"
          variant="text"
          @click="logout"
          class="logout-glass"
        >
          <v-icon size="20">mdi-power</v-icon>
        </v-btn>
      </div>
    </div>

    <!-- Minimal Footer for Collapsed -->
    <div class="glass-footer-mini" v-else>
      <div class="mini-avatar" @click="toggleSidebar">
        {{ getUserInitials(user.name).charAt(0) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isCollapsed = ref(false)
const inventoryCount = ref(0) // This would come from your store

const user = {
  name: 'John Smith',
  role: 'admin',
  online: true
}

const emit = defineEmits(['toggle-collapse', 'logout'])

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  emit('toggle-collapse', isCollapsed.value)
}

const getUserInitials = (name) => {
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const logout = () => {
  emit('logout')
}
</script>

<style scoped>
.sidebar-glass {
  width: 280px;
  height: 100vh;
  background: rgba(10, 14, 23, 0.8);
  backdrop-filter: blur(30px) saturate(200%);
  -webkit-backdrop-filter: blur(30px) saturate(200%);
  border-right: 1px solid rgba(255, 255, 255, 0.12);
  display: flex;
  flex-direction: column;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  overflow: hidden;
}

.sidebar-glass::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(74, 108, 247, 0.08) 0%,
    rgba(138, 43, 226, 0.04) 50%,
    rgba(10, 14, 23, 0.9) 100%
  );
  pointer-events: none;
  z-index: -1;
}

.sidebar-glass.collapsed {
  width: 80px;
}

/* Glass Header */
.glass-header {
  padding: 24px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  min-height: 80px;
}

.brand-glow {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.brand-glow:hover {
  transform: translateX(4px);
}

.brand-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4A6CF7 0%, #8A2BE2 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 
    0 8px 32px rgba(74, 108, 247, 0.4),
    inset 0 1px 1px rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.brand-icon::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0) 60%
  );
  transform: rotate(30deg);
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}

.brand-name {
  color: #FFFFFF;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
  background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 2px 10px rgba(74, 108, 247, 0.3);
}

.brand-tagline {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.glass-toggle {
  color: rgba(255, 255, 255, 0.7) !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border-radius: 10px !important;
  transition: all 0.3s ease !important;
}

.glass-toggle:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  transform: rotate(90deg);
}

/* Navigation Glass */
.nav-glass {
  flex: 1;
  padding: 24px 16px;
  overflow-y: auto;
  position: relative;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-label {
  color: rgba(255, 255, 255, 0.4);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 16px;
  padding: 0 12px;
  font-family: 'Inter', sans-serif;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-glass-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, 0);
  border: 1px solid transparent;
}

.nav-glass-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0);
  border-radius: 14px;
  z-index: -1;
  transition: background-color 0.3s ease;
}

.nav-glass-item:hover::before {
  background: rgba(255, 255, 255, 0.05);
}

.nav-glass-item:hover {
  color: rgba(255, 255, 255, 0.9);
  transform: translateX(8px);
  border-color: rgba(255, 255, 255, 0.1);
}

.nav-glass-item.active {
  background: linear-gradient(
    135deg,
    rgba(74, 108, 247, 0.2) 0%,
    rgba(138, 43, 226, 0.1) 100%
  );
  backdrop-filter: blur(10px);
  border: 1px solid rgba(74, 108, 247, 0.4);
  box-shadow: 
    0 4px 24px rgba(74, 108, 247, 0.2),
    inset 0 1px 1px rgba(255, 255, 255, 0.1);
  color: #FFFFFF;
}

.nav-glass-item.active .nav-glass-icon {
  background: linear-gradient(135deg, #4A6CF7 0%, #8A2BE2 100%);
  box-shadow: 0 4px 16px rgba(74, 108, 247, 0.4);
}

.nav-glass-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.nav-glass-icon .v-icon {
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.3s ease;
}

.nav-glass-item.active .nav-glass-icon .v-icon {
  color: #FFFFFF;
}

.nav-glass-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  letter-spacing: 0.3px;
}

.nav-glass-badge {
  margin-left: auto;
}

.badge-pulse {
  width: 8px;
  height: 8px;
  background: #4A6CF7;
  border-radius: 50%;
  animation: pulse 2s infinite;
  box-shadow: 0 0 0 0 rgba(74, 108, 247, 0.7);
}

.badge-count {
  background: linear-gradient(135deg, #FF3B30 0%, #FF9500 100%);
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(255, 59, 48, 0.3);
}

.badge-ai {
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, #34C759 0%, #5AC8FA 100%);
  border-radius: 50%;
  animation: glow 2s infinite;
}

/* Glass Footer */
.glass-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.user-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.user-avatar-glow {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4A6CF7 0%, #8A2BE2 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
  box-shadow: 0 8px 24px rgba(74, 108, 247, 0.3);
}

.avatar-initials {
  color: #FFFFFF;
  font-size: 16px;
  font-weight: 700;
}

.avatar-status {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 12px;
  height: 12px;
  background: #34C759;
  border: 2px solid rgba(10, 14, 23, 0.8);
  border-radius: 50%;
}

.avatar-status.online {
  background: #34C759;
  box-shadow: 0 0 0 2px rgba(52, 199, 89, 0.3);
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  font-weight: 500;
}

.logout-glass {
  color: rgba(255, 255, 255, 0.6) !important;
  transition: all 0.3s ease !important;
}

.logout-glass:hover {
  color: #FF3B30 !important;
  transform: scale(1.1) rotate(90deg);
}

/* Mini Footer */
.glass-footer-mini {
  padding: 20px;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.mini-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4A6CF7 0%, #8A2BE2 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(74, 108, 247, 0.3);
}

.mini-avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 32px rgba(74, 108, 247, 0.4);
}

/* Collapsed State */
.sidebar-glass.collapsed .nav-label,
.sidebar-glass.collapsed .nav-glass-text,
.sidebar-glass.collapsed .brand-text,
.sidebar-glass.collapsed .user-info,
.sidebar-glass.collapsed .logout-glass {
  display: none;
}

.sidebar-glass.collapsed .nav-glass-item {
  justify-content: center;
  padding: 16px;
}

.sidebar-glass.collapsed .nav-glass-icon {
  width: 48px;
  height: 48px;
  margin: 0;
}

.sidebar-glass.collapsed .brand-glow {
  justify-content: center;
}

.sidebar-glass.collapsed .glass-header {
  justify-content: center;
  padding: 24px 0;
}

.sidebar-glass.collapsed .header-actions {
  display: none;
}

/* Animations */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(74, 108, 247, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(74, 108, 247, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(74, 108, 247, 0);
  }
}

@keyframes glow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Scrollbar */
.nav-glass::-webkit-scrollbar {
  width: 6px;
}

.nav-glass::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 3px;
}

.nav-glass::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #4A6CF7 0%, #8A2BE2 100%);
  border-radius: 3px;
}

.nav-glass::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #4A6CF7 0%, #FF3B30 100%);
}

/* Responsive */
@media (max-width: 960px) {
  .sidebar-glass:not(.collapsed) {
    width: 260px;
  }
  
  .sidebar-glass.collapsed {
    width: 70px;
  }
}

@media (max-width: 600px) {
  .sidebar-glass:not(.collapsed) {
    width: 100%;
    max-width: 300px;
  }
}
</style>