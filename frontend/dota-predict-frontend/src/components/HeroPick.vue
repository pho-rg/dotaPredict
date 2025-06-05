<template>
  <div class="hero-pick" ref="heroPick" @click="handleClick">
    <img :src="unknownSrc" alt="unknown" class="hero-image background" />
    <img
      v-if="id"
      :src="imageSrc"
      :alt="heroName"
      class="hero-image foreground"
    />
    <div
      class="hero-name-vertical"
      v-if="heroName"
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
      leftOffset: 0
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
  mounted() {
    const el = this.$refs.heroPick
    if (!el) return

    const updateLayout = () => {
      const height = el.offsetHeight
      const width = el.offsetWidth

      this.fontSize = Math.max(10, Math.min(25, (height - 60) * 0.18))
      this.leftOffset = Math.max(30, Math.min(width - 5, (width - 5) * 0.78))
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
</style>