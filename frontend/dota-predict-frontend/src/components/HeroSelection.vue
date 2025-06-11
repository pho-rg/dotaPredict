<template>
    <v-container class="hero-selection">
        <div class="close-btn-container">
            <v-btn icon color="#912728" @click="$emit('close')" class="close-btn">
                <v-icon icon="mdi-close" />
            </v-btn>
        </div>
            <span class="modal-title">SELECT A HERO</span>
        <v-btn @click="selectHero(18)">test</v-btn>
    </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  selectHero: Function,
  close: Function
})


const isWideEnough = ref(window.innerWidth >= 1024);
const isTallEnough = ref(window.innerHeight >= 500);

const updateWindowSize = () => {
  isWideEnough.value = window.innerWidth >= 1024
  isTallEnough.value = window.innerHeight >= 500
}

onMounted(async () => {
  window.addEventListener('resize', updateWindowSize)
  updateWindowSize ()
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWindowSize)
})

</script>

<style scoped>
.hero-selection {
  width: 90%;
  height: 90%;
  background: #404040;
  border-radius: 10px;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 24px;
}

.close-btn-container {
  position: absolute;
  top: -20px;
  right: -20px;
}

.close-btn {
  color: white;
}

.modal-title {
    text-align: center;
    font-family: 'Mohave', sans-serif;
    font-size: 35px;
    margin-bottom: 20px;
}
</style>
