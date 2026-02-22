<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mb-8">
          <h1 class="gradient-text text-h3 font-weight-bold mb-2">
            System Logs
          </h1>
          <p class="text-body-1 text-medium-emphasis">
            Complete history of inventory activities
          </p>
        </div>
      </v-col>
    </v-row>

    <!-- Error Banner -->
    <v-row v-if="error" class="mb-4">
      <v-col cols="12">
        <v-alert type="error" variant="tonal" closable @click:close="error = null" density="compact">
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Search logs..."
          variant="outlined"
          density="compact"
          hide-details
          clearable
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="filterType"
          :items="typeOptions"
          label="Filter by type"
          variant="outlined"
          density="compact"
          hide-details
          clearable
        />
      </v-col>
      <v-col cols="12" md="3" class="d-flex align-center justify-end">
        <v-btn
          color="primary"
          variant="tonal"
          prepend-icon="mdi-refresh"
          @click="fetchLogs"
          :loading="loading"
        >
          Refresh
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="gradient-card">
          <v-data-table
            :headers="headers"
            :items="filteredLogs"
            :loading="loading"
            :items-per-page="25"
            class="elevation-0"
          >
            <template v-slot:item.type="{ item }">
              <v-chip
                :color="getTypeColor(item.type)"
                variant="tonal"
                size="small"
                class="font-weight-bold"
              >
                <v-icon start size="14">{{ getTypeIcon(item.type) }}</v-icon>
                {{ item.type.toUpperCase() }}
              </v-chip>
            </template>

            <template v-slot:item.timestamp="{ item }">
              <span class="text-mono text-caption">{{ formatDate(item.timestamp) }}</span>
            </template>

            <template v-slot:item.user="{ item }">
              <span class="font-weight-medium" style="color: #4A6CF7">{{ item.user }}</span>
            </template>

            <template v-slot:no-data>
              <div class="text-center py-8">
                <v-icon size="48" color="disabled" class="mb-2">mdi-clipboard-list</v-icon>
                <h3 class="text-h6 mb-2">No Logs Available</h3>
                <p class="text-body-2 text-medium-emphasis">Logs will appear here as you use the system</p>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:8080'

const api = {
  async get(path) {
    const res = await fetch(`${API_BASE}${path}`)
    if (!res.ok) throw new Error(`Server error: ${res.status}`)
    return res.json()
  }
}

const loading = ref(false)
const error = ref(null)
const logs = ref([])
const search = ref('')
const filterType = ref(null)

const typeOptions = ['add', 'update', 'delete', 'restock']

const headers = [
  { title: 'Timestamp', key: 'timestamp', width: '180px' },
  { title: 'User',      key: 'user',      width: '140px' },
  { title: 'Type',      key: 'type',      width: '120px' },
  { title: 'Location',  key: 'location' },
  { title: 'Details',   key: 'action' },
]

const filteredLogs = computed(() => {
  let result = logs.value

  if (filterType.value) {
    result = result.filter(l => l.type === filterType.value)
  }

  if (search.value) {
    const q = search.value.toLowerCase()
    result = result.filter(l =>
      l.user?.toLowerCase().includes(q) ||
      l.action?.toLowerCase().includes(q) ||
      l.location?.toLowerCase().includes(q)
    )
  }

  return result
})

const getTypeColor = (type) => ({
  add:     'success',
  update:  'primary',
  delete:  'error',
  restock: 'purple',
}[type] ?? 'grey')

const getTypeIcon = (type) => ({
  add:     'mdi-plus',
  update:  'mdi-pencil',
  delete:  'mdi-delete',
  restock: 'mdi-package-down',
}[type] ?? 'mdi-information')

const formatDate = (timestamp) => {
  if (!timestamp) return '—'
  const d = new Date(timestamp)
  return isNaN(d.getTime())
    ? timestamp
    : d.toLocaleString([], {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
}

const fetchLogs = async () => {
  loading.value = true
  error.value = null
  try {
    // Fetch a large batch — adjust amount as your log table grows
    logs.value = await api.get('/api/activity/recent?amount=500')
  } catch (err) {
    error.value = `Failed to load logs: ${err.message}`
  } finally {
    loading.value = false
  }
}

onMounted(fetchLogs)
</script>