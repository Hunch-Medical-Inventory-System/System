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

            <!-- Selected Medication Display -->
            <v-expand-transition>
              <v-alert
                v-if="selectedMedication"
                :color="getMedicationColor(selectedMedication.upid)"
                variant="tonal"
                class="mb-4"
              >
                <div class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center">
                    <v-avatar :color="getMedicationColor(selectedMedication.upid)" size="32" class="mr-3">
                      <v-icon :color="getMedicationColor(selectedMedication.upid)">mdi-pill</v-icon>
                    </v-avatar>
                    <div class="text-left">
                      <div class="font-weight-bold">{{ selectedMedication.name }}</div>
                      <div class="text-caption">UPID: {{ selectedMedication.upid }} | Stock: {{ selectedMedication.quantity }}</div>
                    </div>
                  </div>
                  <v-btn
                    icon="mdi-close"
                    variant="text"
                    size="small"
                    @click="selectedMedication = null"
                  ></v-btn>
                </div>
              </v-alert>
            </v-expand-transition>

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
              :disabled="!selectedMedication && !isScanning"
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

    <!-- Medication Selection Panel (From Database) -->
    <v-row class="mt-6">
      <v-col cols="12" lg="8" xl="6" class="mx-auto">
        <v-card class="medication-panel" elevation="0">
          <v-card-item class="pb-2">
            <div class="d-flex align-center">
              <v-icon color="primary" class="mr-2">mdi-pill</v-icon>
              <v-card-title class="text-subtitle-1 font-weight-bold pa-0">
                Select Medication to Scan
              </v-card-title>
              <v-spacer></v-spacer>
              <v-chip v-if="selectedMedication" color="success" size="small">
                <v-icon start size="14">mdi-check</v-icon>
                Ready to scan
              </v-chip>
            </div>
          </v-card-item>
          
          <v-card-text>
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <div class="text-caption mt-2">Loading medications...</div>
            </div>

            <!-- Error State -->
            <v-alert
              v-else-if="error"
              type="error"
              variant="tonal"
              class="mb-3"
            >
              {{ error }}
            </v-alert>

            <!-- Medication Grid -->
            <v-row v-else dense>
              <v-col cols="6" sm="3" v-for="item in filteredMedications" :key="item.upid">
                <v-hover v-slot="{ isHovering, props }">
                  <v-card
                    v-bind="props"
                    :class="['medication-button', { 
                      'medication-button-selected': selectedMedication?.upid === item.upid,
                      'low-stock': item.quantity < 20
                    }]"
                    :elevation="isHovering ? 4 : 1"
                    @click="selectMedication(item)"
                  >
                    <div class="text-center pa-3">
                      <v-avatar
                        :color="getMedicationColor(item.upid)"
                        size="48"
                        class="mb-2"
                        variant="tonal"
                      >
                        <v-icon :color="getMedicationColor(item.upid)" size="24">mdi-pill</v-icon>
                      </v-avatar>
                      <div class="font-weight-medium">{{ item.name }}</div>
                      <div class="text-caption text-medium-emphasis mt-1">
                        UPID: {{ item.upid }}
                      </div>
                      <v-chip
                        :color="item.quantity < 20 ? 'error' : 'success'"
                        size="x-small"
                        class="mt-2"
                      >
                        Stock: {{ item.quantity }}
                      </v-chip>
                    </div>
                  </v-card>
                </v-hover>
              </v-col>
            </v-row>

            <!-- No Medications Message -->
            <div v-if="!loading && filteredMedications.length === 0" class="text-center py-4">
              <v-icon size="48" color="grey" class="mb-2">mdi-pill-off</v-icon>
              <div class="text-body-2">No medications found in database</div>
            </div>

            <!-- Quick Info -->
            <v-divider class="my-4"></v-divider>
            <div class="text-caption text-medium-emphasis text-center">
              Select a medication above, then click Start Scanning to check it out
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
            <v-avatar :color="getMedicationColor(selectedMedication?.upid)" size="40" class="mr-3">
              <v-icon color="white">mdi-pill</v-icon>
            </v-avatar>
            <div>
              <v-card-title class="text-h6 pa-0">
                Check Out {{ selectedMedication?.name }}
              </v-card-title>
              <v-card-subtitle class="pa-0 text-caption">
                UPID: {{ selectedMedication?.upid }}
              </v-card-subtitle>
            </div>
          </div>
        </v-card-item>

        <v-card-text class="pt-4">
          <v-form ref="checkoutForm" @submit.prevent="confirmScanCheckout">
            <!-- Selected Item Info -->
            <v-alert
              :color="selectedMedication?.quantity < 20 ? 'warning' : 'info'"
              variant="tonal"
              class="mb-3"
            >
              <div class="d-flex align-center">
                <v-icon start :color="selectedMedication?.quantity < 20 ? 'warning' : 'info'">mdi-information</v-icon>
                <div>
                  <div><strong>Current Stock:</strong> {{ selectedMedication?.quantity }} units</div>
                  <div v-if="selectedMedication?.location"><strong>Location:</strong> {{ selectedMedication.location }}</div>
                </div>
              </div>
            </v-alert>

            <!-- Quantity Input -->
            <v-text-field
              v-model="checkoutQuantity"
              label="Quantity"
              type="number"
              :rules="[
                v => !!v || 'Quantity is required',
                v => v > 0 || 'Must be positive',
                v => v <= (selectedMedication?.quantity || 0) || `Only ${selectedMedication?.quantity || 0} available`
              ]"
              variant="outlined"
              density="comfortable"
              min="1"
              :max="selectedMedication?.quantity"
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
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'

