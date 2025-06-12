<template>
    <v-container class="hero-selection">
        <div class="close-btn-container">
            <v-btn icon color="#912728" @click="$emit('close')" class="close-btn">
                <v-icon icon="mdi-close" />
            </v-btn>
        </div>
        <div class="scrollable-content">
          <span class="modal-title">SELECT A HERO</span>
          <div class="hero-grid">
            <div
              v-for="(heroes, attr) in heroesByAttr"
              :key="attr"
              class="hero-column"
            >
              <div class="attr-label">
                <img
                  :key="attr"
                  :src="`/src/assets/attr/${attr}.png`"
                  :alt="attr"
                  class="attr-img"
                />
                <span>{{ attrLabels[attr] }}</span>
              </div>
              <div class="hero-list">
                <img
                  v-for="hero in heroes"
                  :key="hero.id"
                  :src="`/src/assets/heroes/bans/${hero.id}.png`"
                  :alt="hero.localized_name"
                  class="hero-img"
                  @click="props.selectHero(hero.id)"
                />
              </div>
            </div>
          </div>
        </div>
    </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import rawHeroes from '/src/utils/heroes.json'

const props = defineProps({
  selectHero: Function,
  close: Function
})

// Grouper les héros par type
const heroesByAttr = {
  str: [],
  agi: [],
  int: [],
  all: []
}

const heroes = Object.values(rawHeroes)

heroes.forEach(hero => {
  if (hero.primary_attr in heroesByAttr) {
    heroesByAttr[hero.primary_attr].push(hero)
  }
})

// Tri par ordre alphabétique
Object.keys(heroesByAttr).forEach(attr => {
  heroesByAttr[attr].sort((a, b) => a.localized_name.localeCompare(b.localized_name))
})

const attrLabels = {
  str: 'STRENGTH',
  agi: 'AGILITY',
  int: 'INTELLIGENCE',
  all: 'UNIVERSAL'
}

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
  width: 90vw;
  height: 90vh;
  max-height: 100%;
  box-sizing: border-box;
  background: #404040;
  border-radius: 10px;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 24px;
}

.scrollable-content {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-right: 8px; 
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
  margin-bottom: 30px;
  padding-bottom: 5px;
  border-bottom: 2px solid #ffffff;
}

.hero-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); /* adapte les colonnes selon la taille */
  gap: 24px;
  width: 100%;
  flex: 1;
}

.hero-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.attr-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 7px;
  font-family: 'Mohave', sans-serif;
  font-size: 24px;
  color: #ffffff;
  margin-bottom: 20px;
}

.hero-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
  gap: 4px;
  justify-items: center;
  align-items: center;
}

@media (max-width: 1920px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
  }
}

@media (max-height: 1100px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
  }
}

@media (max-width: 1280px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
  }
}

@media (max-height: 700px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
  }
}

@media (max-width: 854px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(40px, 1fr));
  }
}

@media (max-height: 560px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(40px, 1fr));
  }
}

@media (max-width: 640px) {
  .hero-list {
    grid-template-columns: repeat(auto-fit, minmax(30px, 1fr));
  }
}

.hero-img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  cursor: pointer;
  border-radius: 4px;
  transition: transform 0.2s ease;
  max-height: 100%; 
}

.attr-img {
  width: 30px;
  top: -1px;
  position: relative;
}

.hero-img:hover {
  transform: scale(1.7);
}
</style>
