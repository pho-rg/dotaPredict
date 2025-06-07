<template>
  <div class="app-container">
    <Login />
  </div>
</template>

<script setup>
import Login from './Login.vue';
</script>

<style scoped>
.app-container {
  height: 100vh;          /* prend toute la hauteur de la fenêtre */
  display: flex;
  flex-direction: column; /* layout vertical */
}
</style>
