<template>
  <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <!-- Sidebar Header -->
    <div class="sidebar-header">
      <div class="logo" @click="toggleSidebar">
        <div class="logo-icon">JJS</div>
        <div class="logo-text" v-if="!isCollapsed">
          <span class="logo-primary">Medical</span>
          <span class="logo-secondary">Inventory</span>
        </div>
      </div>
      <button class="toggle-btn" @click="toggleSidebar">
        <i class="icon-menu" v-if="!isCollapsed"></i>
        <i class="icon-chevron-right" v-else></i>
      </button>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="nav-label" v-if="!isCollapsed">Main</div>
        <ul class="nav-list">
          <li>
            <router-link to="/dashboard" class="nav-item" active-class="active">
              <i class="nav-icon icon-dashboard"></i>
              <span class="nav-text" v-if="!isCollapsed">Dashboard</span>
            </router-link>
          </li>
          <li>
            <router-link to="/inventory" class="nav-item" active-class="active">
              <i class="nav-icon icon-inventory"></i>
              <span class="nav-text" v-if="!isCollapsed">Inventory</span>
            </router-link>
          </li>
          <li>
            <router-link to="/locker" class="nav-item" active-class="active">
              <i class="nav-icon icon-locker"></i>
              <span class="nav-text" v-if="!isCollapsed">Locker</span>
            </router-link>
          </li>
          <li>
            <router-link to="/logs" class="nav-item" active-class="active">
              <i class="nav-icon icon-logs"></i>
              <span class="nav-text" v-if="!isCollapsed">Activity Logs</span>
            </router-link>
          </li>
        </ul>
      </div>

      <div class="nav-section">
        <div class="nav-label" v-if="!isCollapsed">Tools</div>
        <ul class="nav-list">
          <li>
            <router-link to="/nfc-scanner" class="nav-item" active-class="active">
              <i class="nav-icon icon-scanner"></i>
              <span class="nav-text" v-if="!isCollapsed">NFC Scanner</span>
            </router-link>
          </li>
          <li>
            <router-link to="/ai-chat" class="nav-item" active-class="active">
              <i class="nav-icon icon-ai"></i>
              <span class="nav-text" v-if="!isCollapsed">AI Assistant</span>
            </router-link>
          </li>
        </ul>
      </div>

      <div class="nav-section" v-if="!isCollapsed">
        <div class="nav-label">System</div>
        <ul class="nav-list">
          <li>
            <router-link to="/reports" class="nav-item" active-class="active">
              <i class="nav-icon icon-reports"></i>
              <span class="nav-text" v-if="!isCollapsed">Reports</span>
            </router-link>
          </li>
          <li>
            <router-link to="/users" class="nav-item" active-class="active">
              <i class="nav-icon icon-users"></i>
              <span class="nav-text" v-if="!isCollapsed">Users</span>
            </router-link>
          </li>
          <li>
            <router-link to="/settings" class="nav-item" active-class="active">
              <i class="nav-icon icon-settings"></i>
              <span class="nav-text" v-if="!isCollapsed">Settings</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- User Profile -->
    <div class="sidebar-footer" v-if="!isCollapsed">
      <div class="user-profile">
        <div class="user-avatar">
          <img :src="user.avatar" :alt="user.name" v-if="user.avatar">
          <div class="avatar-fallback" v-else>{{ getUserInitials(user.name) }}</div>
        </div>
        <div class="user-info">
          <div class="user-name">{{ user.name }}</div>
          <div class="user-role">{{ user.role }}</div>
        </div>
        <button class="logout-btn" @click="logout" title="Logout">
          <i class="icon-logout"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      isCollapsed: false,
      user: {
        name: 'John Doe',
        role: 'Administrator',
        avatar: ''
      }
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
      this.$emit('toggle-collapse', this.isCollapsed)
    },
    getUserInitials(name) {
      return name
        .split(' ')
        .map(part => part.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2)
    },
    logout() {
      this.$emit('logout')
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background: #0f172a;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.sidebar.collapsed {
  width: 70px;
}

/* Sidebar Header */
.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.logo-primary {
  color: #ffffff;
  font-weight: 600;
  font-size: 14px;
}

.logo-secondary {
  color: #94a3b8;
  font-size: 12px;
}

.toggle-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 24px;
}

.nav-label {
  color: #64748b;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 0 20px 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.03);
  color: #e2e8f0;
}

.nav-item.active {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border-right: 3px solid #6366f1;
}

.nav-item.active .nav-icon {
  color: #6366f1;
}

.nav-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Icons */
.icon-dashboard::before {
  content: '📊';
}

.icon-inventory::before {
  content: '📦';
}

.icon-locker::before {
  content: '🔒';
}

.icon-logs::before {
  content: '📝';
}

.icon-scanner::before {
  content: '📱';
}

.icon-ai::before {
  content: '🤖';
}

.icon-reports::before {
  content: '📄';
}

.icon-users::before {
  content: '👥';
}

.icon-settings::before {
  content: '⚙️';
}

.icon-logout::before {
  content: '🚪';
}

.icon-menu::before {
  content: '☰';
}

.icon-chevron-right::before {
  content: '›';
  font-size: 20px;
  font-weight: bold;
}

/* User Profile */
.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  color: #94a3b8;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.2);
}

/* Scrollbar Styling */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* Collapsed State */
.sidebar.collapsed .nav-label,
.sidebar.collapsed .nav-text,
.sidebar.collapsed .logo-text,
.sidebar.collapsed .user-info,
.sidebar.collapsed .logout-btn {
  display: none;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px;
}

.sidebar.collapsed .logo {
  justify-content: center;
}

.sidebar.collapsed .user-profile {
  justify-content: center;
}

.sidebar.collapsed .user-avatar {
  width: 32px;
  height: 32px;
}
</style>