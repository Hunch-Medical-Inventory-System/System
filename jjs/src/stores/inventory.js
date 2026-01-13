import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useInventoryStore = defineStore('inventory', () => {
  const inventory = ref([])
  const logs = ref([])
  const alerts = ref([])

  const fetchInventory = async () => {
    // API call placeholder
    inventory.value = []
    return []
  }

  const fetchLogs = async () => {
    logs.value = []
    return []
  }

  const fetchAlerts = async () => {
    alerts.value = []
    return []
  }

  const checkOutItem = async (itemId, quantity, purpose) => {
    console.log(`Checking out item ${itemId}, quantity: ${quantity}, purpose: ${purpose}`)
    return true
  }

  return {
    inventory,
    logs,
    alerts,
    fetchInventory,
    fetchLogs,
    fetchAlerts,
    checkOutItem
  }
})