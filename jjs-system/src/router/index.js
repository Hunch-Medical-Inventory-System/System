// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Home', component: () => import('@/pages/Home.vue') },
      { path: '/locker', name: 'Locker', component: () => import('@/pages/Locker.vue') },
      { path: '/logs', name: 'Logs', component: () => import('@/pages/Logs.vue') },
      { path: '/expired', name: 'Expired', component: () => import('@/pages/Expired.vue') },
      { path: '/scanner', name: 'Scanner', component: () => import('@/pages/Scanner.vue') },
      { path: '/ai-chat', name: 'AIChat', component: () => import('@/pages/AIChat.vue') }
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