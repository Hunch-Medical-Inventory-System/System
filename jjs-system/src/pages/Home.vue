<!-- pages/Home.vue -->
<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>Dashboard</v-card-title>
              <v-card-subtitle>
                Welcome to JJs V2.0 Medical Inventory System
              </v-card-subtitle>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="4">
          <v-card color="primary" theme="dark">
            <v-card-item>
              <div class="d-flex align-center">
                <v-icon class="mr-3" size="48">mdi-package-variant</v-icon>
                <div>
                  <v-card-title class="text-h4">{{ stats.totalItems }}</v-card-title>
                  <v-card-subtitle>Items in Locker</v-card-subtitle>
                </div>
              </div>
            </v-card-item>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card color="warning" theme="dark">
            <v-card-item>
              <div class="d-flex align-center">
                <v-icon class="mr-3" size="48">mdi-alert</v-icon>
                <div>
                  <v-card-title class="text-h4">{{ stats.expiringItems }}</v-card-title>
                  <v-card-subtitle>Expiring Soon</v-card-subtitle>
                </div>
              </div>
            </v-card-item>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card color="info" theme="dark">
            <v-card-item>
              <div class="d-flex align-center">
                <v-icon class="mr-3" size="48">mdi-history</v-icon>
                <div>
                  <v-card-title class="text-h4">{{ stats.recentActivities }}</v-card-title>
                  <v-card-subtitle>Recent Activities</v-card-subtitle>
                </div>
              </div>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>Recent Activity</v-card-title>
            </v-card-item>
            <v-card-text>
              <v-table v-if="recentActivities.length > 0">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Action</th>
                    <th>User</th>
                    <th>Date & Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="activity in recentActivities" :key="activity.id">
                    <td>{{ activity.item || 'N/A' }}</td>
                    <td>{{ activity.action }}</td>
                    <td>{{ activity.user }}</td>
                    <td>{{ activity.timestamp }}</td>
                  </tr>
                </tbody>
              </v-table>
              <div v-else class="text-center py-8">
                <v-icon size="64" color="grey-lighten-1">mdi-clipboard-list</v-icon>
                <h3 class="text-h6 mt-4">No Recent Activity</h3>
                <p class="text-grey">Activity will appear here as you use the system</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

const stats = ref({
  totalItems: 0,
  expiringItems: 0,
  recentActivities: 0
})

const recentActivities = ref([])

const loadDashboardData = async () => {
  await inventoryStore.fetchInventory()
  await inventoryStore.fetchLogs()
  
  stats.value.totalItems = inventoryStore.totalItems
  stats.value.expiringItems = inventoryStore.expiringItems.length
  stats.value.recentActivities = inventoryStore.recentLogs.length
  recentActivities.value = inventoryStore.recentLogs
}

onMounted(() => {
  loadDashboardData()
})
</script>