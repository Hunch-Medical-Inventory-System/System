<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mb-8">
          <h1 class="gradient-text text-h3 font-weight-bold mb-2">
            Inventory Management
          </h1>
          <p class="text-body-1 text-medium-emphasis">
            All medical supplies currently in stock and their status
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
          <v-data-table
            :headers="headers"
            :items="inventory"
            :loading="loading"
            :search="search"
            :items-per-page="25"
            class="elevation-0"
          >
            <template v-slot:top>
              <v-toolbar flat color="transparent">
                <v-text-field
                  v-model="search"
                  prepend-inner-icon="mdi-magnify"
                  label="Search inventory..."
                  variant="outlined"
                  density="compact"
                  hide-details
                  clearable
                  class="mr-4"
                />
                <v-spacer />
                <v-btn
                  color="primary"
                  prepend-icon="mdi-plus"
                  @click="openAddDialog"
                >
                  Add Item
                </v-btn>
              </v-toolbar>
            </template>

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
                icon
                size="small"
                color="primary"
                class="mr-2"
                @click="openCheckoutDialog(item)"
              >
                <v-icon>mdi-cart-arrow-down</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                color="warning"
                @click="openEditDialog(item)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>

            <template v-slot:no-data>
              <div class="text-center py-8">
                <v-icon size="48" color="disabled" class="mb-2">mdi-cube</v-icon>
                <h3 class="text-h6 mb-2">No Items in Inventory</h3>
                <p class="text-body-2 text-medium-emphasis">Add items to get started</p>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add / Edit Dialog -->
    <v-dialog v-model="addItemDialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingItem ? 'Edit Item' : 'Add New Item' }}</v-card-title>
        <v-card-text>
          <v-form ref="itemForm">
            <v-text-field
              v-model="newItem.name"
              label="Item Name"
              :rules="[v => !!v || 'Name is required']"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.upid"
              label="UPID (Unique Product ID)"
              :rules="[v => !!v || 'UPID is required']"
              :readonly="editingItem"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.location"
              label="Storage Location"
              :rules="[v => !!v || 'Location is required']"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.quantity"
              label="Quantity"
              type="number"
              :rules="[
                v => !!v || 'Quantity is required',
                v => v > 0 || 'Must be positive'
              ]"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.expiration"
              label="Expiry Date"
              type="date"
              :rules="[v => !!v || 'Expiry date is required']"
              class="mb-4"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="addItemDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveItem" :loading="saving">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Checkout Dialog -->
    <v-dialog v-model="useItemDialog" max-width="400">
      <v-card>
        <v-card-title>Check Out Item</v-card-title>
        <v-card-text>
          <v-form ref="useItemForm">
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
                v => !!v || 'Quantity is required',
                v => v > 0 || 'Must be positive',
                v => v <= selectedItem.quantity || `Max ${selectedItem.quantity} available`
              ]"
              class="mb-4"
            />
            <v-text-field
              v-model="checkoutPurpose"
              label="Purpose / Notes"
              class="mb-4"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="useItemDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="confirmCheckout" :loading="checkingOut">
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:8080'

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

// --------------------------------------------------
// State
// --------------------------------------------------

const loading    = ref(false)
const saving     = ref(false)
const checkingOut = ref(false)
const error      = ref(null)
const search     = ref('')

const inventory     = ref([])
const addItemDialog = ref(false)
const useItemDialog = ref(false)
const editingItem   = ref(false)

const itemForm    = ref(null)
const useItemForm = ref(null)

const newItem = ref({
  name: '', upid: '', location: '', quantity: 1, expiration: ''
})

const selectedItem      = ref({})
const checkoutQuantity  = ref(1)
const checkoutPurpose   = ref('')

// --------------------------------------------------
// Table headers — match keys returned by /api/inventory
// --------------------------------------------------

const headers = [
  { title: 'UPID',        key: 'upid' },
  { title: 'Name',        key: 'name' },
  { title: 'Location',    key: 'location' },
  { title: 'Quantity',    key: 'quantity' },
  { title: 'Expiry Date', key: 'expiration' },
  { title: 'Status',      key: 'status',  sortable: false },
  { title: 'Actions',     key: 'actions', sortable: false }
]

// --------------------------------------------------
// Helpers
// --------------------------------------------------

const daysUntilExpiry = (expiration) =>
  Math.ceil((new Date(expiration) - new Date()) / (1000 * 60 * 60 * 24))

const getStatusText = (item) => {
  if (!item.expiration) return 'N/A'
  const days = daysUntilExpiry(item.expiration)
  if (days < 0)   return 'EXPIRED'
  if (days <= 7)  return 'CRITICAL'
  if (days <= 30) return 'WARNING'
  return 'OK'
}

const getStatusColor = (item) => {
  if (!item.expiration) return 'grey'
  const days = daysUntilExpiry(item.expiration)
  if (days < 0)   return 'error'
  if (days <= 7)  return 'deep-orange'
  if (days <= 30) return 'warning'
  return 'success'
}

const getQuantityColor = (qty) => {
  if (qty < 20) return 'error'
  if (qty < 50) return 'warning'
  return 'success'
}

// --------------------------------------------------
// Dialog Openers
// --------------------------------------------------

const openAddDialog = () => {
  editingItem.value = false
  newItem.value = { name: '', upid: '', location: '', quantity: 1, expiration: '' }
  addItemDialog.value = true
}

const openEditDialog = (item) => {
  editingItem.value = true
  newItem.value = {
    name:       item.name,
    upid:       item.upid,
    location:   item.location,
    quantity:   item.quantity,
    expiration: item.expiration ?? ''
  }
  addItemDialog.value = true
}

const openCheckoutDialog = (item) => {
  selectedItem.value    = { ...item }
  checkoutQuantity.value = 1
  checkoutPurpose.value  = ''
  useItemDialog.value    = true
}

// --------------------------------------------------
// Actions
// --------------------------------------------------

const saveItem = async () => {
  const { valid } = await itemForm.value.validate()
  if (!valid) return

  saving.value = true
  error.value  = null
  try {
    await api.post('/api/inventory/add', {
      userid:     'admin',
      upid:       newItem.value.upid,
      location:   newItem.value.location,
      quantity:   parseInt(newItem.value.quantity),
      expiration: newItem.value.expiration,
      name:       newItem.value.name
    })
    addItemDialog.value = false
    await fetchInventory()
  } catch (err) {
    error.value = `Failed to save item: ${err.message}`
  } finally {
    saving.value = false
  }
}

const confirmCheckout = async () => {
  const { valid } = await useItemForm.value.validate()
  if (!valid) return

  checkingOut.value = true
  error.value       = null
  try {
    await api.post('/api/inventory/remove', {
      userid:     'admin',
      upid:       selectedItem.value.upid,
      location:   selectedItem.value.location,
      quantity:   parseInt(checkoutQuantity.value),
      expiration: selectedItem.value.expiration
    })
    useItemDialog.value = false
    await fetchInventory()
  } catch (err) {
    error.value = `Failed to check out item: ${err.message}`
  } finally {
    checkingOut.value = false
  }
}

const fetchInventory = async () => {
  loading.value = true
  error.value   = null
  try {
    inventory.value = await api.get('/api/inventory?amount=1000&offset=0')
  } catch (err) {
    error.value = `Failed to load inventory: ${err.message}`
  } finally {
    loading.value = false
  }
}

onMounted(fetchInventory)
</script>