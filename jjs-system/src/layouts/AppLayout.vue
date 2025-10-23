<!-- layouts/AppLayout.vue -->
<template>
  <v-layout>
    <AppSidebar :drawer="drawer" />
    
    <v-app-bar color="primary" density="compact">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      
      <v-app-bar-title>
        <span class="font-weight-bold">JJs</span>
        <span class="text-grey-lighten-1"> V2.0</span>
      </v-app-bar-title>

      <v-spacer />

      <v-btn icon>
        <v-icon>mdi-bell</v-icon>
        <v-badge v-if="expiringItems.length > 0" color="error" :content="expiringItems.length" />
      </v-btn>

      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon>
            <v-avatar size="32" color="primary">
              <span class="text-white">{{ userInitials }}</span>
            </v-avatar>
          </v-btn>
        </template>
        
        <v-list>
          <v-list-item>
            <v-list-item-title>{{ user?.name || 'Demo User' }}</v-list-item-title>
            <v-list-item-subtitle>{{ user?.role || 'User' }}</v-list-item-subtitle>
          </v-list-item>
          <v-divider />
          <v-list-item @click="handleLogout">
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useInventoryStore } from '@/stores/inventory'
import AppSidebar from '@/components/AppSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()
const inventoryStore = useInventoryStore()

const drawer = ref(true)

const user = computed(() => authStore.user)
const expiringItems = computed(() => inventoryStore.expiringItems)

const userInitials = computed(() => {
  if (!user.value?.name) return 'DU'
  return user.value.name.split(' ').map(n => n[0]).join('').toUpperCase()
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>