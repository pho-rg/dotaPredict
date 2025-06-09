<template>
  <v-container class="menu-component-container">
    <v-row class="component-title">
      <span>Live matches</span>
    </v-row>
    <v-row v-for="match in matches" :key="match.match_id" class="match-row">
      <v-col class="match-infos">
        {{ match.radiant_team }} VS {{ match.dire_team }}
      </v-col>

      <v-col class="match-infos">
        <span v-if="match.draft_in_progress" class="green-dot"></span>
        {{ match.draft_in_progress ? 'Draft in progress' : 'Live' }}
      </v-col>

      <v-col class="match-action">
        <v-btn color="#727272" @click="seeAnalysis(match.match_id)">
          Go to analysis view
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-btn color="#912728" @click="gotoSimulation()">
          Simulate a draft
        </v-btn>
    </v-row>
  </v-container>
</template>
<script setup>
  import { onMounted, ref } from 'vue'
  import router from '../../router/index.js'
  import { getAllMatches } from '../../service/matchService.js'

  const matches = ref([])

  const fetchMatches = async () => {
    try {
      const data = await getAllMatches()
      matches.value = data
    } catch (error) {
      console.error('Failed to fetch matches', error)
    }
  }

  const seeAnalysis = matchId => {
    router.push(`/draftPrediction/${matchId}`)
  }

  const gotoSimulation = () => {
    // TODO create simulation page
    router.push('/draftPrediction/')
  }

  onMounted(fetchMatches)
</script>
<style scoped>
  .menu-component-container {
    display: flex;
    align-content: center;
    flex-direction: column;
    background: #404040;
    border-radius: 10px;
  }

  .component-title {
    font-size: 25px;
    font-family: 'Mohave', sans-serif;
    font-weight: bold;
    margin: 10px;
  }

  .match-infos {
    font-family: 'Mohave', sans-serif;
  }

  .match-row {
    margin-left: 10px;
  }

  .green-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  background-color: #4caf50; /* vert */
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}
</style>
