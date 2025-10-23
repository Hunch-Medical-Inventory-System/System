<!-- pages/Expired.vue -->
<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>Expired & Warnings</v-card-title>
              <v-card-subtitle>Items requiring attention</v-card-subtitle>
            </v-card-item>
            
            <v-card-text>
              <v-tabs v-model="tab" color="primary">
                <v-tab value="expired">Expired ({{ inventoryStore.expiredItems.length }})</v-tab>
                <v-tab value="expiring">Expiring Soon ({{ inventoryStore.expiringItems.length }})</v-tab>
                <v-tab value="low">Low Stock ({{ lowStockItems.length }})</v-tab>
              </v-tabs>

              <v-window v-model="tab">
                <v-window-item value="expired">
                  <warning-items-table
                    :items="inventoryStore.expiredItems"
                    warning-type="expired"
                    @dispose="disposeItem"
                    @use="useItem"
                  />
                </v-window-item>

                <v-window-item value="expiring">
                  <warning-items-table
                    :items="inventoryStore.expiringItems"
                    warning-type="expiring"
                    @dispose="disposeItem"
                    @use="useItem"
                  />
                </v-window-item>

                <v-window-item value="low">
                  <warning-items-table
                    :items="lowStockItems"
                    warning-type="low"
                    @dispose="disposeItem"
                    @use="useItem"
                  />
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Check Out Dialog -->
    <v-dialog v-model="checkOutDialog" max-width="500">
      <v-card>
        <v-card-title>Use Medication</v-card-title>
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
          <v-btn color="primary" @click="confirmUse">Use Item</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import WarningItemsTable from '@/components/WarningItemsTable.vue'

const inventoryStore = useInventoryStore()

const tab = ref('expired')
const checkOutDialog = ref(false)
const selectedItem = ref({})
const checkOutQuantity = ref(1)
const purpose = ref('')

const lowStockItems = computed(() => {
  return inventoryStore.inventory.filter(item => item.quantity < 10)
})

const useItem = (item) => {
  selectedItem.value = { ...item }
  checkOutQuantity.value = 1
  purpose.value = ''
  checkOutDialog.value = true
}

const confirmUse = async () => {
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

const disposeItem = async (item) => {
  if (confirm(`Are you sure you want to dispose of ${item.name}? This action cannot be undone.`)) {
    await inventoryStore.deleteItem(item.id)
    await inventoryStore.fetchInventory()
  }
}

onMounted(async () => {
  await inventoryStore.fetchInventory()
})
</script>