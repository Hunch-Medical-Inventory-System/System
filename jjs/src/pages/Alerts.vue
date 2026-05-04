<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mb-8">
          <h1 class="gradient-text text-h3 font-weight-bold mb-2">
            Expired & Warnings
          </h1>
          <p class="text-body-1 text-medium-emphasis">
            Items requiring attention
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

    <v-row>
      <v-col cols="12">
        <v-card class="gradient-card">
          <div class="quick-actions">
            <v-chip
              key="expired"
              :variant="getChipVariant('expired')"
              size="small"
              class="quick-action-chip"
              prepend-icon="mdi-alert-circle"
              @click="toggleFilter('expired')"
            >
              Expired
            </v-chip>
            <v-chip
              key="low-stock"
              :variant="getChipVariant('low-stock')"
              size="small"
              class="quick-action-chip"
              prepend-icon="mdi-package-variant"
              @click="toggleFilter('low-stock')"
            >
              Low Stock
            </v-chip>
            <v-chip
              key="low-stock"
              size="small"
              class="quick-action-chip"
              :variant="getChipVariant('clear-filters')"
              @click="toggleFilter('clear-filters')"
              prepend-icon="mdi-broom"
            >
              Clear Filters
            </v-chip>
          </div>
          <v-data-table
            :headers="headers"
            :items="warningItems"
            :loading="loading"
            hide-default-footer
            class="elevation-0"
          >
            <template v-slot:item.quantity="{ item }">
              <v-chip :color="getQuantityColor(item.quantity)" variant="tonal">
                {{ item.quantity }} units
              </v-chip>
            </template>

            <template v-slot:item.expiration="{ item }">
              {{ item.expiration ?? 'N/A' }}
            </template>

            <template v-slot:item.status="{ item }">
              <v-chip
                :color="getStatusColor(item)"
                variant="tonal"
                size="small"
                class="font-weight-bold"
              >
                {{ getStatusText(item) }}
              </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-btn
                :color="isExpired(item) ? 'error' : 'warning'"
                variant="tonal"
                size="small"
                :loading="actionLoadingId === item.upid"
                @click="handleAction(item)"
              >
                {{ isExpired(item) ? 'Dispose' : 'Use First' }}
              </v-btn>
            </template>

            <template v-slot:no-data>
              <div class="text-center py-8">
                <v-icon size="48" color="success" class="mb-2">mdi-check-circle</v-icon>
                <h3 class="text-h6 mb-2">No Warnings</h3>
                <p class="text-body-2 text-medium-emphasis">All items are in good condition</p>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dispose Confirm Dialog -->
    <v-dialog v-model="disposeDialog" max-width="400">
      <v-card>
        <v-card-title>Confirm Disposal</v-card-title>
        <v-card-text>
          Are you sure you want to dispose of <strong>{{ selectedItem?.name }}</strong>?
          This will remove all {{ selectedItem?.quantity }} units and cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="disposeDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="confirmDispose" :loading="actionLoading">
            Dispose
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Use First Dialog -->
    <v-dialog v-model="useDialog" max-width="400">
      <v-card>
        <v-card-title>Use Item First</v-card-title>
        <v-card-text>
          <v-form ref="useForm">
            <v-text-field
              v-model="selectedItem.name"
              label="Item"
              readonly
              class="mb-4"
            />
            <v-text-field
              v-model="checkoutQuantity"
              label="Quantity"
              type="number"
              :rules="[
                v => !!v || 'Required',
                v => v > 0 || 'Must be positive',
                v => v <= selectedItem.quantity || `Max ${selectedItem.quantity}`
              ]"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="useDialog = false">Cancel</v-btn>
          <v-btn color="warning" @click="confirmUse" :loading="actionLoading">
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = 'http://100.97.185.98:8080'

const api = {
  async get(path) {
    const res = await fetch(`${API_BASE}${path}`)
    if (!res.ok) throw new Error(`Server error: ${res.status}`)
    return res.json()
  },
  async post(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    if (!res.ok) throw new Error(`Server error: ${res.status}`)
    return res.json()
  }
}

const loading = ref(false)
const actionLoading = ref(false)
const actionLoadingId = ref(null)
const error = ref(null)
const allInventory = ref([])
const disposeDialog = ref(false)
const useDialog = ref(false)
const selectedItem = ref({})
const checkoutQuantity = ref(1)
const useForm = ref(null)

const headers = [
  { title: 'UPID',        key: 'upid' },
  { title: 'Name',        key: 'name' },
  { title: 'Location',    key: 'location' },
  { title: 'Quantity',    key: 'quantity' },
  { title: 'Expiry Date', key: 'expiration' },
  { title: 'Status',      key: 'status',  sortable: false },
  { title: 'Action',      key: 'actions', sortable: false }
]

