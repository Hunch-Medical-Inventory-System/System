<template>
  <div class="header">
    <div class="logo">
      <h1>JJs <span>V2.0</span></h1>
    </div>
    <button class="mobile-menu-btn" @click="$emit('toggle-mobile-menu')">
      <i class="fas fa-bars"></i>
    </button>
    <div class="user-info">
      <img src="#" alt="">
      <div class="user-details">
        <h4>{{ user.username }}</h4>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Header',
  props: {
    user: Object
  }
}
</script>

<style scoped>
.header {
  background: linear-gradient(to right, #4a6cf7, #8a2be2);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.logo span {
  color: #b19cd9;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  background-color: white;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }
  
  .header {
    padding: 15px;
  }
}

@media (max-width: 576px) {
  .logo h1 {
    font-size: 1.3rem;
  }
}
</style>