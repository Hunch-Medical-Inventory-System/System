<template>
  <v-container fluid class="px-4 px-sm-6">
    <!-- Header Section -->
    <v-row class="mb-6 mb-md-8">
      <v-col cols="12">
        <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between">
          <div>
            <h1 class="text-h4 text-sm-h3 font-weight-bold mb-1">
              <span class="gradient-text">NFC Scanner</span>
            </h1>
            <p class="text-body-2 text-medium-emphasis">
              Scan NFC tags to check out medications
            </p>
          </div>
          
          <!-- Quick Stats -->
          <v-chip-group class="mt-3 mt-sm-0">
            <v-chip color="primary" variant="flat" size="small">
              <v-icon start size="18">mdi-nfc</v-icon>
              Scanner Ready
            </v-chip>
            <v-chip color="success" variant="flat" size="small">
              <v-icon start size="18">mdi-check-circle</v-icon>
              {{ scansToday }} Today
            </v-chip>
          </v-chip-group>
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

    <!-- Main Scanner Card -->
    <v-row>
      <v-col cols="12" lg="8" xl="6" class="mx-auto">
        <v-card class="scanner-card" elevation="0">
          <!-- Scanner Header -->
          <v-card-item>
            <div class="d-flex align-center">
              <v-avatar color="primary" variant="tonal" size="40" class="mr-3">
                <v-icon color="primary">mdi-nfc</v-icon>
              </v-avatar>
              <div>
                <v-card-title class="text-h6 font-weight-bold pa-0">
                  NFC Scanner Interface
                </v-card-title>
                <v-card-subtitle class="pa-0 text-caption">
                  {{ scannerStatus }}
                </v-card-subtitle>
              </div>
            </div>
          </v-card-item>

          <v-divider></v-divider>

          <!-- Scanner Body -->
          <v-card-text class="text-center py-6 py-md-8">
            <!-- Scanner Animation -->
            <div class="scanner-container mb-6">
              <div class="scanner-ring" :class="{ 'scanning-active': isScanning }">
                <div class="scanner-inner">
                  <v-icon 
                    :size="isScanning ? 56 : 48" 
                    :color="isScanning ? 'primary' : 'grey'"
                    class="scanner-icon"
                    :class="{ 'pulse': isScanning }"
                  >
                    mdi-nfc
                  </v-icon>
                </div>
              </div>
            </div>

            <!-- Status Messages -->
            <div class="mb-6">
              <div class="text-h6 font-weight-medium mb-2">
                {{ scannerMessage }}
              </div>
              <div class="text-caption text-medium-emphasis">
                {{ scannerFeedback }}
              </div>
            </div>

            <!-- Progress Bar -->
            <v-expand-transition>
              <div v-if="isScanning" class="mb-6">
                <v-progress-linear
                  v-model="scanProgress"
                  color="primary"
                  height="6"
                  rounded
                  striped
                >
                  <template v-slot:default>
                    <span class="text-caption font-weight-bold">
                      {{ Math.round(scanProgress) }}%
                    </span>
                  </template>
                </v-progress-linear>
              </div>
            </v-expand-transition>

            <!-- Action Button -->
            <v-btn
              :color="isScanning ? 'error' : 'primary'"
              size="x-large"
              block
              :prepend-icon="isScanning ? 'mdi-stop-circle' : 'mdi-play-circle'"
              @click="toggleScan"
              :loading="loading"
              class="mb-4"
              height="56"
            >
              {{ isScanning ? 'Stop Scanning' : 'Start Scanning' }}
            </v-btn>

            <!-- Manual Entry Option -->
            <div class="text-center">
              <v-btn
                variant="text"
                color="primary"
                size="small"
                prepend-icon="mdi-pencil"
                @click="openManualEntry"
                :disabled="isScanning"
              >
                Manual Entry
              </v-btn>
            </div>

            <!-- Scanner Info -->
            <div class="d-flex flex-wrap justify-center gap-4 mt-4">
              <div class="d-flex align-center">
                <v-icon size="small" color="grey" class="mr-1">mdi-clock-outline</v-icon>
                <span class="text-caption">Last scan: {{ lastScanTime || 'Never' }}</span>
              </div>
              <div class="d-flex align-center">
                <v-icon size="small" color="grey" class="mr-1">mdi-wifi</v-icon>
                <span class="text-caption">Connected</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Scan Result Dialog -->
    <v-dialog v-model="scanResultDialog" max-width="500" persistent>
      <v-card class="dialog-card">
        <v-card-item class="bg-primary-light">
          <div class="d-flex align-center">
            <v-avatar color="primary" size="40" class="mr-3">
              <v-icon color="white">mdi-pill</v-icon>
            </v-avatar>
            <div>
              <v-card-title class="text-h6 pa-0">
                {{ isManualEntry ? 'Manual Checkout' : 'Medication Found' }}
              </v-card-title>
              <v-card-subtitle class="pa-0 text-caption">
                {{ isManualEntry ? 'Select medication to check out' : 'Enter checkout details' }}
              </v-card-subtitle>
            </div>
          </div>
        </v-card-item>

        <v-card-text class="pt-4">
          <v-form ref="checkoutForm" @submit.prevent="confirmScanCheckout">
            <!-- Medication Dropdown - Real database items -->
            <v-autocomplete
              v-model="selectedItem"
              :items="inventory"
              label="Select Medication"
              placeholder="Search by name or UPID"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              :rules="[v => !!v || 'Medication is required']"
              clearable
              return-object
              item-title="name"
              item-value="upid"
              :disabled="!isManualEntry && selectedItem"
              :loading="loading"
            >
              <template v-slot:prepend-inner>
                <v-icon size="small" color="primary">mdi-pill</v-icon>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :title="item.raw.name">
                  <template v-slot:subtitle>
                    <div class="d-flex align-center">
                      <span class="text-caption">UPID: {{ item.raw.upid }} | Stock: {{ item.raw.quantity }}</span>
                    </div>
                  </template>
                </v-list-item>
              </template>
            </v-autocomplete>

            <!-- Selected Item Info -->
            <v-expand-transition>
              <v-alert
                v-if="selectedItem"
                :color="selectedItem.quantity < 20 ? 'warning' : 'info'"
                variant="tonal"
                class="mb-3"
                density="compact"
              >
                <div class="d-flex align-center justify-space-between">
                  <div>
                    <div><strong>Location:</strong> {{ selectedItem.location }}</div>
                    <div><strong>Available:</strong> {{ selectedItem.quantity }} units</div>
                    <div v-if="selectedItem.expiration"><strong>Expires:</strong> {{ formatDate(selectedItem.expiration) }}</div>
                  </div>
                </div>
              </v-alert>
            </v-expand-transition>

            <!-- Quantity Input -->
            <v-text-field
              v-model="checkoutQuantity"
              label="Quantity"
              type="number"
              :rules="[
                v => !!v || 'Quantity is required',
                v => v > 0 || 'Must be positive',
                v => v <= (selectedItem?.quantity || 0) || `Only ${selectedItem?.quantity || 0} available`
              ]"
              variant="outlined"
              density="comfortable"
              min="1"
              :max="selectedItem?.quantity"
              class="mb-3"
            >
              <template v-slot:prepend-inner>
                <v-icon size="small" color="primary">mdi-counter</v-icon>
              </template>
            </v-text-field>

            <!-- Purpose/Notes -->
            <v-textarea
              v-model="checkoutPurpose"
              label="Purpose / Notes (Optional)"
              variant="outlined"
              density="comfortable"
              rows="2"
              auto-grow
              class="mb-3"
            >
              <template v-slot:prepend-inner>
                <v-icon size="small" color="primary">mdi-note-text</v-icon>
              </template>
            </v-textarea>

            <!-- Success Message -->
            <v-expand-transition>
              <v-alert
                v-if="showSuccess"
                type="success"
                variant="tonal"
                class="mt-3"
              >
                Checkout completed successfully!
              </v-alert>
            </v-expand-transition>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="closeDialog"
            :disabled="processingCheckout"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="confirmScanCheckout"
            :loading="processingCheckout"
            variant="flat"
          >
            <v-icon start>mdi-checkout</v-icon>
            Check Out
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="showSnackbar"
      :timeout="3000"
      color="success"
      location="top"
    >
      <div class="d-flex align-center">
        <v-icon class="mr-3">mdi-check-circle</v-icon>
        <span>{{ snackbarMessage }}</span>
      </div>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

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

