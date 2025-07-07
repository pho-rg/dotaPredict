<template>
  <v-container class="menu-component-container" fluid v-if="!archivedMode">
    <v-row align="center" class="component-title" justify="space-between">
      <span>Live matches</span>
      <div class="nav-btns">
        <v-btn
          align="end"
          color="#727272"
          @click="() => archivedMode = !archivedMode"
        >
          <div class="nav-btn-content">
            <v-icon icon="mdi-history" size="22" />
            <span>Show archived matches</span>
          </div>
        </v-btn>
        <v-btn
          v-if="checkRole"
          align="end"
          color="#912728"
          @click="gotoSimulation()"
        >
          <div class="nav-btn-content">
            <v-icon icon="mdi-magnify-scan" size="22" />
            <span>Simulate a draft</span>
          </div>
        </v-btn>
      </div>
    </v-row>
    <v-row v-if="matches.length === 0" class="no-match-row">No match in progress.</v-row>
    <v-row v-for="match in matches" :key="match.match_id" class="match-row">
      <v-col class="match-infos">
        {{ match.radiant_team }} VS {{ match.dire_team }}
      </v-col>

      <v-col class="match-infos">
        <span :class="getStatusDotClass(match.match_status)" />
        {{ getStatusLabel(match.match_status) }}
      </v-col>

      <v-col class="match-infos">
        <div v-if="match.pro_match" style="display: flex; align-items: center; flex-direction: row; gap: 5px;"> 
          <img alt="Pro Match" class="pro-match-icon" src="/src/assets/trophy.png">
          <span>PROFESSIONNAL</span>
        </div>
      </v-col>

      <v-col align="center">
        <v-btn color="#727272" @click="seeAnalysis(match.match_id)">
          <div class="nav-btn-content">
            <span>Go to draft analysis</span>
            <v-icon icon="mdi-chevron-right" size="24" style="padding-bottom: 2px;" />
          </div>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
  <v-container class="menu-component-container" fluid v-if="archivedMode">
    <v-row align="center" class="component-title" justify="space-between">
      <span>Archived matches</span>
      <div class="nav-btns">
        <v-btn
          align="end"
          color="#727272"
          @click="() => archivedMode = !archivedMode"
        >
          <div class="nav-btn-content">
            <v-icon icon="mdi-broadcast" size="22" />
            <span>Show live matches</span>
          </div>
        </v-btn>
        <v-btn
          v-if="checkRole"
          align="end"
          color="#912728"
          @click="gotoSimulation()"
        >
          <div class="nav-btn-content">
            <v-icon icon="mdi-magnify-scan" size="22" />
            <span>Simulate a draft</span>
          </div>
        </v-btn>
      </div>
    </v-row>
    <v-row v-if="archivedMatches.length === 0" class="no-match-row">No archived match.</v-row>
    <v-row v-for="archived_match in archivedMatches" :key="archived_match.match_id" class="match-row">
      <v-col class="match-infos">
        {{ archived_match.radiant_team }} VS {{ archived_match.dire_team }}
      </v-col>

      <v-col class="match-infos">
        <span class="status-dot red-dot" />
        Match finished
      </v-col>

      <v-col class="match-infos">
        <div v-if="archived_match.pro_match" style="display: flex; align-items: center; flex-direction: row; gap: 5px;"> 
          <img alt="Pro Match" class="pro-match-icon" src="/src/assets/trophy.png">
          <span>PROFESSIONNAL</span>
        </div>
      </v-col>

      <v-col class="match-infos">
        <div style="display: flex; align-items: center; flex-direction: row; gap: 5px;"> 
          Winner : <span class="team-label">{{ archived_match.radiant_win ? "RADIANT" : "DIRE" }} </span> 
          <v-icon :icon="archived_match.radiant_win ? 'mdi-sword' : 'mdi-security'" :size="archived_match.radiant_win ? 18 : 16" color="#ca4b4d"/>
        </div>
      </v-col>

      <v-col align="center">
        <v-btn color="#727272" @click="seeAnalysis(archived_match.match_id)">
          <div class="nav-btn-content">
            <span>Show the draft</span>
            <v-icon icon="mdi-chevron-right" size="24" style="padding-bottom: 2px;" />
          </div>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
  import { computed, onMounted, onUnmounted, ref } from 'vue'
  import router from '../router/index.js'
  import { getAllLiveMatches, getAllMatchesHistory } from '../service/matchService.js'

  const archivedMode = ref(false)

  const matches = ref([])
  const archivedMatches = ref([])

  let intervalId = null
  let archiveIntervalId = null

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

  const fetchArchivedMatches = async () => {
    try {
      const data = await getAllMatchesHistory()
      archivedMatches.value = data
    } catch (error) {
      console.error('Failed to fetch archived matches', error)
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
    await fetchArchivedMatches()
    intervalId = setInterval(fetchMatches, 2000) // update match list every 2s
    archiveIntervalId = setInterval(fetchArchivedMatches, 10000) // update match list every 10s
  })

  onUnmounted(() => {
    if (intervalId) clearInterval(intervalId)
    if (archiveIntervalId) clearInterval(archiveIntervalId)
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
    padding-bottom: 30px;
  }

  .component-title {
    font-size: 25px;
    font-family: 'Mohave', sans-serif;
    font-weight: bold;
    margin: 10px;
    padding-bottom: 15px;
    padding-inline: 15px;
    border-bottom: white solid 2px;
  }

  .match-infos{
    font-family: 'Mohave', sans-serif;
  }

  .nav-btn-content {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Mohave', sans-serif;
    font-size: 16px;
  }

  .nav-btns {
    display: flex;
    flex-direction: row;
    gap: 10px;
  }

  .match-row {
    margin-left: 10px;
    display: flex;
    align-items: center;
  }

  .no-match-row {
    margin-left: 10px;
    display: flex;
    align-items: center;
    font-family: 'Mohave', sans-serif;
    justify-content: center;
    padding-block: 10px;
  }

  .status-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
  }

  .team-label {
    font-weight: bold;
    color: #ca4b4d;
  }

  .green-dot {
    background-color: #4caf50;
  }

  .blue-dot {
    background-color: #008cff;
  }

  .purple-dot {
    background-color: #8718dd; 
  }

  .red-dot {
    background-color: #912728; 
  }
</style>
