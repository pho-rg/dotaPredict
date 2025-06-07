<template>
  <div class="login-page">
    <header class="header">
      DOTAPREDICT
    </header>

    <main class="login-container">
      <Login />
    </main>
  </div>
</template>

<script setup>
import Login from '../components/Login.vue'
</script>

<style scoped>
.login-page {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  height: 100%;
}

.header {
  position: fixed;
  top: 10px;
  left: 10px;
  margin-left: 10px;
  font-size: 40px;
  font-family: 'Mohave', sans-serif;
  font-weight: bold;
}

.login-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem; /* Pour éviter que ça colle aux bords sur petit écran */
}
</style>

