<template>
  <v-container fluid class="dashboard-container">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12">
        <div class="dashboard-header">
          <h1 class="dashboard-title">Dashboard</h1>
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

    <!-- Stats Cards -->
    <v-row class="mb-6" dense>
      <v-col cols="12" md="3" v-for="stat in stats" :key="stat.title">
        <v-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <v-icon :color="stat.color">{{ stat.icon }}</v-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
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
            <div v-if="inventorySummary" class="inventory-grid">
              <div class="inventory-item">
                <div class="inventory-label">Total Items</div>
                <div class="inventory-value">{{ inventorySummary.totalItems }}</div>
              </div>
              <div class="inventory-item">
                <div class="inventory-label">Low Stock</div>
                <div class="inventory-value accent">{{ inventorySummary.lowStock }}</div>
              </div>
              <div class="inventory-item">
                <div class="inventory-label">Expiring Soon</div>
                <div class="inventory-value warning">{{ inventorySummary.expiringSoon }}</div>
              </div>
              <div class="inventory-item">
                <div class="inventory-label">Critical Items</div>
                <div class="inventory-value error">{{ inventorySummary.criticalItems }}</div>
              </div>
            </div>
            <div v-else class="no-data">
              <v-icon color="disabled">mdi-database-off</v-icon>
              <div>No inventory data</div>
            </div>
          </v-card-text>
          
          <v-card-actions>
            <v-btn color="primary" variant="text" @click="fetchInventorySummary">
              View Details
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
            <div v-if="recentActivity.length" class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-icon" :style="{ color: getActivityColor(activity.type) }">
                  <v-icon size="16">{{ getActivityIcon(activity.type) }}</v-icon>
                </div>
                <div class="activity-text">
                  <span class="activity-user">{{ activity.user }}</span>
                  {{ activity.action }}
                </div>
                <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
              </div>
            </div>
            <div v-else class="no-data">
              <v-icon color="disabled">mdi-timeline-clock</v-icon>
              <div>No activity</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()
const isLoading = ref(false)
const inventorySummary = ref(null)
const recentActivity = ref([])

const stats = ref([
  {
    title: 'Total Items',
    value: '0',
    icon: 'mdi-package-variant',
    color: '#4A6CF7'
  },
  {
    title: 'Low Stock',
    value: '0',
    icon: 'mdi-alert-circle',
    color: '#4A6CF7'
  },
  {
    title: 'Expiring Soon',
    value: '0',
    icon: 'mdi-clock-alert',
    color: '#4A6CF7'
  },
  {
    title: 'Today\'s Updates',
    value: '0',
    icon: 'mdi-update',
    color: '#4A6CF7'
  }
])

const PYTHON_BACKEND = {
  baseUrl: 'http://localhost:8000',
  endpoints: {
    inventorySummary: '/api/inventory/summary',
    recentActivity: '/api/activity/recent'
  }
}

const refreshDashboard = async () => {
  isLoading.value = true
  try {
    await Promise.all([
      fetchInventorySummary(),
      fetchRecentActivity()
    ])
  } catch (error) {
    console.error('Error refreshing dashboard:', error)
  } finally {
    isLoading.value = false
  }
}

const fetchInventorySummary = async () => {
  try {
    const response = await callPythonBackend('inventorySummary')
    if (response) {
      inventorySummary.value = response
      stats.value[0].value = response.totalItems?.toString() || '0'
      stats.value[1].value = response.lowStock?.toString() || '0'
      stats.value[2].value = response.expiringSoon?.toString() || '0'
      stats.value[3].value = response.recentUpdates?.toString() || '0'
    }
  } catch (error) {
    console.error('Error fetching inventory summary:', error)
  }
}

const fetchRecentActivity = async () => {
  try {
    const response = await callPythonBackend('recentActivity')
    if (response && Array.isArray(response)) {
      recentActivity.value = response.slice(0, 4)
    }
  } catch (error) {
    console.error('Error fetching recent activity:', error)
  }
}

const callPythonBackend = async (endpoint) => {
  /*
  const response = await fetch(`${PYTHON_BACKEND.baseUrl}${PYTHON_BACKEND.endpoints[endpoint]}`)
  if (!response.ok) throw new Error(`Backend error: ${response.status}`)
  return await response.json()
  */
  
  return new Promise(resolve => {
    setTimeout(() => {
      switch (endpoint) {
        case 'inventorySummary':
          resolve({
            totalItems: inventoryStore.inventory?.length || 0,
            lowStock: inventoryStore.inventory?.filter(item => item.quantity < (item.reorderLevel || 50)).length || 0,
            expiringSoon: inventoryStore.inventory?.filter(item => {
              if (!item.expiryDate) return false
              const daysUntilExpiry = Math.ceil((new Date(item.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))
              return daysUntilExpiry <= 30
            }).length || 0,
            criticalItems: inventoryStore.inventory?.filter(item => item.isCritical).length || 0,
            recentUpdates: 0
          })
          break
        case 'recentActivity':
          resolve([])
          break
        default:
          resolve(null)
      }
    }, 300)
  })
}

const getActivityIcon = (type) => {
  const icons = {
    add: 'mdi-plus',
    update: 'mdi-pencil',
    delete: 'mdi-delete',
    checkout: 'mdi-cart',
    restock: 'mdi-package-down'
  }
  return icons[type] || 'mdi-information'
}

const getActivityColor = (type) => {
  const colors = {
    add: '#4A6CF7',
    update: '#4A6CF7',
    delete: '#4A6CF7',
    checkout: '#4A6CF7',
    restock: '#4A6CF7'
  }
  return colors[type] || '#8E8E93'
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

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

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
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

.stat-card {
  background: #1A1F2E;
  border: 1px solid #2D3447;
  border-radius: 12px;
  padding: 20px;
  height: 100px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  width: 56px;
  height: 56px;
  background: rgba(74, 108, 247, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.stat-icon .v-icon {
  font-size: 28px;
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-title {
  font-size: 14px;
  color: #8E8E93;
  font-weight: 500;
}

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

.card-title .v-icon {
  margin-right: 8px;
}

.v-card-text {
  padding: 20px;
  flex: 1;
}

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
  color: #4A6CF7;
}

.inventory-value.accent {
  color: #4A6CF7;
}

.inventory-value.warning {
  color: #4A6CF7;
}

.inventory-value.error {
  color: #4A6CF7;
}

.activity-content {
  height: 280px;
  padding: 0 !important;
}

.activity-list {
  padding: 20px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #2D3447;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  background: rgba(74, 108, 247, 0.1);
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

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #8E8E93;
}

.no-data .v-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-data div {
  font-size: 16px;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 960px) {
  .dashboard-container {
    padding: 16px;
  }
  
  .dashboard-title {
    font-size: 24px;
  }
  
  .stat-card {
    padding: 16px;
    height: 90px;
  }
  
  .stat-icon {
    width: 48px;
    height: 48px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .inventory-value {
    font-size: 28px;
  }
}

@media (max-width: 600px) {
  .inventory-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-text {
    font-size: 13px;
  }
}
</style>