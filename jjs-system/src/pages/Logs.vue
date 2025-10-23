<!-- pages/Logs.vue -->
<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>System Logs</v-card-title>
              <v-card-subtitle>Complete history of inventory activities</v-card-subtitle>
            </v-card-item>
            
            <v-card-text>
              <v-row class="mb-4">
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="search"
                    prepend-inner-icon="mdi-magnify"
                    label="Search logs..."
                    variant="outlined"
                    hide-details
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="actionFilter"
                    :items="actionTypes"
                    label="Filter by Action"
                    variant="outlined"
                    hide-details
                    clearable
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="userFilter"
                    :items="users"
                    label="Filter by User"
                    variant="outlined"
                    hide-details
                    clearable
                  />
                </v-col>
              </v-row>

              <v-data-table
                :headers="headers"
                :items="filteredLogs"
                :loading="inventoryStore.loading"
              >
                <template v-slot:item.timestamp="{ item }">
                  <span class="text-caption">{{ item.timestamp }}</span>
                </template>

                <template v-slot:item.action="{ item }">
                  <v-chip :color="getActionColor(item.action)" variant="flat" size="small">
                    {{ item.action }}
                  </v-chip>
                </template>

                <template v-slot:item.details="{ item }">
                  <span class="text-caption">{{ item.details }}</span>
                </template>

                <template v-slot:no-data>
                  <div class="text-center py-8">
                    <v-icon size="64" color="grey-lighten-1">mdi-clipboard-list</v-icon>
                    <h3 class="text-h6 mt-4">No Logs Available</h3>
                    <p class="text-grey">Logs will appear here as you use the system</p>
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

const search = ref('')
const actionFilter = ref(null)
const userFilter = ref(null)

const headers = [
  { title: 'Timestamp', key: 'timestamp', width: '180px' },
  { title: 'User', key: 'user', width: '120px' },
  { title: 'Action', key: 'action', width: '130px' },
  { title: 'Item', key: 'item', width: '150px' },
  { title: 'Details', key: 'details' }
]

const actionTypes = [
  'Login',
  'Logout',
  'Check Out',
  'Add',
  'Update',
  'Delete',
  'Dispose'
]

const users = computed(() => {
  const uniqueUsers = new Set(inventoryStore.logs.map(log => log.user))
  return Array.from(uniqueUsers)
})

const filteredLogs = computed(() => {
  let logs = inventoryStore.logs

  if (search.value) {
    const searchLower = search.value.toLowerCase()
    logs = logs.filter(log => 
      log.user.toLowerCase().includes(searchLower) ||
      log.action.toLowerCase().includes(searchLower) ||
      (log.item && log.item.toLowerCase().includes(searchLower)) ||
      log.details.toLowerCase().includes(searchLower)
    )
  }

  if (actionFilter.value) {
    logs = logs.filter(log => log.action === actionFilter.value)
  }

  if (userFilter.value) {
    logs = logs.filter(log => log.user === userFilter.value)
  }

  return logs.reverse() // Show latest first
})

const getActionColor = (action) => {
  const colors = {
    'Login': 'success',
    'Logout': 'grey',
    'Check Out': 'primary',
    'Add': 'info',
    'Update': 'warning',
    'Delete': 'error',
    'Dispose': 'error'
  }
  return colors[action] || 'grey'
}

onMounted(async () => {
  await inventoryStore.fetchLogs()
})
</script>