<template>
  <v-container fluid class="dashboard-container">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12">
        <div class="dashboard-header">
          <div class="header-left">
            <h1 class="dashboard-title">Dashboard</h1>
            <div class="status-dot" :class="serverOnline ? 'online' : 'offline'">
              <span class="dot-pulse"></span>
              {{ serverOnline ? 'Connected' : 'Offline' }}
            </div>
          </div>
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-refresh"
            @click="refreshDashboard"
            :loading="isLoading"
            size="small"
          >
            Refresh
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Error Banner -->
    <v-row v-if="error" class="mb-4">
      <v-col cols="12">
        <v-alert
          type="error"
          variant="tonal"
          closable
          @click:close="error = null"
          density="compact"
        >
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mb-6" dense>
      <v-col cols="12" md="3" v-for="stat in stats" :key="stat.title">
        <v-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: `${stat.color}18` }">
              <v-icon :color="stat.color" size="28">{{ stat.icon }}</v-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">
                <span v-if="!isLoading">{{ stat.value }}</span>
                <v-skeleton-loader v-else type="text" width="40" />
              </div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Main Content -->
    <v-row>
      <!-- Inventory Status -->
      <v-col cols="12" md="8">
        <v-card class="content-card">
          <v-card-title class="card-title">
            <v-icon color="primary" class="mr-2">mdi-clipboard-list</v-icon>
            Inventory Status
          </v-card-title>

          <v-card-text>
            <div v-if="isLoading" class="inventory-grid">
              <div class="inventory-item" v-for="n in 4" :key="n">
                <v-skeleton-loader type="text" />
                <v-skeleton-loader type="heading" />
              </div>
            </div>
            <div v-else-if="inventorySummary" class="inventory-grid">
              <div class="inventory-item">
                <div class="inventory-label">Total Items</div>
                <div class="inventory-value primary-val">{{ inventorySummary.totalItems }}</div>
              </div>
              <div class="inventory-item">
                <div class="inventory-label">Low Stock</div>
                <div class="inventory-value" :class="inventorySummary.lowStock > 0 ? 'warn-val' : 'ok-val'">
                  {{ inventorySummary.lowStock }}
                </div>
              </div>
              <div class="inventory-item">
                <div class="inventory-label">Expiring Soon</div>
                <div class="inventory-value" :class="inventorySummary.expiringSoon > 0 ? 'warn-val' : 'ok-val'">
                  {{ inventorySummary.expiringSoon }}
                </div>
              </div>
              <div class="inventory-item">
                <div class="inventory-label">Critical Items</div>
                <div class="inventory-value" :class="inventorySummary.criticalItems > 0 ? 'error-val' : 'ok-val'">
                  {{ inventorySummary.criticalItems }}
                </div>
              </div>
            </div>
            <div v-else class="no-data">
              <v-icon color="disabled" size="48">mdi-database-off</v-icon>
              <div>No inventory data</div>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn color="primary" variant="text" @click="fetchInventorySummary" :loading="isLoading">
              Refresh Data
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Recent Activity -->
      <v-col cols="12" md="4">
        <v-card class="content-card">
          <v-card-title class="card-title">
            <v-icon color="accent" class="mr-2">mdi-history</v-icon>
            Recent Activity
          </v-card-title>

          <v-card-text class="activity-content">
            <div v-if="isLoading" class="activity-list">
              <div class="activity-item" v-for="n in 4" :key="n">
                <v-skeleton-loader type="list-item-avatar" />
              </div>
            </div>
            <div v-else-if="recentActivity.length" class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-icon" :style="{ background: getActivityColor(activity.type) + '22' }">
                  <v-icon :color="getActivityColor(activity.type)" size="16">
                    {{ getActivityIcon(activity.type) }}
                  </v-icon>
                </div>
                <div class="activity-text">
                  <span class="activity-user">{{ activity.user }}</span>
                  {{ activity.action }}
                </div>
                <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
              </div>
            </div>
            <div v-else class="no-data">
              <v-icon color="disabled" size="48">mdi-timeline-clock</v-icon>
              <div>No recent activity</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// --------------------------------------------------
// Config
// --------------------------------------------------

const API_BASE = 'http://localhost:8080'

const api = {
  async get(path) {
    const response = await fetch(`${API_BASE}${path}`)
    if (!response.ok) throw new Error(`Server error: ${response.status}`)
    return response.json()
  },
  async post(path, body) {
    const response = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    if (!response.ok) throw new Error(`Server error: ${response.status}`)
    return response.json()
  }
}

// --------------------------------------------------
// State
// --------------------------------------------------

const isLoading = ref(false)
const serverOnline = ref(false)
const error = ref(null)
const inventorySummary = ref(null)
const recentActivity = ref([])

const stats = ref([
  { title: 'Total Items',     value: '—', icon: 'mdi-package-variant', color: '#4A6CF7' },
  { title: 'Low Stock',       value: '—', icon: 'mdi-alert-circle',    color: '#FF9800' },
  { title: 'Expiring Soon',   value: '—', icon: 'mdi-clock-alert',     color: '#FF5722' },
  { title: "Today's Updates", value: '—', icon: 'mdi-update',          color: '#4CAF50' },
])

