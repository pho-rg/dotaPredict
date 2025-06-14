<template>
  <div class="menu-container">
    <div class="content-grow">
      <HeaderBar />
    </div>
    <div class="menu-container">
      <Menu />
    </div>
  </div>
</template>
<script setup>
  import HeaderBar from '../components/HeaderBar.vue'
  import Menu from '../components/Menu.vue'
</script>
<style>
.menu-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  height: 100%;
}

.content-grow {
  flex-grow: 1;
}
</style>
