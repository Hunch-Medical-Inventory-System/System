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

    <v-row>
      <v-col cols="12">
        <v-card class="gradient-card">
          <v-data-table
            :headers="headers"
            :items="inventory"
            :loading="loading"
            :search="search"
            hide-default-footer
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
                  class="mr-4"
                />
                <v-spacer />
                <v-btn
                  color="primary"
                  prepend-icon="mdi-plus"
                  @click="addItemDialog = true"
                >
                  Add Item
                </v-btn>
              </v-toolbar>
            </template>

            <template v-slot:item.quantity="{ item }">
              <v-chip
                :color="getQuantityColor(item.quantity)"
                variant="tonal"
              >
                {{ item.quantity }} units
              </v-chip>
            </template>

            <template v-slot:item.status="{ item }">
              <v-chip
                :class="getStatusClass(item)"
                size="small"
                class="status-badge font-weight-bold"
              >
                {{ getStatusText(item) }}
              </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                size="small"
                color="primary"
                @click="useItem(item)"
                class="mr-2"
              >
                <v-icon>mdi-cart-arrow-down</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                color="warning"
                @click="editItem(item)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>

            <template v-slot:no-data>
              <v-alert
                type="info"
                variant="tonal"
                class="ma-4"
              >
                <div class="text-center py-4">
                  <v-icon size="48" class="mb-2">mdi-cube</v-icon>
                  <h3 class="text-h6 mb-2">No Items in Inventory</h3>
                  <p class="text-body-2">Add items to your inventory to get started</p>
                </div>
              </v-alert>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add/Edit Item Dialog -->
    <v-dialog v-model="addItemDialog" max-width="500">
      <v-card>
        <v-card-title>
          {{ editingItem ? 'Edit Item' : 'Add New Item' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="itemForm">
            <v-text-field
              v-model="newItem.name"
              label="Item Name"
              :rules="[v => !!v || 'Name is required']"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.category"
              label="Category"
              :rules="[v => !!v || 'Category is required']"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.quantity"
              label="Quantity"
              type="number"
              :rules="[
                v => !!v || 'Quantity is required',
                v => v > 0 || 'Quantity must be positive'
              ]"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.expiryDate"
              label="Expiry Date"
              type="date"
              :rules="[v => !!v || 'Expiry date is required']"
              class="mb-4"
            />
            <v-text-field
              v-model="newItem.location"
              label="Storage Location"
              class="mb-4"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="addItemDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="saveItem"
            :loading="saving"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Use Item Dialog -->
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
                v => v > 0 || 'Quantity must be positive',
                v => v <= selectedItem.quantity || `Max ${selectedItem.quantity} available`
              ]"
              class="mb-4"
            />
            <v-text-field
              v-model="checkoutPurpose"
              label="Purpose/Notes"
              class="mb-4"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="useItemDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="confirmCheckout"
            :loading="checkingOut"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/main'

const inventoryStore = useInventoryStore()
const loading = ref(false)
const search = ref('')
const addItemDialog = ref(false)
const useItemDialog = ref(false)
const saving = ref(false)
const checkingOut = ref(false)
const editingItem = ref(false)
const itemForm = ref(null)
const useItemForm = ref(null)

const newItem = ref({
  name: '',
  category: '',
  quantity: 0,
  expiryDate: '',
  location: ''
})

const selectedItem = ref({})
const checkoutQuantity = ref(1)
const checkoutPurpose = ref('')

const inventory = computed(() => inventoryStore.inventory)

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
  if (quantity < 20) return 'error'
  if (quantity < 50) return 'warning'
  return 'success'
}

const getStatusClass = (item) => {
  const expiryDate = new Date(item.expiryDate)
  const today = new Date()
  const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) return 'expired'
  if (daysUntilExpiry <= 7) return 'warning'
  if (daysUntilExpiry <= 30) return 'warning'
  return 'ok'
}

const getStatusText = (item) => {
  const expiryDate = new Date(item.expiryDate)
  const today = new Date()
  const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) return 'EXPIRED'
  if (daysUntilExpiry <= 7) return 'CRITICAL'
  if (daysUntilExpiry <= 30) return 'WARNING'
  return 'OK'
}

const useItem = (item) => {
  selectedItem.value = { ...item }
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
  useItemDialog.value = true
}

const editItem = (item) => {
  newItem.value = { ...item }
  editingItem.value = true
  addItemDialog.value = true
}

const saveItem = async () => {
  const { valid } = await itemForm.value.validate()
  if (!valid) return

  saving.value = true
  // API call to save item
  saving.value = false
  addItemDialog.value = false
  resetForm()
}

const confirmCheckout = async () => {
  const { valid } = await useItemForm.value.validate()
  if (!valid) return

  checkingOut.value = true
  const success = await inventoryStore.checkOutItem(
    selectedItem.value.id,
    checkoutQuantity.value,
    checkoutPurpose.value
  )
  
  if (success) {
    useItemDialog.value = false
  }
  checkingOut.value = false
}

const resetForm = () => {
  newItem.value = {
    name: '',
    category: '',
    quantity: 0,
    expiryDate: '',
    location: ''
  }
  editingItem.value = false
}

onMounted(async () => {
  loading.value = true
  await inventoryStore.fetchInventory()
  loading.value = false
})
</script>