// State
const loading = ref(false)
const processingCheckout = ref(false)
const error = ref(null)

const isScanning = ref(false)
const scanProgress = ref(0)
const scannerStatus = ref('Scanner Ready')
const scannerMessage = ref('Place NFC tag near device')
const scannerFeedback = ref('Waiting for NFC tag...')
const scanResultDialog = ref(false)
const checkoutForm = ref(null)
const showSnackbar = ref(false)
const snackbarMessage = ref('')
const showSuccess = ref(false)
const isManualEntry = ref(false)

const inventory = ref([])
const selectedItem = ref(null)
const checkoutQuantity = ref(1)
const checkoutPurpose = ref('')

const lastScanTime = ref('')
const scansToday = ref(parseInt(localStorage.getItem('scansToday') || '0'))

let scanInterval = null

// Helper functions
const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString()
}

const getQuantityColor = (qty) => {
  if (qty < 20) return 'error'
  if (qty < 50) return 'warning'
  return 'success'
}

// Fetch inventory from database
const fetchInventory = async () => {
  loading.value = true
  error.value = null
  try {
    inventory.value = await api.get('/api/inventory?amount=1000&offset=0')
  } catch (err) {
    error.value = `Failed to load inventory.. BOY FIX TS RIGHT NOW OR ELSE YOU FAG - ${err.message}`
  } finally {
    loading.value = false
  }
}

