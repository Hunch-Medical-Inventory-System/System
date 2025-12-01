<template>
  <div id="logs" class="page">
    <div class="page-header">
      <h2>System Logs</h2>
      <p>Complete history of inventory activities</p>
    </div>
    
    <div class="table-container">
      <table v-if="logs.length > 0">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>User</th>
            <th>Action</th>
            <th>Item</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.timestamp">
            <td>{{ log.timestamp }}</td>
            <td>{{ log.user }}</td>
            <td>{{ log.action }}</td>
            <td>{{ log.item || 'N/A' }}</td>
            <td>{{ log.details }}</td>
          </tr>
        </tbody>
      </table>
      
      <div v-else class="empty-state">
        <i class="fas fa-clipboard-list"></i>
        <h3>No Logs Available</h3>
        <p>Logs will appear here as you use the system</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Logs',
  props: {
    logs: Array
  }
}
</script>

<style scoped>
/* Reuses styles from Dashboard component */
</style>