// --------------------------------------------------
// Data Fetching
// --------------------------------------------------

const checkHealth = async () => {
  try {
    await api.get('/api/health')
    serverOnline.value = true
  } catch {
    serverOnline.value = false
    error.value = 'Cannot reach server at localhost:8000 — is it running?'
  }
}

const fetchInventorySummary = async () => {
  try {
    const data = await api.get('/api/inventory/summary')
    inventorySummary.value = data

    stats.value[0].value = data.totalItems?.toString()   ?? '0'
    stats.value[1].value = data.lowStock?.toString()     ?? '0'
    stats.value[2].value = data.expiringSoon?.toString() ?? '0'
    stats.value[3].value = data.recentUpdates?.toString() ?? '0'
  } catch (err) {
    error.value = `Failed to load inventory summary: ${err.message}`
  }
}

const fetchRecentActivity = async () => {
  try {
    const data = await api.get('/api/activity/recent?amount=6')
    recentActivity.value = Array.isArray(data) ? data : []
  } catch (err) {
    error.value = `Failed to load activity: ${err.message}`
  }
}

const refreshDashboard = async () => {
  isLoading.value = true
  error.value = null
  try {
    await checkHealth()
    if (serverOnline.value) {
      await Promise.all([fetchInventorySummary(), fetchRecentActivity()])
    }
  } finally {
    isLoading.value = false
  }
}

// --------------------------------------------------
// Helpers
// --------------------------------------------------

const getActivityIcon = (type) => ({
  add:      'mdi-plus',
  update:   'mdi-pencil',
  delete:   'mdi-delete',
  checkout: 'mdi-cart',
  restock:  'mdi-package-down'
}[type] ?? 'mdi-information')

const getActivityColor = (type) => ({
  add:      '#4A6CF7',
  update:   '#4CAF50',
  delete:   '#F44336',
  checkout: '#FF9800',
  restock:  '#9C27B0'
}[type] ?? '#8E8E93')

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return isNaN(date.getTime())
    ? timestamp
    : date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// --------------------------------------------------
// Init
// --------------------------------------------------

onMounted(() => {
  refreshDashboard()
})
</script>

<style scoped>
.dashboard-container {
  height: 100%;
  background: linear-gradient(135deg, #0A0E17 0%, #1A1F2E 100%);
  padding: 24px;
  overflow-y: auto;
}

/* Header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.dashboard-title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(90deg, #4A6CF7 0%, #8A2BE2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

/* Server status dot */
.status-dot {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid;
}

.status-dot.online {
  color: #4CAF50;
  border-color: #4CAF5044;
  background: #4CAF5011;
}

.status-dot.offline {
  color: #F44336;
  border-color: #F4433644;
  background: #F4433611;
}

.dot-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* Stat Cards */
.stat-card {
  background: #1A1F2E;
  border: 1px solid #2D3447;
  border-radius: 12px;
  padding: 20px;
  height: 100px;
  transition: border-color 0.2s;
}

.stat-card:hover {
  border-color: #4A6CF755;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.stat-info { flex: 1; min-width: 0; }

.stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1;
  margin-bottom: 4px;
  min-height: 34px;
}

.stat-title {
  font-size: 14px;
  color: #8E8E93;
  font-weight: 500;
}

/* Content cards */
.content-card {
  background: #1A1F2E;
  border: 1px solid #2D3447;
  border-radius: 12px;
  height: 100%;
}

.card-title {
  color: #FFFFFF;
  font-weight: 600;
  padding: 20px 20px 0 20px;
}

/* Inventory grid */
.inventory-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.inventory-item {
  background: #2D3447;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.inventory-label {
  font-size: 14px;
  color: #8E8E93;
  margin-bottom: 8px;
}

.inventory-value {
  font-size: 36px;
  font-weight: 800;
}

.primary-val { color: #4A6CF7; }
.ok-val      { color: #4CAF50; }
.warn-val    { color: #FF9800; }
.error-val   { color: #F44336; }

/* Activity */
.activity-content {
  height: 280px;
  overflow-y: auto;
  padding: 0 !important;
}

.activity-list { padding: 20px; }

.activity-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #2D3447;
}

.activity-item:last-child { border-bottom: none; }

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.activity-text {
  flex: 1;
  font-size: 14px;
  color: #FFFFFF;
  line-height: 1.4;
  min-width: 0;
  word-wrap: break-word;
}

.activity-user {
  font-weight: 600;
  color: #4A6CF7;
  margin-right: 4px;
}

.activity-time {
  font-size: 12px;
  color: #8E8E93;
  margin-left: 12px;
  flex-shrink: 0;
}

/* Empty state */
.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #8E8E93;
  gap: 12px;
}

.no-data div {
  font-size: 16px;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 960px) {
  .dashboard-container { padding: 16px; }
  .dashboard-title { font-size: 24px; }
  .stat-card { padding: 16px; height: 90px; }
  .stat-icon { width: 48px; height: 48px; }
  .stat-value { font-size: 24px; }
  .inventory-value { font-size: 28px; }
}

@media (max-width: 600px) {
  .inventory-grid { grid-template-columns: 1fr; }
  .activity-text { font-size: 13px; }
  .header-left { flex-direction: column; align-items: flex-start; gap: 8px; }
}
</style>