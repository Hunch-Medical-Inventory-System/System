export const useInventoryStore = defineStore('inventory', () => {
  const inventory = ref([])
  const logs = ref([])
  const alerts = ref([])

  const API_BASE = "http://localhost:5000/api"

  const fetchInventory = async () => {
    try {
      const res = await fetch(`${API_BASE}/inventory`)
      if (!res.ok) throw new Error("Failed to fetch inventory")
      inventory.value = await res.json()
      return inventory.value
    } catch (err) {
      console.error("Inventory fetch error:", err)
      return []
    }
  }

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/logs`)
      if (!res.ok) throw new Error("Failed to fetch logs")
      logs.value = await res.json()
      return logs.value
    } catch (err) {
      console.error(err)
      return []
    }
  }

  const fetchAlerts = async () => {
    try {
      const res = await fetch(`${API_BASE}/alerts`)
      if (!res.ok) throw new Error("Failed to fetch alerts")
      alerts.value = await res.json()
      return alerts.value
    } catch (err) {
      console.error(err)
      return []
    }
  }

  const checkOutItem = async (itemId, quantity, purpose) => {
    try {
      const res = await fetch(`${API_BASE}/inventory/${itemId}/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quantity, purpose })
      })

      if (!res.ok) throw new Error("Checkout failed")

      await fetchInventory()
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  }

  const addItem = async (item) => {
    try {
      const res = await fetch(`${API_BASE}/inventory`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(item)
      })

      if (!res.ok) throw new Error("Add item failed")

      await fetchInventory()
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  }

  return {
    inventory,
    logs,
    alerts,
    fetchInventory,
    fetchLogs,
    fetchAlerts,
    checkOutItem,
    addItem
  }
})