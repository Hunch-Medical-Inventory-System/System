<template>
  <div id="expired" class="page">
    <div class="page-header">
      <h2>Expired & Warnings</h2>
      <p>Items requiring attention</p>
    </div>
    
    <div class="table-container">
      <table v-if="warningItems.length > 0">
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>Quantity</th>
            <th>Expiry Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in warningItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.location || 'N/A' }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.expiryDate }}</td>
            <td>
              <span :class="['status', getItemStatus(item).class]">
                {{ getItemStatus(item).text }}
              </span>
            </td>
            <td>
              <button 
                class="action-btn"
                @click="handleAction(item)"
              >
                {{ getActionText(item) }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-else class="empty-state">
        <i class="fas fa-check-circle"></i>
        <h3>No Warnings</h3>
        <p>All items are in good condition</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Warnings',
  props: {
    inventory: Array
  },
  computed: {
    warningItems() {
      return this.inventory.filter(item => {
        const status = this.getItemStatus(item)
        return status.class !== 'ok'
      })
    }
  },
  methods: {
    getItemStatus(item) {
      const expiryDate = new Date(item.expiryDate)
      const today = new Date()
      const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
      
      if (daysUntilExpiry < 0) {
        return { class: 'expired', text: 'Expired' }
      } else if (daysUntilExpiry <= 30) {
        return { class: 'warning', text: 'Expiring Soon' }
      } else {
        return { class: 'ok', text: 'OK' }
      }
    },
    getActionText(item) {
      const status = this.getItemStatus(item)
      return status.class === 'expired' ? 'Dispose' : 'Use First'
    },
    handleAction(item) {
      const status = this.getItemStatus(item)
      
      if (status.class === 'expired') {
        if (confirm(`Are you sure you want to dispose of ${item.name}? This action cannot be undone.`)) {
          this.$emit('dispose-item', item)
        }
      } else {
        const quantity = prompt(`Enter quantity to check out (max: ${item.quantity}):`, "1")
        if (quantity && quantity > 0 && quantity <= item.quantity) {
          this.$emit('use-item', item, parseInt(quantity))
        } else {
          alert('Invalid quantity')
        }
      }
    }
  }
}
</script>

<style scoped>
/* Reuses styles from Locker component */
</style>