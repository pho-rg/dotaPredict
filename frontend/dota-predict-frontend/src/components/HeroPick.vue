<template>
  <div class="hero-pick" ref="heroPick" @click="handleClick">
    <img :src="fogSrc" alt="fog" class="hero-image background" />
    
    <template v-if="id === -1">
      <v-progress-circular
        indeterminate
        :size=progressSize
        :width=progressWidth
        class="loader"
      />
    </template>
    
    <img
      v-if="id === -2"
      :src="plusIconSrc"
      alt="Add"
      :style="{ height: plusIconSize + 'px', width: plusIconSize + 'px', cursor: 'pointer' }"
      class="overlay-center"
    />

    <img
      v-if="id > 0"
      :src="imageSrc"
      :alt="heroName"
      class="hero-image foreground"
    />
    
    <div
      class="hero-name-vertical"
      v-if="heroName && id > 0"
      :style="{ fontSize: fontSize + 'px', left: leftOffset + 'px' }"
    >
      {{ heroName.toUpperCase() }}
    </div>
  </div>
</template>

<script>
import heroes from '@/utils/heroes.json'

export default {
  props: {
    id: {
      /**
       * id > 0 -> hero
       * id = -1 -> next hero to be chosen (real-time match)
       * id = -2 -> hero to chose (analysis mode)
       */
      type: Number, 
      default: null
    },
    onClick: {
      type: Function,
      default: null
    }
  },
  data() {
    return {
      fontSize: 25,
      progressSize: 38,
      progressWidth: 6,
      leftOffset: 0,
      plusIconSize: 64
    }
  },
  computed: {
    hero() {
      return heroes.find(h => h.id === this.id)
    },
    heroName() {
      return this.hero ? this.hero.localized_name : null
    },
    imageSrc() {
      return new URL(`/src/assets/heroes/picks/${this.id}.png`, import.meta.url).href
    },
    fogSrc() {
      return new URL('/src/assets/heroes/fog.png', import.meta.url).href
    },
    plusIconSrc() {
      return new URL('/src/assets/plus-icon.png', import.meta.url).href
    }
  },
  mounted() {
    const el = this.$refs.heroPick
    if (!el) return

    const updateLayout = () => {
      const height = el.offsetHeight
      const width = el.offsetWidth

      this.fontSize = Math.max(10, Math.min(25, (height - 60) * 0.18))
      this.leftOffset = Math.max(30, Math.min(width - 5, (width - 5) * 0.78))
      this.progressSize = Math.max(16, Math.min(40, (height - 60) * 0.4))
      this.progressWidth = Math.max(2, Math.min(6, (height - 60) * 0.075))
      this.plusIconSize = Math.max(24, Math.min(64, (height - 60) * 0.6))
    }

    this._resizeObserver = new ResizeObserver(updateLayout)
    this._resizeObserver.observe(el)

    requestAnimationFrame(() => {
      updateLayout()
    })
  },
  beforeUnmount() {
    if (this._resizeObserver) {
      this._resizeObserver.disconnect()
    }
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
  width: calc(100% / 5 - 28px);
  max-height: 180px;
  aspect-ratio: 0.6;
  position: relative;
  overflow: hidden;
  clip-path: polygon(
    25% 0,
    100% 0,
    100% 100%,
    0 100%,
    0 15%
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
  animation: fog-move 30s ease-in-out infinite;
  transform: scale(1.5);
  opacity: 1;
  filter: blur(1.5px);
  will-change: transform;
}
@keyframes fog-move {
  0% {
    transform: scale(1.5) translateX(0px);
  }
  25% {
    transform: scale(1.5) translateX(-10px);
  }
  50% {
    transform: scale(1.5) translateX(10px);
  }
  75% {
    transform: scale(1.5) translateX(-10px);
  }
  100% {
    transform: scale(1.5) translateX(0px);
  }
}

.foreground {
  z-index: 2;
}

.hero-name-vertical {
  position: absolute;
  bottom: -13%;
  transform: rotate(-90deg);
  transform-origin: top left;
  font-weight: bold;
  color: white;
  text-shadow: 0px 0px 3px black;
  white-space: nowrap;
  z-index: 4;
  pointer-events: none;
  font-family: 'Mohave', sans-serif;
}
.loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3; 
  color: white; 
}
.overlay-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
}
</style>