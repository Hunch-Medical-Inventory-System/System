// stores/inventory.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useInventoryStore = defineStore('inventory', () => {
  const inventory = ref([])
  const logs = ref([])
  const loading = ref(false)

  // Mock data - replace with actual API calls
  const mockInventory = [
    {
      id: 'MED-001',
      name: 'Paracetamol',
      category: 'Pain Relief',
      quantity: 100,
      expiryDate: '2024-12-31',
      location: 'A1'
    },
    {
      id: 'MED-002',
      name: 'Amoxicillin',
      category: 'Antibiotic',
      quantity: 50,
      expiryDate: '2024-06-30',
      location: 'B2'
    }
  ]

  const mockLogs = [
    {
      id: 1,
      timestamp: '2024-01-15 10:30:00',
      user: 'demo',
      action: 'Check Out',
      item: 'Paracetamol',
      details: 'Quantity: 10'
    }
  ]

  // Computed properties
  const totalItems = computed(() => inventory.value.length)
  
  const expiringItems = computed(() => {
    const today = new Date()
    const thirtyDaysFromNow = new Date(today.setDate(today.getDate() + 30))
    return inventory.value.filter(item => {
      const expiryDate = new Date(item.expiryDate)
      return expiryDate <= thirtyDaysFromNow && expiryDate > new Date()
    })
  })

  const expiredItems = computed(() => {
    const today = new Date()
    return inventory.value.filter(item => new Date(item.expiryDate) < today)
  })

  const recentLogs = computed(() => logs.value.slice(-5).reverse())

  // Actions
  const fetchInventory = async () => {
    loading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      inventory.value = mockInventory
    } catch (error) {
      console.error('Failed to fetch inventory:', error)
    } finally {
      loading.value = false
    }
  }

  const fetchLogs = async () => {
    loading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      logs.value = mockLogs
    } catch (error) {
      console.error('Failed to fetch logs:', error)
    } finally {
      loading.value = false
    }
  }

  const addItem = async (item) => {
    const newItem = {
      ...item,
      id: `MED-${Date.now()}`
    }
    inventory.value.push(newItem)
    
    // Add to logs
    await addLog('System', 'Add', `Added new item: ${item.name}`, item.name)
  }

  const updateItem = async (id, updates) => {
    const index = inventory.value.findIndex(item => item.id === id)
    if (index !== -1) {
      inventory.value[index] = { ...inventory.value[index], ...updates }
      await addLog('System', 'Update', `Updated item: ${updates.name || id}`, id)
    }
  }

  const deleteItem = async (id) => {
    const item = inventory.value.find(item => item.id === id)
    inventory.value = inventory.value.filter(item => item.id !== id)
    await addLog('System', 'Delete', `Deleted item: ${item?.name || id}`, id)
  }

  const checkOutItem = async (id, quantity, purpose) => {
    const item = inventory.value.find(item => item.id === id)
    if (item && item.quantity >= quantity) {
      item.quantity -= quantity
      await addLog('System', 'Check Out', `Quantity: ${quantity}, Purpose: ${purpose}`, item.name)
      
      // Remove if quantity is 0
      if (item.quantity === 0) {
        await deleteItem(id)
      }
      return true
    }
    return false
  }

  const addLog = async (user, action, details, item = null) => {
    const now = new Date()
    const timestamp = `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`
    
    const newLog = {
      id: Date.now(),
      timestamp,
      user,
      action,
      item,
      details
    }
    
    logs.value.push(newLog)
  }

  return {
    inventory,
    logs,
    loading,
    totalItems,
    expiringItems,
    expiredItems,
    recentLogs,
    fetchInventory,
    fetchLogs,
    addItem,
    updateItem,
    deleteItem,
    checkOutItem,
    addLog
  }
})