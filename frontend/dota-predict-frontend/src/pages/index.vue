<template>
  <div class="app-container">
    <DraftPrediction />
  </div>
</template>

<script setup>
import DraftPrediction from './DraftPrediction.vue';
</script>

<style scoped>
.app-container {
  height: 100vh;          /* prend toute la hauteur de la fenêtre */
  display: flex;
  flex-direction: column; /* layout vertical */
}
</style>