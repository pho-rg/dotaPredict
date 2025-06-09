<template>
  <div class="login-container">
    <div class="app-name">
      DOTAPREDICT
    </div>
    <div class="login-component">
      <Login />
    </div>
  </div>
</template>

<script setup>
  import Login from '../components/Login.vue'
</script>

<style scoped>
.login-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.app-name {
  top: 10px;
  left: 10px;
  margin-top: 15px;
  margin-left: 15px;
  font-size: 40px;
  font-family: 'Mohave', sans-serif;
  font-weight: bold;
}

.login-component {
  margin-top: 5vh;
}
</style>