// Only show items that are expired or expiring within 30 days
const warningItems = computed(() => {
  return allInventory.value.filter(item => {
    if (!item.expiration) return false
    const days = daysUntilExpiry(item.expiration)
    if (days > 30) return false

    const hasExpiredFilter = activeFilters.value.has('expired')
    const hasLowStockFilter = activeFilters.value.has('low-stock')

    // No filters active — show everything
    if (!hasExpiredFilter && !hasLowStockFilter) return true

    const isExpiredItem = days < 0
    const isLowStock = item.quantity < 20

    // Both active — must match both
    if (hasExpiredFilter && hasLowStockFilter) {
      return isExpiredItem && isLowStock
    }

    // Only expired active
    if (hasExpiredFilter) return isExpiredItem

    // Only low-stock active
    if (hasLowStockFilter) return isLowStock
  })
})

const daysUntilExpiry = (expiration) => {
  return Math.ceil((new Date(expiration) - new Date()) / (1000 * 60 * 60 * 24))
}

const isExpired = (item) => daysUntilExpiry(item.expiration) < 0

const getStatusText = (item) => {
  const days = daysUntilExpiry(item.expiration)
  if (days < 0)   return 'EXPIRED'
  if (days <= 7)  return 'CRITICAL'
  return 'WARNING'
}

const getStatusColor = (item) => {
  const days = daysUntilExpiry(item.expiration)
  if (days < 0)   return 'error'
  if (days <= 7)  return 'deep-orange'
  return 'warning'
}

const getQuantityColor = (qty) => {
  if (qty < 20) return 'error'
  if (qty < 50) return 'warning'
  return 'success'
}

const handleAction = (item) => {
  selectedItem.value = { ...item }
  if (isExpired(item)) {
    disposeDialog.value = true
  } else {
    checkoutQuantity.value = 1
    useDialog.value = true
  }
}

const confirmDispose = async () => {
  actionLoading.value = true
  try {
    await api.post('/api/inventory/remove', {
      userid: 'admin',
      upid: selectedItem.value.upid,
      location: selectedItem.value.location,
      quantity: selectedItem.value.quantity,
      expiration: selectedItem.value.expiration
    })
    disposeDialog.value = false
    await fetchInventory()
  } catch (err) {
    error.value = `Failed to dispose item: ${err.message}`
  } finally {
    actionLoading.value = false
  }
}

const confirmUse = async () => {
  const { valid } = await useForm.value.validate()
  if (!valid) return

  actionLoading.value = true
  try {
    await api.post('/api/inventory/remove', {
      userid: 'admin',
      upid: selectedItem.value.upid,
      location: selectedItem.value.location,
      quantity: parseInt(checkoutQuantity.value),
      expiration: selectedItem.value.expiration
    })
    useDialog.value = false
    await fetchInventory()
  } catch (err) {
    error.value = `Failed to check out item: ${err.message}`
  } finally {
    actionLoading.value = false
  }
}

const fetchInventory = async () => {
  loading.value = true
  try {
    allInventory.value = await api.get('/api/inventory?amount=1000&offset=0')
  } catch (err) {
    error.value = `Failed to load inventory: ${err.message}`
  } finally {
    loading.value = false
  }
}

const activeFilters = ref(new Set())

const toggleFilter = (filter) => {
  if (filter === 'clear-filters') {
    activeFilters.value.clear()
    activeFilters.value = new Set() // trigger reactivity
    return
  }
  if (activeFilters.value.has(filter)) {
    activeFilters.value.delete(filter)
  } else {
    activeFilters.value.add(filter)
  }
  activeFilters.value = new Set(activeFilters.value) // trigger reactivity
  if (activeFilters.value.size > 0) {
    activeFilters.value.add('clear-filters')
  }
  if (activeFilters.value.size === 1 && activeFilters.value.has('clear-filters')) {
    activeFilters.value.delete('clear-filters')
  }
}

const getChipVariant = (filter) => {
  return activeFilters.value.has(filter) ? 'outlined' : 'elevated'
}

onMounted(fetchInventory)
</script>

<style scoped>
.quick-actions {
  display: flex;
  gap: 6px;
  margin: 0.75rem;
  margin-left: 0;
  flex-wrap: wrap;
}

.quick-action-chip {
  border: 1px solid var(--border-color) !important;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8rem;
  height: 28px;
}

.quick-action-chip:hover { 
  transform: translateY(-1px); 
  background: var(--tertiary-dark) !important;
}
</style>