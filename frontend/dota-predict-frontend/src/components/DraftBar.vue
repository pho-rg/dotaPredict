<template>
  <v-container fluid class="draftbar-container">
    <v-row justify="space-between">
      <v-col cols="5">
        <div class="d-flex flex-wrap" style="gap: 6px;">
          <HeroBan v-for="(id, i) in radiantBans" :key="'rb'+i" :id="id" />
        </div>
        <div class="d-flex flex-wrap mt-2" style="gap: 8px;">
          <HeroPick v-for="(id, i) in radiantPicks" :key="'rp'+i" :id="id" />
        </div>
        <div class="mt-3 d-flex flex-row align-center">
          <span class="text-start team-title me-4">RADIANT</span>
          <span class="text-start team-name">{{ radiantTeam }}</span>
        </div>
      </v-col>

      <v-col cols="2" class="text-center d-flex flex-column justify-end">
        <div class="text-h1 mb-2 prediction-text vs-title">VS</div>
        <div class="text-h5 mb-2 prediction-text">WIN PREDICTION</div>
        <div class="prediction-container mt-4">
          <div class="d-flex justify-space-between px-1 mb-1">
            <span
              class="prediction-text"
              :class="{ 'font-weight-bold': radiantWinChance >= 50 }"
            >
              {{ radiantWinChance }} %
            </span>
            <span
              class="prediction-text"
              :class="{ 'font-weight-bold': radiantWinChance < 50 }"
            >
              {{ 100 - radiantWinChance }} %
            </span>
          </div>
          <div class="prediction-bar">
            <div class="prediction-fill" :style="{ width: radiantWinChance + '%' }"></div>
          </div>
        </div>
      </v-col>

      <v-col cols="5">
        <div class="d-flex flex-wrap justify-end" style="gap: 6px;">
          <HeroBan v-for="(id, i) in [...this.direBans].reverse()" :key="'db' + (direBans.length - 1 - i)" :id="id" />
        </div>
        <div class="d-flex flex-wrap justify-end mt-2" style="gap: 8px;">
          <HeroPick v-for="(id, i) in [...this.direPicks].reverse()" :key="'dp' + (direPicks.length - 1 - i)" :id="id" />
        </div>
        <div class="mt-3 d-flex flex-row align-center justify-end">
          <span class="text-end team-name">{{ direTeam }}</span>
          <span class="text-end team-title ms-4">DIRE</span>
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
  }
}
</script>

<style scoped>
.draftbar-container {
  padding-block: 1%;
  padding-inline: 3%;
}
.team-name {
  margin-top: 10px;
  font-size: 20px;
  font-family: 'Mohave', sans-serif;
}
.team-title {
  margin-top: 10px;
  font-size: 30px;
  font-family: 'Mohave', sans-serif;
}
.prediction-text{
  font-family: 'Mohave', sans-serif;
}
.vs-title{
  font-weight: 600;
  letter-spacing: 0.2rem !important;
}
.prediction-container {
  width: 100%;
}

.prediction-bar {
  height: 6px;
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