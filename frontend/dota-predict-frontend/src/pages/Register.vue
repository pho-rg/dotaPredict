<template>
  <div class="register-page">
    <header class="header">
      DOTAPREDICT
    </header>

    <main class="register-container">
      <Register />
    </main>
  </div>
</template>

<script setup>
import Register from '../components/Register.vue'
</script>

<style scoped>
.register-page {
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

.register-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem; /* Pour éviter que ça colle aux bords sur petit écran */
}
</style>

