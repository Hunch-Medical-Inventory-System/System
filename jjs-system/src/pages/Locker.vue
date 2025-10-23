<!-- pages/Locker.vue -->
<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>In-Locker Inventory</v-card-title>
              <v-card-subtitle>All medical supplies currently in the locker</v-card-subtitle>
            </v-card-item>
            
            <v-card-text>
              <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                label="Search items..."
                single-line
                hide-details
                variant="outlined"
                class="mb-4"
              />

              <v-data-table
                :headers="headers"
                :items="inventoryStore.inventory"
                :search="search"
                :loading="inventoryStore.loading"
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
                    icon
                    size="small"
                    color="primary"
                    @click="checkOutItem(item)"
                  >
                    <v-icon>mdi-cart-arrow-down</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    size="small"
                    color="error"
                    @click="deleteItem(item)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>

                <template v-slot:no-data>
                  <div class="text-center py-8">
                    <v-icon size="64" color="grey-lighten-1">mdi-package-variant</v-icon>
                    <h3 class="text-h6 mt-4">No Items in Locker</h3>
                    <p class="text-grey">Add items to your inventory to get started</p>
                    <v-btn color="primary" class="mt-4" @click="showAddItemDialog = true">
                      <v-icon start>mdi-plus</v-icon>
                      Add First Item
                    </v-btn>
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Check Out Dialog -->
    <v-dialog v-model="checkOutDialog" max-width="500">
      <v-card>
        <v-card-title>Check Out Medication</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="selectedItem.name"
            label="Medication"
            readonly
            class="mb-4"
          />
          <v-text-field
            v-model="checkOutQuantity"
            label="Quantity"
            type="number"
            :max="selectedItem.quantity"
            min="1"
            class="mb-4"
          />
          <v-text-field
            v-model="purpose"
            label="Purpose"
            placeholder="Enter purpose for this medication"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="checkOutDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="confirmCheckOut">Confirm Check Out</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Add Item Dialog -->
    <v-dialog v-model="showAddItemDialog" max-width="600">
      <v-card>
        <v-card-title>Add New Item</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newItem.name"
                label="Item Name"
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newItem.category"
                label="Category"
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newItem.quantity"
                label="Quantity"
                type="number"
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newItem.expiryDate"
                label="Expiry Date"
                type="date"
                required
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="newItem.location"
                label="Location"
                placeholder="e.g., A1, B2"
              />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showAddItemDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addNewItem">Add Item</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

const search = ref('')
const checkOutDialog = ref(false)
const showAddItemDialog = ref(false)
const selectedItem = ref({})
const checkOutQuantity = ref(1)
const purpose = ref('')

const newItem = ref({
  name: '',
  category: '',
  quantity: 1,
  expiryDate: '',
  location: ''
})

const headers = [
  { title: 'Item ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'Category', key: 'category' },
  { title: 'Quantity', key: 'quantity' },
  { title: 'Expiry Date', key: 'expiryDate' },
  { title: 'Status', key: 'status' },
  { title: 'Actions', key: 'actions', sortable: false }
]

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
  return { class: 'success', text: 'OK' }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const checkOutItem = (item) => {
  selectedItem.value = { ...item }
  checkOutQuantity.value = 1
  purpose.value = ''
  checkOutDialog.value = true
}

const confirmCheckOut = async () => {
  const success = await inventoryStore.checkOutItem(
    selectedItem.value.id,
    checkOutQuantity.value,
    purpose.value
  )
  
  if (success) {
    checkOutDialog.value = false
    await inventoryStore.fetchInventory()
  }
}

const deleteItem = async (item) => {
  if (confirm(`Are you sure you want to delete ${item.name}?`)) {
    await inventoryStore.deleteItem(item.id)
    await inventoryStore.fetchInventory()
  }
}

const addNewItem = async () => {
  await inventoryStore.addItem(newItem.value)
  showAddItemDialog.value = false
  // Reset form
  newItem.value = {
    name: '',
    category: '',
    quantity: 1,
    expiryDate: '',
    location: ''
  }
}

onMounted(async () => {
  await inventoryStore.fetchInventory()
})
</script>