const API_BASE = 'http://127.0.0.1:8080'

const api = {
  async get(path) {
    try {
      const res = await fetch(`${API_BASE}${path}`)
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      return res.json()
    } catch (err) {
      throw new Error(`Failed to connect to database: ${err.message}`)
    }
  },
  async post(path, body) {
    try {
      const res = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      return res.json()
    } catch (err) {
      throw new Error(`Failed to connect to database: ${err.message}`)
    }
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

// Medication selection
const selectedMedication = ref(null)

const inventory = ref([])
const checkoutQuantity = ref(1)
const checkoutPurpose = ref('')

const lastScanTime = ref('')
const scansToday = ref(parseInt(localStorage.getItem('scansToday') || '0'))

let scanInterval = null

// Filter to show only specific medications we want (with the specified UPIDs)
const filteredMedications = computed(() => {
  const allowedUPIDs = ['GUMMY-BEAR', 'SKITTLES', 'MIKE-N-IKE', 'STARBURSTS']
  return inventory.value.filter(item => allowedUPIDs.includes(item.upid))
})

// Helper functions
const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString()
}

const getMedicationColor = (upid) => {
  const colorMap = {
    'GUMMY-BEAR': 'red',
    'SKITTLES': 'purple',
    'MIKE-N-IKE': 'green',
    'STARBURSTS': 'orange'
  }
  return colorMap[upid] || 'primary'
}

// Medication functions
const selectMedication = (medication) => {
  if (selectedMedication.value?.upid === medication.upid) {
    selectedMedication.value = null // Toggle off if same medication
    scannerMessage.value = 'Place NFC tag near device'
    scannerFeedback.value = 'Waiting for NFC tag...'
  } else {
    selectedMedication.value = medication
    scannerMessage.value = `Ready to scan ${medication.name}`
    scannerFeedback.value = 'Click Start Scanning to begin'
  }
}

// Fetch inventory from database
const fetchInventory = async () => {
  loading.value = true
  error.value = null
  try {
    inventory.value = await api.get('/api/inventory?amount=1000&offset=0')
    
    // Check if our specific medications exist
    const allowedUPIDs = ['GUMMY-BEAR', 'SKITTLES', 'MIKE-N-IKE', 'STARBURSTS']
    const foundUPIDs = inventory.value.map(item => item.upid)
    const missingUPIDs = allowedUPIDs.filter(upid => !foundUPIDs.includes(upid))
    
    if (missingUPIDs.length > 0) {
      error.value = `Warning: Missing medications in database: ${missingUPIDs.join(', ')}`
    }
  } catch (err) {
    error.value = `Database connection failed: ${err.message}`
    inventory.value = []
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
  if (!selectedMedication.value) {
    error.value = 'Please select a medication first'
    return
  }
  
  if (selectedMedication.value.quantity <= 0) {
    error.value = `${selectedMedication.value.name} is out of stock`
    return
  }
  
  isScanning.value = true
  scannerStatus.value = 'Scanning...'
  scannerMessage.value = `Scanning ${selectedMedication.value.name}...`
  scannerFeedback.value = 'Reading NFC tag...'
  scanProgress.value = 0
  
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
      
      // Handle the scan result with selected medication
      handleScanResult()
      
      stopScanning()
    }
  }, 2000)
}

