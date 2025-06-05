<template>
  <div class="ban-frame" @click="handleClick">
    <img
      v-if="id"
      :src="imageSrc"
      alt="banned hero"
      class="ban-image"
    />
    <div class="ban-overlay" v-if="id"></div>
    <div class="ban-line" v-if="id"></div>
    <div v-else class="ban-placeholder">?</div>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      default: null
    }
  },
  computed: {
    imageSrc() {
      if (!this.id) return null
      return new URL(`/src/assets/heroes/bans/${this.id}.png`, import.meta.url).href
    }
  },
  methods: {
    handleClick() {
      this.$emit('click', this.id)
    }
  }
}
</script>

<style scoped>
.ban-frame {
  width: calc(100% / 7 - 32px); /* 7 par ligne avec 6px de gap */
  max-height: 40px;
  aspect-ratio: 75 / 42; /* ou approx 1.7857 */
  background: #222;
  position: relative;
  overflow: hidden;
}

.ban-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: grayscale(100%);
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.ban-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 2;
}

.ban-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 1000px; 
  height: 1px;
  background: red;
  transform: rotate(-27.5deg); /* angle exact calculé */
  transform-origin: left bottom;
  z-index: 3;
}

.ban-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: clamp(2px, 1.5vw, 25px);
  color: #fff;
  z-index: 2;
  user-select: none;
  pointer-events: none;
}

</style>