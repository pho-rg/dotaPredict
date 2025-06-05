<template>
  <div class="hero-pick" @click="handleClick">
    <img :src="unknownSrc" alt="unknown" class="hero-image background" />
    <img
      v-if="id"
      :src="imageSrc"
      :alt="heroName"
      class="hero-image foreground"
    />
    <div class="hero-name-vertical" v-if="heroName">
  {{ heroName.toUpperCase() }}
</div>
  </div>
</template>

<script>
import heroes from '@/utils/heroes.json'

export default {
  props: {
    id: {
      type: Number,
      default: null
    },
    onClick: {
      type: Function,
      default: null
    }
  },
  computed: {
    hero() {
      return heroes.find(h => h.id === this.id)
    },
    heroName() {
      return this.hero ? this.hero.localized_name : 'Unknown'
    },
    imageSrc() {
      return new URL(`/src/assets/heroes/picks/${this.id}.png`, import.meta.url).href
    },
    unknownSrc() {
      return new URL('/src/assets/heroes/unknown.png', import.meta.url).href
    },
  },
  methods: {
    handleClick() {
      if (this.onClick) this.onClick(this.id)
    }
  }
}
</script>

<style scoped>
.hero-pick {
  width: 150px;
  height: 250px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  clip-path: polygon( /* coin haut gauche découpé */
    30px 0,   
    100% 0,
    100% 100%,
    0 100%,
    0 30px   
  );
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  position: absolute;
  top: 0;
  left: 0;
}

.background {
  z-index: 1;
}

.foreground {
  z-index: 2;
}

.hero-name-vertical {
  position: absolute;
  left: 78%; /* on part du bord droit */
  bottom: -30px;
  transform: rotate(-90deg);
  transform-origin: top left;
  font-size: 25px;
  font-weight: bold;
  color: white;
  text-shadow: 0px 0px 3px black;
  white-space: nowrap;
  z-index: 4;
  pointer-events: none;
  font-family: 'Mohave', sans-serif;
}
</style>