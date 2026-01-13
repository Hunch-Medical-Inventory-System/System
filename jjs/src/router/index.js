import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/main'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/pages/Dashboard.vue')
      },
      {
        path: 'inventory',
        name: 'Inventory',
        component: () => import('@/pages/Inventory.vue')
      },
      {
        path: 'logs',
        name: 'ActivityLogs',
        component: () => import('@/pages/ActivityLogs.vue')
      },
      {
        path: 'alerts',
        name: 'Alerts',
        component: () => import('@/pages/Alerts.vue')
      },
      {
        path: 'scanner',
        name: 'Scanner',
        component: () => import('@/pages/Scanner.vue')
      },
      {
        path: 'ai-chat',
        name: 'AIChat',
        component: () => import('@/pages/AiChat.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router