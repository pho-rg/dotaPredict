<template>
  <v-container>
    <v-row justify="space-between">
      <v-col cols="5">
        <h3 class="text-center">Radiant - {{ radiantTeam }}</h3>
        <div class="d-flex flex-wrap mt-2" style="gap: 6px;">
          <HeroBan v-for="(id, i) in radiantBans" :key="'rb'+i" :id="id" />
        </div>
        <div class="d-flex flex-wrap" style="gap: 10px;">
          <HeroPick v-for="(id, i) in radiantPicks" :key="'rp'+i" :id="id" />
        </div>
      </v-col>

      <v-col cols="2" class="text-center">
        <div class="text-h5 mb-2">Win Prediction</div>
        <v-progress-linear
          :value="radiantWinChance"
          color="white"
          height="24"
          rounded
        >
          <template #default>
            <div class="d-flex justify-space-between px-2">
              <span>{{ radiantWinChance }}%</span>
              <span>{{ 100 - radiantWinChance }}%</span>
            </div>
          </template>
        </v-progress-linear>
      </v-col>

      <v-col cols="5">
        <h3 class="text-center">Dire - {{ direTeam }}</h3>
        <div class="d-flex flex-wrap justify-end mt-2" style="gap: 6px;">
          <HeroBan v-for="(id, i) in [...this.direBans].reverse()" :key="'db' + (direBans.length - 1 - i)" :id="id" />
        </div>
        <div class="d-flex flex-wrap justify-end" style="gap: 10px;">
          <HeroPick v-for="(id, i) in [...this.direPicks].reverse()" :key="'dp' + (direPicks.length - 1 - i)" :id="id" />
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