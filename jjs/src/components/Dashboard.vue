<template>
  <div id="home" class="page">
    <div class="page-header">
      <h2>Dashboard</h2>
      <p>Welcome to JJs V2.0 Medical Inventory System</p>
    </div>
    
    <div class="dashboard-cards">
      <div class="card">
        <div class="card-icon">
          <i class="fas fa-cube"></i>
        </div>
        <h3>{{ totalItems }}</h3>
        <p>Items in Locker</p>
      </div>
      <div class="card">
        <div class="card-icon">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h3>{{ expiringItems }}</h3>
        <p>Expiring Soon</p>
      </div>
      <div class="card">
        <div class="card-icon">
          <i class="fas fa-clipboard-list"></i>
        </div>
        <h3>{{ recentActivities }}</h3>
        <p>Recent Activities</p>
      </div>
    </div>
    
    <div class="page-header">
      <h2>Recent Activity</h2>
    </div>
    
    <div class="table-container">
      <table v-if="recentLogs.length > 0">
        <thead>
          <tr>
            <th>Item</th>
            <th>Action</th>
            <th>User</th>
            <th>Date & Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in recentLogs" :key="log.timestamp">
            <td>{{ log.item || 'N/A' }}</td>
            <td>{{ log.action }}</td>
            <td>{{ log.user }}</td>
            <td>{{ log.timestamp }}</td>
          </tr>
        </tbody>
      </table>
      
      <div v-else class="empty-state">
        <i class="fas fa-clipboard-list"></i>
        <h3>No Recent Activity</h3>
        <p>Activity will appear here as you use the system</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  props: {
    inventory: Array,
    logs: Array
  },
  computed: {
    totalItems() {
      return this.inventory.length
    },
    expiringItems() {
      return this.inventory.filter(item => {
        const expiryDate = new Date(item.expiryDate)
        const today = new Date()
        const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
        return daysUntilExpiry <= 30 && daysUntilExpiry > 0
      }).length
    },
    recentActivities() {
      return this.logs.length
    },
    recentLogs() {
      return this.logs.slice(-5).reverse()
    }
  }
}
</script>

<style scoped>
.page {
  display: block;
}

.page-header {
  margin-bottom: 25px;
}

.page-header h2 {
  font-size: 1.8rem;
  color: #333333;
  margin-bottom: 10px;
}

.page-header p {
  color: #666666;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  border-left: 4px solid #4a6cf7;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.card-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  font-size: 1.5rem;
  color: white;
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
}

.card h3 {
  font-size: 1.5rem;
  margin-bottom: 5px;
}

.card p {
  color: #666666;
  font-size: 0.9rem;
}

.table-container {
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

th, td {
  padding: 15px 20px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333333;
}

tr:last-child td {
  border-bottom: none;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666666;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #e0e0e0;
}

@media (max-width: 768px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
}
</style>