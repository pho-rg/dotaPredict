<template>
  <v-container class="menu-component-container" fluid>
    <v-row align="center" class="component-title" justify="space-between">
      <span>Live matches</span>
      <v-btn v-if="checkRole" align="end" color="#912728" @click="gotoSimulation()">
        Simulate a draft
      </v-btn>
    </v-row>
    <v-row v-for="match in matches" :key="match.match_id" class="match-row">
      <v-col class="match-infos">
        {{ match.radiant_team }} VS {{ match.dire_team }}
      </v-col>

      <v-col class="match-infos">
        <span :class="getStatusDotClass(match.match_status)"></span>
        {{ getStatusLabel(match.match_status) }}
      </v-col>

      <v-col  class="match-infos">
        <img v-if="match.pro_match" alt="Pro Match" class="pro-match-icon" src="/src/assets/trophy.png" />
      </v-col>

      <v-col align="end" class="match-action">
        <v-btn color="#727272" @click="seeAnalysis(match.match_id)">
          Go to analysis
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import {computed, onMounted, onUnmounted, ref} from 'vue'
  import router from '../router/index.js'
  import { getAllLiveMatches } from '../service/matchService.js'

  const matches = ref([])

  let intervalId = null

  const matchStatusLabel = {
    draft_to_start: 'Draft to start',
    draft_in_progress: 'Draft in progress',
    draft_finished: 'Draft finished',
  }

  const checkRole = computed(() => {
    const role = localStorage.getItem('role')
    return role === 'analyst'
  })

  const getStatusLabel = status => {
    return matchStatusLabel[status] || status || 'Live'
  }

  const getStatusDotClass = status => {
    const statusClasses = {
      draft_to_start: 'status-dot blue-dot',
      draft_in_progress: 'status-dot green-dot',
      draft_finished: 'status-dot purple-dot',
    }
    return statusClasses[status]
  }

  const fetchMatches = async () => {
    try {
      const data = await getAllLiveMatches()
      matches.value = data
    } catch (error) {
      console.error('Failed to fetch matches', error)
    }
  }

  const seeAnalysis = matchId => {
    router.push(`/draftPrediction/${matchId}`)
  }

  const gotoSimulation = () => {
    router.push('/draftSimulation')
  }

  onMounted(async () => {
    await fetchMatches()
    intervalId = setInterval(fetchMatches, 5000) // update match list every 5s
  })

  onUnmounted(() => {
    if (intervalId) clearInterval(intervalId)
  })
</script>
<style scoped>
  .menu-component-container {
    display: flex;
    align-content: center;
    flex-direction: column;
    background: #404040;
    border-radius: 10px;
    margin: 20px;
    margin-left: auto;
    margin-right: auto;
    max-width: 1000px;
    padding: 16px;
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

  .status-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
  }

  .green-dot {
    background-color: #4caf50; /* vert - draft en cours */
  }

  .blue-dot {
    background-color: #008cff; /* orange - draft à commencer */
  }

  .purple-dot {
    background-color: #8718dd; /* rouge - match terminé */
  }
</style>
