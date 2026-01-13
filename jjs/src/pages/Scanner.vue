<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mb-8">
          <h1 class="gradient-text text-h3 font-weight-bold mb-2">
            NFC Scanner
          </h1>
          <p class="text-body-1 text-medium-emphasis">
            Scan medicine NFC tags to check out items in real-time
          </p>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8" lg="6" class="mx-auto">
        <v-card class="gradient-card pa-8 text-center">
          <div
            class="scanner-animation mx-auto mb-6"
            :class="{ scanning: isScanning }"
          >
            <v-icon size="64" color="white">mdi-nfc</v-icon>
          </div>

          <h3 class="gradient-text text-h4 font-weight-bold mb-4">
            {{ scannerStatus }}
          </h3>

          <p class="text-body-1 text-medium-emphasis mb-6">
            {{ scannerMessage }}
          </p>

          <v-progress-linear
            v-if="isScanning"
            v-model="scanProgress"
            color="primary"
            height="8"
            rounded
            class="mb-6"
          />

          <v-alert
            v-if="scannerFeedback"
            variant="tonal"
            color="info"
            class="mb-6"
          >
            <v-icon start>mdi-information</v-icon>
            {{ scannerFeedback }}
          </v-alert>

          <v-btn
            :color="isScanning ? 'error' : 'primary'"
            size="x-large"
            :prepend-icon="isScanning ? 'mdi-stop' : 'mdi-play'"
            @click="toggleScan"
            :loading="loading"
            class="mb-6"
          >
            {{ isScanning ? 'Stop Scanning' : 'Start Scanning' }}
          </v-btn>

          <v-divider class="my-6" />

          <div class="d-flex justify-center align-center flex-wrap gap-4">
            <div class="d-flex align-center">
              <v-icon color="primary" class="mr-2">mdi-microchip</v-icon>
              <span class="text-body-2">Last scan: {{ lastScanTime }}</span>
            </div>
            <div class="d-flex align-center">
              <v-icon color="primary" class="mr-2">mdi-database</v-icon>
              <span class="text-body-2">Scans today: {{ scansToday }}</span>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-8">
      <v-col cols="12">
        <div class="mb-6">
          <h3 class="gradient-text text-h4 font-weight-bold mb-2">
            Test Medications
          </h3>
          <p class="text-body-1 text-medium-emphasis">
            Test the scanner with these medications
          </p>
        </div>

        <div class="d-flex flex-wrap gap-3">
          <v-btn
            v-for="med in testMedications"
            :key="med"
            variant="tonal"
            @click="testScan(med)"
            :disabled="isScanning"
          >
            <v-icon start>mdi-capsule</v-icon>
            {{ med }}
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Scan Result Dialog -->
    <v-dialog v-model="scanResultDialog" max-width="500">
      <v-card>
        <v-card-title>Medication Found</v-card-title>
        <v-card-text>
          <v-form ref="checkoutForm">
            <v-text-field
              v-model="scannedItem.name"
              label="Medication"
              readonly
              class="mb-4"
            />
            <v-text-field
              v-model="checkoutQuantity"
              label="Quantity"
              type="number"
              :rules="[
                v => !!v || 'Quantity is required',
                v => v > 0 || 'Quantity must be positive'
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
          <v-btn @click="scanResultDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="confirmScanCheckout"
            :loading="processingCheckout"
          >
            Check Out
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
const isScanning = ref(false)
const scanProgress = ref(0)
const scannerStatus = ref('Ready to Scan')
const scannerMessage = ref('Place the medicine NFC tag near your device to automatically identify and check out items')
const scannerFeedback = ref('Scanner will automatically detect compatible NFC tags')
const scanResultDialog = ref(false)
const processingCheckout = ref(false)
const checkoutForm = ref(null)

const scannedItem = ref({})
const checkoutQuantity = ref(1)
const checkoutPurpose = ref('')

const lastScanTime = ref('Never')
const scansToday = ref(0)
const testMedications = [
  'Aspirin 100mg',
  'Amoxicillin 500mg',
  'Insulin Glargine',
  'Metformin 850mg'
]

const scanInterval = ref(null)

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
  scannerMessage.value = 'Move NFC tag closer to your device'
  scannerFeedback.value = 'Searching for NFC tags...'
  scanProgress.value = 0
  
  // Check if Web NFC is available
  if (!('NDEFReader' in window)) {
    scannerFeedback.value = 'NFC not supported in this browser. Using simulation mode.'
  }
  
  // Simulate scanning progress
  scanInterval.value = setInterval(() => {
    if (scanProgress.value < 100) {
      scanProgress.value += 10
    }
  }, 300)
  
  // Simulate finding a tag after 3 seconds
  setTimeout(() => {
    if (isScanning.value) {
      clearInterval(scanInterval.value)
      scanProgress.value = 100
      
      // For demo: pick a random inventory item
      if (inventoryStore.inventory.length > 0) {
        const randomIndex = Math.floor(Math.random() * inventoryStore.inventory.length)
        handleScanResult(inventoryStore.inventory[randomIndex])
      }
      
      stopScanning()
    }
  }, 3000)
}

const stopScanning = () => {
  isScanning.value = false
  scannerStatus.value = 'Ready to Scan'
  scannerMessage.value = 'Place the medicine NFC tag near your device to automatically identify and check out items'
  scannerFeedback.value = 'Scanner will automatically detect compatible NFC tags'
  scanProgress.value = 0
  
  if (scanInterval.value) {
    clearInterval(scanInterval.value)
    scanInterval.value = null
  }
}

const testScan = (medicationName) => {
  const item = inventoryStore.inventory.find(i => 
    i.name.toLowerCase().includes(medicationName.toLowerCase())
  )
  
  if (item) {
    handleScanResult(item)
  } else {
    scannerStatus.value = 'Medication Not Found'
    scannerMessage.value = `${medicationName} not found in inventory`
    
    // Simulate adding new medication
    setTimeout(() => {
      scannerStatus.value = 'Ready to Scan'
      scannerMessage.value = 'Place the medicine NFC tag near your device to automatically identify and check out items'
    }, 2000)
  }
}

const handleScanResult = (item) => {
  scannedItem.value = { ...item }
  checkoutQuantity.value = 1
  checkoutPurpose.value = ''
  
  // Update stats
  scansToday.value++
  lastScanTime.value = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  
  scanResultDialog.value = true
}

const confirmScanCheckout = async () => {
  const { valid } = await checkoutForm.value.validate()
  if (!valid) return

  processingCheckout.value = true
  
  const success = await inventoryStore.checkOutItem(
    scannedItem.value.id,
    checkoutQuantity.value,
    checkoutPurpose.value
  )
  
  if (success) {
    scanResultDialog.value = false
    scannerStatus.value = 'Checkout Successful'
    scannerMessage.value = `${scannedItem.value.name} checked out successfully`
    
    setTimeout(() => {
      scannerStatus.value = 'Ready to Scan'
      scannerMessage.value = 'Place the medicine NFC tag near your device to automatically identify and check out items'
    }, 2000)
  }
  
  processingCheckout.value = false
}

onMounted(() => {
  // Load scan stats from localStorage
  const stats = JSON.parse(localStorage.getItem('scanStats') || '{}')
  lastScanTime.value = stats.lastScanTime || 'Never'
  scansToday.value = stats.scansToday || 0
})

// Clean up interval on unmount
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (scanInterval.value) {
    clearInterval(scanInterval.value)
  }
})
</script>

<style scoped>
.scanner-animation {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.scanner-animation.scanning {
  animation: scannerPulse 2s ease-in-out infinite;
}
</style>