// Scanner functions
const toggleScan = async () => {
  if (isScanning.value) {
    stopScanning()
  } else {
    await startScanning()
  }
}

const startScanning = async () => {
  isScanning.value = true
  scannerStatus.value = 'Scanning...'
  scannerMessage.value = 'NFC tag detected'
  scannerFeedback.value = 'Reading medication data...'
  scanProgress.value = 0
  isManualEntry.value = false
  
  // Simulate scanning progress
  scanInterval = setInterval(() => {
    if (scanProgress.value < 100) {
      scanProgress.value += 5
    }
  }, 50)
  
  // Simulate finding a tag after 2 seconds
  setTimeout(() => {
    if (isScanning.value) {
      clearInterval(scanInterval)
      scanProgress.value = 100
      
      // Get real item from inventory
      if (inventory.value.length > 0) {
        const randomItem = inventory.value[Math.floor(Math.random() * inventory.value.length)]
        handleScanResult(randomItem)
      } else {
        scannerFeedback.value = 'No items in inventory'
        setTimeout(() => {
          scannerFeedback.value = 'Waiting for NFC tag...'
        }, 2000)
      }
      
      stopScanning()
    }
  }, 2000)
}

const stopScanning = () => {
  isScanning.value = false
  scannerStatus.value = 'Scanner Ready'
  scannerMessage.value = 'Place NFC tag near device'
  scannerFeedback.value = 'Waiting for NFC tag...'
  scanProgress.value = 0
  
  if (scanInterval) {
    clearInterval(scanInterval)
    scanInterval = null
  }
}

const openManualEntry = () => {
  isManualEntry.value = true
  selectedItem.value = null
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
  showSuccess.value = false
  scanResultDialog.value = true
}

const handleScanResult = (item) => {
  selectedItem.value = item
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
  showSuccess.value = false
  isManualEntry.value = false
  
  // Update stats
  scansToday.value++
  localStorage.setItem('scansToday', scansToday.value.toString())
  lastScanTime.value = new Date().toLocaleTimeString()
  
  scanResultDialog.value = true
}

const confirmScanCheckout = async () => {
  const { valid } = await checkoutForm.value.validate()
  if (!valid) return

  if (!selectedItem.value) {
    error.value = 'Please select a medication'
    return
  }

  processingCheckout.value = true
  error.value = null
  
  try {
    // Call the actual API to remove inventory
    await api.post('/api/inventory/remove', {
      userid: 'admin',
      upid: selectedItem.value.upid,
      location: selectedItem.value.location,
      quantity: parseInt(checkoutQuantity.value),
      expiration: selectedItem.value.expiration
    })
    
    showSuccess.value = true
    
    // Refresh inventory
    await fetchInventory()
    
    setTimeout(() => {
      closeDialog()
      
      snackbarMessage.value = `${checkoutQuantity.value}x ${selectedItem.value.name} checked out`
      showSnackbar.value = true
      
      processingCheckout.value = false
    }, 1000)
  } catch (err) {
    error.value = `Failed to check out item: ${err.message}`
    processingCheckout.value = false
  }
}

const closeDialog = () => {
  scanResultDialog.value = false
  showSuccess.value = false
  isManualEntry.value = false
  selectedItem.value = null
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
}

// Watch selected item to reset quantity if needed
watch(selectedItem, (newItem) => {
  if (newItem && checkoutQuantity.value > newItem.quantity) {
    checkoutQuantity.value = newItem.quantity
  }
})

onMounted(() => {
  fetchInventory()
  scannerStatus.value = 'Scanner Ready'
})

onUnmounted(() => {
  if (scanInterval) {
    clearInterval(scanInterval)
  }
})
</script>

<style scoped>
.scanner-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-radius: 24px;
  transition: all 0.3s ease;
}

.scanner-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.2);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08);
}

.scanner-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.scanner-ring {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05) 0%, rgba(var(--v-theme-primary), 0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;
}

.scanner-ring.scanning-active {
  animation: ringPulse 2s infinite;
}

.scanner-inner {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: rgb(var(--v-theme-surface));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.scanner-icon.pulse {
  animation: iconPulse 2s infinite;
}

.dialog-card {
  border-radius: 20px;
  overflow: hidden;
}

.bg-primary-light {
  background: rgba(var(--v-theme-primary), 0.05);
}

@keyframes ringPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.4);
  }
  70% {
    box-shadow: 0 0 0 20px rgba(var(--v-theme-primary), 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0);
  }
}

@keyframes iconPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.gap-4 {
  gap: 16px;
}

@media (max-width: 600px) {
  .scanner-ring {
    width: 140px;
    height: 140px;
  }
  
  .scanner-inner {
    width: 100px;
    height: 100px;
  }
}
</style>