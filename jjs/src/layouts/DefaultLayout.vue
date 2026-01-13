<template>
  <v-app>
    <NavigationDrawer />
    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import NavigationDrawer from '@/components/NavigationDrawer.vue'
</script>

<style scoped>
.v-main {
  background: var(--primary-dark);
  min-height: 100vh;
}
</style>