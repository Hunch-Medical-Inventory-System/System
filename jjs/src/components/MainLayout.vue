<template>
  <div class="layout">
    <Sidebar :collapsed="sidebarCollapsed" @toggle="toggleSidebar" />
    <div class="content-wrapper" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <router-view v-slot="{ Component }">
        <component 
          :is="Component" 
          :key="$route.fullPath"
          @toggle-sidebar="toggleSidebar"
        />
      </router-view>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'

export default {
  name: 'MainLayout',
  components: {
    Sidebar
  },
  setup() {
    const sidebarCollapsed = ref(false)
    
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }
    
    return {
      sidebarCollapsed,
      toggleSidebar
    }
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  background: #0f172a;
}

.content-wrapper {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
  overflow-x: hidden;
}

.content-wrapper.sidebar-collapsed {
  margin-left: 70px;
}

@media (max-width: 768px) {
  .content-wrapper {
    margin-left: 0;
  }
  
  .content-wrapper.sidebar-collapsed {
    margin-left: 0;
  }
}
</style>