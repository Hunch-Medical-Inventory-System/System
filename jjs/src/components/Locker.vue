<template>
  <div id="locker" class="page">
    <div class="page-header">
      <h2>In-Locker Inventory</h2>
      <p>All medical supplies currently in the locker</p>
    </div>
    
    <div class="table-container">
      <table v-if="inventory.length > 0">
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Name</th>
            <th>Category</th>
            <th>Quantity</th>
            <th>Expiry Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in inventory" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.category }}</td>
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
                @click="handleUseItem(item)"
                :disabled="item.quantity === 0"
              >
                Check Out
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-else class="empty-state">
        <i class="fas fa-cube"></i>
        <h3>No Items in Locker</h3>
        <p>Add items to your inventory to get started</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Locker',
  props: {
    inventory: Array
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
    handleUseItem(item) {
      const quantity = prompt(`Enter quantity to check out (max: ${item.quantity}):`, "1")
      if (quantity && quantity > 0 && quantity <= item.quantity) {
        this.$emit('use-item', item, parseInt(quantity))
      } else {
        alert('Invalid quantity')
      }
    }
  }
}
</script>

<style scoped>
.status {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status.expired {
  background-color: rgba(255, 71, 87, 0.1);
  color: #ff4757;
}

.status.warning {
  background-color: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.status.ok {
  background-color: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
}

.action-btn {
  padding: 6px 12px;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: opacity 0.3s;
}

.action-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>