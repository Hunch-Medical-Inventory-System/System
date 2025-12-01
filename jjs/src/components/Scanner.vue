<template>
  <div id="scanner" class="page">
    <div class="page-header">
      <h2>NFC Scanner</h2>
      <p>Scan medicine NFC tags to check out items</p>
    </div>
    
    <div class="scanner-container">
      <div class="scanner-icon">
        <i class="fas fa-qrcode"></i>
      </div>
      <h3>{{ scannerStatus }}</h3>
      <p>{{ scannerMessage }}</p>
      <button 
        class="scanner-btn" 
        @click="startScan"
        :disabled="!nfcSupported || isScanning"
      >
        {{ scanButtonText }}
      </button>
      <p style="margin-top: 20px; font-size: 0.9rem; color: #666666;">
        <i class="fas fa-info-circle"></i> This feature requires an NFC-enabled device and browser permission
      </p>
    </div>
    
    <!-- Modal for checkout -->
    <div v-if="showModal" class="modal active">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Check Out Medication</h3>
          <button class="close-modal" @click="closeModal">&times;</button>
        </div>
        <div class="form-group">
          <label for="medication-name">Medication</label>
          <input type="text" id="medication-name" :value="scannedItem.name" readonly>
        </div>
        <div class="form-group">
          <label for="quantity">Quantity to Check Out</label>
          <input type="number" id="quantity" v-model="checkoutQuantity" :max="scannedItem.quantity" min="1">
        </div>
        <div class="form-group">
          <label for="purpose">Purpose</label>
          <input type="text" id="purpose" v-model="purpose" placeholder="Enter purpose for this medication">
        </div>
        <button class="scanner-btn" @click="confirmCheckout" style="width: 100%;">
          Confirm Check Out
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Scanner',
  props: {
    inventory: Array
  },
  data() {
    return {
      nfcSupported: 'NDEFReader' in window,
      isScanning: false,
      scannerStatus: 'NFC Scanner',
      scannerMessage: 'Place the medicine near your device to scan its NFC tag',
      showModal: false,
      scannedItem: null,
      checkoutQuantity: 1,
      purpose: '',
      nfcReader: null
    }
  },
  computed: {
    scanButtonText() {
      if (!this.nfcSupported) return 'NFC Not Available'
      if (this.isScanning) return 'Scanning...'
      return 'Start NFC Scan'
    }
  },
  mounted() {
    if (this.nfcSupported) {
      this.scannerStatus = 'NFC Scanner Ready'
      this.scannerMessage = 'Click "Start NFC Scan" and place the medicine near your device'
    }
  },
  methods: {
    async startScan() {
      if (!this.nfcSupported) return
      
      try {
        this.nfcReader = new NDEFReader()
        await this.nfcReader.scan()
        
        this.isScanning = true
        this.scannerStatus = 'Scanning for NFC Tags'
        this.scannerMessage = 'Place the medicine near your device now'
        
        this.nfcReader.onreading = (event) => {
          this.handleNFCScan(event)
        }
        
        this.nfcReader.onreadingerror = () => {
          this.scannerStatus = 'Scanning Error'
          this.scannerMessage = 'Error reading NFC tag. Please try again.'
          this.isScanning = false
        }
      } catch (error) {
        console.error("Error starting NFC scan:", error)
        this.scannerStatus = 'NFC Error'
        this.scannerMessage = 'NFC scanning is not supported or permission was denied.'
        this.isScanning = false
      }
    },
    handleNFCScan(event) {
      const decoder = new TextDecoder()
      for (const record of event.message.records) {
        if (record.recordType === "text") {
          const text = decoder.decode(record.data)
          this.processScannedData(text)
        }
      }
    },
    processScannedData(nfcData) {
      this.isScanning = false
      
      const scannedItem = this.inventory.find(item => 
        item.id.toLowerCase().includes(nfcData.toLowerCase()) || 
        item.name.toLowerCase().includes(nfcData.toLowerCase())
      )
      
      if (scannedItem) {
        this.scannedItem = scannedItem
        this.checkoutQuantity = 1
        this.purpose = ''
        this.showModal = true
        
        this.scannerStatus = 'Medication Found'
        this.scannerMessage = `${scannedItem.name} identified successfully`
      } else {
        this.scannerStatus = 'Medication Not Found'
        this.scannerMessage = 'This medication is not in the inventory. Would you like to add it?'
        
        if (confirm('Medication not found in inventory. Would you like to add it?')) {
          this.addNewMedication(nfcData)
        }
      }
    },
    addNewMedication(nfcData) {
      const name = prompt('Enter medication name:', nfcData)
      if (!name) return
      
      const category = prompt('Enter medication category:', 'General')
      if (!category) return
      
      const quantity = parseInt(prompt('Enter quantity:', "1"))
      if (isNaN(quantity)) return
      
      const expiryDate = prompt('Enter expiry date (YYYY-MM-DD):', 
        new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
      if (!expiryDate) return
      
      const newItem = {
        id: `MED-${Date.now()}`,
        name,
        category,
        quantity,
        expiryDate,
        location: 'Locker'
      }
      
      this.$emit('add-item', newItem)
    },
    confirmCheckout() {
      if (this.scannedItem && this.checkoutQuantity > 0) {
        this.$emit('checkout-item', this.scannedItem, parseInt(this.checkoutQuantity))
        this.closeModal()
      } else {
        alert('Please enter a valid quantity')
      }
    },
    closeModal() {
      this.showModal = false
      this.scannedItem = null
    }
  }
}
</script>

<style scoped>
.scanner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.scanner-icon {
  font-size: 5rem;
  color: #4a6cf7;
  margin-bottom: 20px;
}

.scanner-btn {
  padding: 12px 30px;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
  margin-top: 20px;
}

.scanner-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.scanner-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  font-size: 1.5rem;
  color: #333333;
}

.close-modal {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666666;
}

@media (max-width: 576px) {
  .scanner-container {
    padding: 20px;
  }
  
  .scanner-icon {
    font-size: 3rem;
  }
}
</style>