<!-- pages/Scanner.vue -->
<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>NFC Scanner</v-card-title>
              <v-card-subtitle>Scan medicine NFC tags to check out items</v-card-subtitle>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card class="scanner-card">
            <v-card-text class="text-center pa-8">
              <v-icon 
                size="80" 
                :color="scannerStatus.color"
                class="mb-4"
              >
                {{ scannerStatus.icon }}
              </v-icon>
              
              <h3 class="text-h5 mb-2">{{ scannerStatus.title }}</h3>
              <p class="text-grey mb-6">{{ scannerStatus.message }}</p>

              <v-btn
                color="primary"
                size="large"
                :loading="scanning"
                :disabled="!nfcSupported"
                @click="startScan"
              >
                <v-icon start>{{ scannerStatus.buttonIcon }}</v-icon>
                {{ scannerStatus.buttonText }}
              </v-btn>

              <v-alert
                v-if="!nfcSupported"
                type="warning"
                class="mt-6"
              >
                <v-alert-title>NFC Not Supported</v-alert-title>
                Your device or browser does not support NFC scanning.
              </v-alert>

              <div v-else class="mt-6">
                <v-chip variant="outlined" color="info">
                  <v-icon start>mdi-information</v-icon>
                  This feature requires an NFC-enabled device and browser permission
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- NFC Scan Result Dialog -->
    <v-dialog v-model="scanResultDialog" max-width="500">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>Check Out Medication</span>
          <v-btn icon @click="scanResultDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <v-text-field
            v-model="scannedItem.name"
            label="Medication"
            readonly
            class="mb-4"
          />
          <v-text-field
            v-model="checkOutQuantity"
            label="Quantity to Check Out"
            type="number"
            :max="scannedItem.quantity"
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
          <v-btn @click="scanResultDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="confirmCheckOut">Confirm Check Out</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Add New Item Dialog -->
    <v-dialog v-model="addItemDialog" max-width="600">
      <v-card>
        <v-card-title>Add New Medication</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newItem.name"
                label="Medication Name"
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
          <v-btn @click="addItemDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addNewItem">Add to Inventory</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

const nfcSupported = ref('NDEFReader' in window)
const scanning = ref(false)
const scanResultDialog = ref(false)
const addItemDialog = ref(false)
const scannedItem = ref({})
const nfcData = ref('')
const checkOutQuantity = ref(1)
const purpose = ref('')

const newItem = ref({
  name: '',
  category: '',
  quantity: 1,
  expiryDate: '',
  location: ''
})

const scannerStatus = computed(() => {
  if (!nfcSupported.value) {
    return {
      icon: 'mdi-nfc-off',
      color: 'error',
      title: 'NFC Not Supported',
      message: 'Your device or browser does not support NFC scanning.',
      buttonIcon: 'mdi-nfc-off',
      buttonText: 'NFC Not Available'
    }
  }

  if (scanning.value) {
    return {
      icon: 'mdi-nfc-search',
      color: 'warning',
      title: 'Scanning for NFC Tags',
      message: 'Place the medicine near your device now',
      buttonIcon: 'mdi-loading',
      buttonText: 'Scanning...'
    }
  }

  return {
    icon: 'mdi-nfc',
    color: 'primary',
    title: 'NFC Scanner Ready',
    message: 'Click "Start NFC Scan" and place the medicine near your device',
    buttonIcon: 'mdi-nfc',
    buttonText: 'Start NFC Scan'
  }
})

let nfcReader = null

const startScan = async () => {
  if (!nfcSupported.value) return

  try {
    scanning.value = true
    nfcReader = new NDEFReader()
    
    await nfcReader.scan()
    
    nfcReader.onreading = (event) => {
      const decoder = new TextDecoder()
      for (const record of event.message.records) {
        if (record.recordType === "text") {
          const text = decoder.decode(record.data)
          handleNFCScan(text)
        }
      }
    }
    
    nfcReader.onreadingerror = () => {
      scanning.value = false
      // Handle error
    }
    
  } catch (error) {
    console.error("Error starting NFC scan:", error)
    scanning.value = false
  }
}

const handleNFCScan = (data) => {
  scanning.value = false
  nfcData.value = data
  
  // Try to find the medication in inventory
  const foundItem = inventoryStore.inventory.find(item => 
    item.id.toLowerCase().includes(data.toLowerCase()) || 
    item.name.toLowerCase().includes(data.toLowerCase())
  )
  
  if (foundItem) {
    scannedItem.value = { ...foundItem }
    checkOutQuantity.value = 1
    purpose.value = ''
    scanResultDialog.value = true
  } else {
    // Item not found, offer to add it
    newItem.value.name = data
    addItemDialog.value = true
  }
}

const confirmCheckOut = async () => {
  const success = await inventoryStore.checkOutItem(
    scannedItem.value.id,
    checkOutQuantity.value,
    purpose.value
  )
  
  if (success) {
    scanResultDialog.value = false
    await inventoryStore.fetchInventory()
  }
}

const addNewItem = async () => {
  await inventoryStore.addItem(newItem.value)
  addItemDialog.value = false
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

<style scoped>
.scanner-card {
  border-radius: 12px;
}
</style>