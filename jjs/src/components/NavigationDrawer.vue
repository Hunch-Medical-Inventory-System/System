<template>
  <v-navigation-drawer
    v-model="drawer"
    :rail="rail"
    permanent
    app
    width="280"
    class="bg-surface"
  >
    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-alpha-j-box"
        title="JJs V2.0"
        subtitle="Medical Inventory"
        class="mb-4"
      >
        <template v-slot:prepend>
          <v-icon size="large" color="primary">mdi-alpha-j-box</v-icon>
        </template>
      </v-list-item>

      <v-divider class="mb-4" />

      <v-list-item
        v-for="item in navigation"
        :key="item.title"
        :prepend-icon="item.icon"
        :title="item.title"
        :value="item.route"
        :to="{ name: item.route }"
        active-class="gradient-active"
        :class="{ 'gradient-active': $route.name === item.route }"
      >
        <template v-slot:prepend>
          <v-icon>{{ item.icon }}</v-icon>
        </template>

        <template v-slot:append v-if="item.badge">
          <v-badge
            :color="item.badgeColor"
            :content="item.badge"
            inline
          />
        </template>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-account-circle"
          :title="authStore.user?.username || 'User'"
          :subtitle="authStore.user?.role || 'Medical Staff'"
        />
        <v-list-item
          prepend-icon="mdi-logout"
          title="Logout"
          @click="authStore.logout"
        />
      </v-list>
    </template>
  </v-navigation-drawer>

  <v-app-bar
    app
    color="surface"
    border
    elevation="0"
  >
    <v-app-bar-nav-icon @click="rail = !rail" />
    <v-app-bar-title class="gradient-text font-weight-bold">
      {{ currentPageTitle }}
    </v-app-bar-title>

    <v-spacer />

    <v-btn icon @click="toggleTheme">
      <v-icon>mdi-theme-light-dark</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useInventoryStore } from '@/stores/inventory'

const route = useRoute()
const authStore = useAuthStore()
const inventoryStore = useInventoryStore()

const drawer = ref(true)
const rail = ref(false)

const pageTitles = {
  Dashboard: 'Dashboard Overview',
  Inventory: 'Inventory Management',
  ActivityLogs: 'System Logs',
  Alerts: 'System Alerts',
  Scanner: 'NFC Scanner',
  AIChat: 'AI Assistant'
}

const currentPageTitle = computed(() => {
  return pageTitles[route.name] || 'Medical Inventory System'
})

const navigation = computed(() => [
  {
    title: 'Dashboard',
    icon: 'mdi-view-dashboard',
    route: 'Dashboard'
  },
  {
    title: 'Inventory',
    icon: 'mdi-cube',
    route: 'Inventory',
    badge: inventoryStore.inventory?.length || 0,
    badgeColor: 'success'
  },
  {
    title: 'Activity Logs',
    icon: 'mdi-history',
    route: 'ActivityLogs',
    badge: inventoryStore.logs?.length || 0,
    badgeColor: 'warning'
  },
  {
    title: 'Alerts',
    icon: 'mdi-alert',
    route: 'Alerts',
    badge: inventoryStore.alerts?.length || 0,
    badgeColor: 'error'
  },
  {
    title: 'NFC Scanner',
    icon: 'mdi-nfc',
    route: 'Scanner'
  },
  {
    title: 'AI Assistant',
    icon: 'mdi-robot',
    route: 'AIChat'
  }
])

const toggleTheme = () => {
  // Theme toggle logic will be implemented later
  console.log('Toggle theme')
}
</script>

<style scoped>
.gradient-active {
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)) !important;
  color: white !important;
}

.gradient-active .v-icon {
  color: white !important;
}
</style>