import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// Import styles
import '@/assets/styles.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        colors: {
          primary: '#4a6cf7',
          secondary: '#8a2be2',
          background: '#0a0a0f',
          surface: '#141420',
          'surface-bright': '#252535',
          'surface-variant': '#1e1e2d',
          'on-surface': '#ffffff',
          'on-surface-variant': '#b0b0c0',
          success: '#2ecc71',
          warning: '#f39c12',
          error: '#ff4757',
        }
      }
    }
  }
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(vuetify)
app.mount('#app')