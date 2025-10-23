<!-- components/AppSidebar.vue -->
<template>
  <v-navigation-drawer v-model="internalDrawer">
    <v-list density="compact" nav>
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :value="item.route"
        :to="item.route"
        :prepend-icon="item.icon"
        :title="item.title"
        :active="isActive(item.route)"
      />
    </v-list>

    <template v-slot:append>
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-logout"
          title="Logout"
          @click="handleLogout"
        />
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useInventoryStore } from '@/stores/inventory'

const props = defineProps({
  drawer: Boolean
})

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const inventoryStore = useInventoryStore()

const internalDrawer = computed({
  get: () => props.drawer,
  set: (value) => {
    // Handle drawer state changes if needed
  }
})

const navItems = computed(() => [
  { 
    title: 'Home', 
    icon: 'mdi-home', 
    route: '/' 
  },
  { 
    title: 'In-Locker', 
    icon: 'mdi-package-variant', 
    route: '/locker',
    badge: inventoryStore.totalItems
  },
  { 
    title: 'Logs', 
    icon: 'mdi-clipboard-list', 
    route: '/logs' 
  },
  { 
    title: 'Expired & Warnings', 
    icon: 'mdi-alert', 
    route: '/expired',
    badge: inventoryStore.expiringItems.length + inventoryStore.expiredItems.length
  },
  { 
    title: 'NFC Scanner', 
    icon: 'mdi-qrcode-scan', 
    route: '/scanner' 
  },
  { 
    title: 'AI Chat', 
    icon: 'mdi-robot', 
    route: '/ai-chat' 
  }
])

const isActive = (routePath) => {
  return route.path === routePath
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>