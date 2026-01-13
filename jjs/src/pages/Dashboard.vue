<template>
  <div class="page-transition">
    <div class="page-header">
      <h2>Dashboard Overview</h2>
      <p>Welcome back! Here's what's happening with your medical inventory today.</p>
    </div>
    
    <div class="dashboard-cards">
      <v-card class="gradient-card" v-for="card in cards" :key="card.title">
        <div class="card-icon">
          <v-icon>{{ card.icon }}</v-icon>
        </div>
        <h3>{{ card.value }}</h3>
        <p>{{ card.title }}</p>
        <div class="card-trend" :class="card.trend">
          <v-icon small>{{ card.trendIcon }}</v-icon>
          {{ card.trendText }}
        </div>
      </v-card>
    </div>
    
    <div class="page-header">
      <h2>Recent Activity</h2>
      <p>Latest actions and updates in your inventory system</p>
    </div>
    
    <v-card class="gradient-card">
      <v-table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Action</th>
            <th>User</th>
            <th>Date & Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="activity in recentActivities" :key="activity.id">
            <td>{{ activity.item }}</td>
            <td>{{ activity.action }}</td>
            <td>
              <v-chip size="small">{{ activity.user }}</v-chip>
            </td>
            <td>{{ activity.timestamp }}</td>
            <td>
              <span class="status-badge" :class="activity.statusClass">
                {{ activity.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </v-table>
      <div v-if="!recentActivities.length" class="empty-state">
        <v-icon size="48">mdi-clipboard-list</v-icon>
        <h3>No Recent Activity</h3>
        <p>Activity will appear here as you use the system</p>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

// Cards data - YOU WILL REPLACE WITH REAL DATA
const cards = computed(() => [
  {
    title: 'Total Inventory Items',
    value: inventoryStore.inventory.length || 0,
    icon: 'mdi-pill',
    trend: 'up',
  },
  {
    title: 'Expiring Soon',
    value: 0,
    icon: 'mdi-clock-alert',
    trend: 'warning',
  },
  {
    title: 'Recent Activities',
    value: 0,
    icon: 'mdi-clipboard-list',
    trend: 'up',
  },
  {
    title: 'Inventory Accuracy',
    value: '%',
    icon: 'mdi-check-circle',
    trend: 'up',
  }
])

// Recent activities - YOU WILL REPLACE WITH REAL DATA
const recentActivities = computed(() => {
  return []
})
</script>

<style scoped>
.page-header {
  margin-bottom: 40px;
}

.page-header h2 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 12px;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 1.05rem;
  max-width: 600px;
  line-height: 1.6;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  font-size: 1.6rem;
  color: white;
  background: var(--accent-gradient);
  box-shadow: var(--accent-glow);
}

.card-icon :deep(.v-icon) {
  font-size: 1.6rem;
}

.gradient-card h3 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.gradient-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  font-size: 0.9rem;
}

.card-trend.up {
  color: var(--success-color);
}

.card-trend.warning {
  color: var(--warning-color);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-state h3 {
  font-size: 1.6rem;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.empty-state p {
  max-width: 400px;
  margin: 0 auto;
  line-height: 1.6;
}

:deep(.v-table) {
  background: transparent !important;
}

:deep(.v-table thead th) {
  background: var(--tertiary-dark);
  color: var(--text-secondary) !important;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border-color);
}

:deep(.v-table tbody td) {
  color: var(--text-primary) !important;
  border-bottom: 1px solid var(--border-color);
}

:deep(.v-table tbody tr:hover td) {
  background: rgba(74, 108, 247, 0.05) !important;
}
</style>