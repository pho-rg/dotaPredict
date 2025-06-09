<template>
  <v-container fluid class="draftbar-container">
    <v-row justify="space-between">
      <v-col cols="5">
        <div class="d-flex flex-wrap" style="gap: 6px;">
          <HeroBan v-for="(id, i) in radiantBans" :key="'rb'+i" :id="id" />
        </div>
        <div class="d-flex flex-wrap mt-2" style="gap: 8px;">
          <HeroPick v-for="(id, i) in radiantPicks" :key="'rp'+i" :id="id" :onClick="()=>pickOnClick(id)" />
        </div>
        
      </v-col>

      <v-col cols="2" class="text-center d-flex flex-column justify-end">
        <div class="d-flex flex-column align-center">
          <div class="vs-title" :style="{ fontSize: vsTitleSize + 'px'}">VS</div>
          <div class="prediction-title" :style="{ fontSize: predictionTitleSize + 'px'}">WIN PREDICTION</div>
        </div>
      </v-col>

      <v-col cols="5">
        <div class="d-flex flex-wrap justify-end" style="gap: 6px;">
          <HeroBan v-for="(id, i) in [...this.direBans].reverse()" :key="'db' + (direBans.length - 1 - i)" :id="id" />
        </div>
        <div class="d-flex flex-wrap justify-end mt-2" style="gap: 8px;">
          <HeroPick v-for="(id, i) in [...this.direPicks].reverse()" :key="'dp' + (direPicks.length - 1 - i)" :id="id" :onClick="()=>pickOnClick(id)" />
        </div>
        
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <div class="d-flex flex-row align-center">
          <span class="text-start team-title mr-4 ms-4" :style="{ fontSize: teamTitleSize + 'px'}">RADIANT</span>
          <span class="text-start team-name" :style="{ fontSize: teamNameSize + 'px'}">{{ radiantTeam }}</span>
        </div>
      </v-col>
      <v-col cols="2">
        <div class="prediction-container">
          <div class="d-flex justify-space-between">
            <span
              class="prediction-text"
              :class="{ 'font-weight-bold': radiantWinChance >= 50 }"
              :style="{ fontSize: predictionValueSize + 'px'}"
            >
              {{ radiantWinChance }} %
            </span>
            <span
              class="prediction-text"
              :class="{ 'font-weight-bold': radiantWinChance < 50 }"
              :style="{ fontSize: predictionValueSize + 'px'}"
            >
              {{ 100 - radiantWinChance }} %
            </span>
          </div>
          <div class="prediction-bar" :style="{ height: predictionBarHeight + 'px'}">
            <div class="prediction-fill" :style="{ width: radiantWinChance + '%' }"></div>
          </div>
        </div>
      </v-col>
      <v-col cols="5">
        <div class="d-flex flex-row align-center justify-end">
          <span class="text-end team-name" :style="{ fontSize: teamNameSize + 'px'}">{{ direTeam }}</span>
          <span class="text-end team-title ms-4 mr-4" :style="{ fontSize: teamTitleSize + 'px'}">DIRE</span>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import HeroPick from './HeroPick.vue'
import HeroBan from './HeroBan.vue'

export default {
  components: { HeroPick, HeroBan },
  props: {
    radiantPicks: Array,
    direPicks: Array,
    radiantBans: Array,
    direBans: Array,
    radiantWinChance: Number,
    radiantTeam: String,
    direTeam: String
  },
  data() {
    return {
      containerWidth: 0,
      teamTitleSize: 30, // valeur par défaut
      teamNameSize: 20,
      predictionValueSize: 18,
      predictionBarHeight: 6,
      predictionTitleSize: 30,
      vsTitleSize: 90
    }
  },
  mounted() {
    this.updateSizes();
    window.addEventListener('resize', this.updateSizes);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateSizes);
  },
  methods: {
    updateSizes() {
      this.containerWidth = this.$el.offsetWidth || window.innerWidth;

      // fix dimensions proportions
      this.teamTitleSize = Math.min(Math.max(this.containerWidth * 0.02, 12), 30); // 12px - 30px
      this.teamNameSize = Math.min(Math.max(this.containerWidth * 0.01, 10), 20); // 10px - 20px
      this.predictionValueSize = Math.min(Math.max(this.containerWidth * 0.01, 10), 18); // 10px - 18px
      this.predictionBarHeight = Math.min(Math.max(this.containerWidth * 0.0045, 2), 6); // 2px - 6px
      this.vsTitleSize = Math.min(Math.max(this.containerWidth * 0.06, 10), 90); // 10px - 90px
      this.predictionTitleSize = Math.min(Math.max(this.containerWidth * 0.015, 10), 25); // 10px - 25px
    },
    pickOnClick(id) {
      if (id > 0) {
        console.log("hero :", id);
      } else if (id === -1) {
        console.log("waiting for the player's pick...");
      } else if (id === -2) {
        console.log("waiting for analyst input");
      }
    }
  }
}
</script>

<style scoped>
.draftbar-container {
  padding-block: 1%;
  padding-inline: 3%;
  position: relative;
  z-index: 1;

  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 3%;
    right: 3%;
    height: 60%;
    background: linear-gradient(
      to right,
      #130f0f 0%,
      #491313 49.9%,
      #491313 51.1%,
      #130f0f 100%
    );
    background-size: 200% 100%;
    background-position: 100% 0;
    animation: aura-move 6s ease-in-out infinite;
    z-index: -1;
  }
}

@keyframes aura-move {
  0% {
    background-position: 100% 0;
  }
  50% {
    background-position: 0% 0;
  }
  100% {
    background-position: 100% 0;
  }
}

.team-name, .team-title {
  font-family: 'Mohave', sans-serif;
}

.vs-title {
  font-family: 'Mohave', sans-serif;
  font-weight: 600;
  margin-bottom: -6px;
  letter-spacing: 0.2rem !important;
}

.prediction-title {
  border-bottom: 1px solid white;
  padding-bottom: 1%;
  width: 70%;
  font-family: 'Mohave', sans-serif;
}

.prediction-text {
  font-family: 'Mohave', sans-serif;
}

.prediction-container {
  width: 100%;
}

.prediction-bar {
  background-color: #444; /* gris foncé */
  width: 100%;
  position: relative;
  border-radius: 2px;
  overflow: hidden;
}

.prediction-fill {
  height: 100%;
  background-color: white;
  transition: width 0.3s ease;
}
</style>