const stopScanning = () => {
  isScanning.value = false
  scannerStatus.value = 'Scanner Ready'
  
  if (selectedMedication.value) {
    scannerMessage.value = `Ready to scan ${selectedMedication.value.name}`
    scannerFeedback.value = 'Click Start Scanning to begin'
  } else {
    scannerMessage.value = 'Place NFC tag near device'
    scannerFeedback.value = 'Waiting for NFC tag...'
  }
  
  scanProgress.value = 0
  
  if (scanInterval) {
    clearInterval(scanInterval)
    scanInterval = null
  }
}

const openManualEntry = () => {
  isManualEntry.value = true
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
  showSuccess.value = false
  scanResultDialog.value = true
}

const handleScanResult = () => {
  if (!selectedMedication.value) return
  
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

  if (!selectedMedication.value) {
    error.value = 'No medication selected'
    return
  }

  if (parseInt(checkoutQuantity.value) > selectedMedication.value.quantity) {
    error.value = `Only ${selectedMedication.value.quantity} units available`
    return
  }

  processingCheckout.value = true
  error.value = null
  
  try {
    // Call the API to remove inventory
    await api.post('/api/inventory/remove', {
      userid: 'admin',
      upid: selectedMedication.value.upid,
      location: selectedMedication.value.location || 'Unknown',
      quantity: parseInt(checkoutQuantity.value),
      expiration: selectedMedication.value.expiration
    })
    
    showSuccess.value = true
    
    // Refresh inventory
    await fetchInventory()
    
    // Update the selected medication with new quantity
    const updatedMedication = inventory.value.find(item => item.upid === selectedMedication.value.upid)
    if (updatedMedication) {
      selectedMedication.value = updatedMedication
    }
    
    setTimeout(() => {
      closeDialog()
      
      snackbarMessage.value = `${checkoutQuantity.value}x ${selectedMedication.value.name} checked out`
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
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
}

// Watch selected medication to update scanner messages and check stock
watch(selectedMedication, (newMedication) => {
  if (newMedication && !isScanning.value) {
    if (newMedication.quantity <= 0) {
      scannerMessage.value = `${newMedication.name} is out of stock`
      scannerFeedback.value = 'Please select another medication'
      error.value = `${newMedication.name} is out of stock`
    } else {
      scannerMessage.value = `Ready to scan ${newMedication.name}`
      scannerFeedback.value = 'Click Start Scanning to begin'
    }
  } else if (!newMedication && !isScanning.value) {
    scannerMessage.value = 'Place NFC tag near device'
    scannerFeedback.value = 'Waiting for NFC tag...'
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

.medication-panel {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-radius: 16px;
}

.medication-button {
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  border-radius: 12px !important;
}

.medication-button:hover {
  transform: translateY(-2px);
}

.medication-button-selected {
  border-color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.05);
}

.medication-button.low-stock {
  border-color: rgb(var(--v-theme-error));
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