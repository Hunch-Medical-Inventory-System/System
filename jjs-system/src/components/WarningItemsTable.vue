<!-- components/WarningItemsTable.vue -->
<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :loading="loading"
    >
      <template v-slot:item.quantity="{ item }">
        <v-chip :color="getQuantityColor(item.quantity)" variant="flat">
          {{ item.quantity }}
        </v-chip>
      </template>

      <template v-slot:item.expiryDate="{ item }">
        <span :class="getExpiryClass(item.expiryDate)">
          {{ formatDate(item.expiryDate) }}
        </span>
      </template>

      <template v-slot:item.status="{ item }">
        <v-chip :class="getStatusClass(item)" variant="flat" size="small">
          {{ getStatusText(item) }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-btn
          v-if="warningType === 'expired'"
          color="error"
          size="small"
          @click="$emit('dispose', item)"
        >
          <v-icon start>mdi-delete</v-icon>
          Dispose
        </v-btn>
        <v-btn
          v-else
          color="primary"
          size="small"
          @click="$emit('use', item)"
        >
          <v-icon start>mdi-cart-arrow-down</v-icon>
          Use First
        </v-btn>
      </template>

      <template v-slot:no-data>
        <div class="text-center py-8">
          <v-icon size="64" color="success">mdi-check-circle</v-icon>
          <h3 class="text-h6 mt-4">No Warnings</h3>
          <p class="text-grey">All items are in good condition</p>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  warningType: {
    type: String,
    default: 'expired'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['dispose', 'use'])

const headers = computed(() => [
  { title: 'Item ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'Location', key: 'location' },
  { title: 'Quantity', key: 'quantity' },
  { title: 'Expiry Date', key: 'expiryDate' },
  { title: 'Status', key: 'status' },
  { title: 'Action', key: 'actions', sortable: false }
])

const getQuantityColor = (quantity) => {
  if (quantity < 10) return 'error'
  if (quantity < 25) return 'warning'
  return 'success'
}

const getExpiryClass = (expiryDate) => {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const daysUntilExpiry = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) return 'text-error'
  if (daysUntilExpiry <= 30) return 'text-warning'
  return 'text-success'
}

const getStatusClass = (item) => {
  const status = getItemStatus(item)
  return `bg-${status.class}`
}

const getStatusText = (item) => {
  const status = getItemStatus(item)
  return status.text
}

const getItemStatus = (item) => {
  const today = new Date()
  const expiryDate = new Date(item.expiryDate)
  const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) return { class: 'error', text: 'Expired' }
  if (daysUntilExpiry <= 30) return { class: 'warning', text: 'Expiring Soon' }
  if (item.quantity < 10) return { class: 'warning', text: 'Low Stock' }
  return { class: 'success', text: 'OK' }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}
</script>