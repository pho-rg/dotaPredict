<template>
  <div class="draft-prediction-container">
    <div class="content-grow">
      <HeaderBar v-if="isTallEnough" />

      <div v-if="isTallEnough" class="menu-btn">
        <v-btn color="#912728" flat @click="handleMenu">
          <div class="menu-btn-content">
            <v-icon icon="mdi-keyboard-return" size="24" />
            <span>Return to menu</span>
          </div>
        </v-btn>
      </div>

      <span class="title"><v-icon icon="mdi-information-outline" size="38" />Add / Edit heroes in the draft to update the AI prediction</span>

      <div v-if="heroSelection" class="hero-selection-overlay">
        <HeroSelection
          :select-hero="(id) => selectHero(id)"
          :selected-heroes="selectedHeroes"
          @close="heroSelection = false"
        />
      </div>

    </div>

    <div class="reset-btns">
      <v-btn color="#912728" flat @click="()=>resetTeamPicks(0)">
        <div class="menu-btn-content">
          <v-icon icon="mdi-sync" size="22" />
          <span>Reset</span>
        </div>
      </v-btn>
      <v-btn color="#912728" flat @click="()=>resetTeamPicks(1)">
        <div class="menu-btn-content">
          <v-icon icon="mdi-sync" size="22" />
          <span>Reset</span>
        </div>
      </v-btn>
    </div>

    <div class="draftbar-container">
      <DraftBar
        v-if="isWideEnough"
        :dire-bans="draftBarData.direBans"
        :dire-picks="draftBarData.direPicks"
        :dire-team="draftBarData.direTeam"
        :no-bans="draftBarData.noBans"
        :on-click="draftBarData.onClick"
        :radiant-bans="draftBarData.radiantBans"
        :radiant-picks="draftBarData.radiantPicks"
        :radiant-team="draftBarData.radiantTeam"
        :radiant-win-chance="draftBarData.radiantWinChance"
      />
      <div v-else class="draftbar-warning">
        <v-icon class="mr-4" icon="mdi-monitor-screenshot" size="36" />
        <span>Please enlarge the window to view the draft.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, onMounted, onUnmounted, ref } from 'vue'
  import HeaderBar from '@/components/HeaderBar.vue'
  import router from '../router/index.js'
  import DraftBar from '/src/components/DraftBar.vue'

  const isWideEnough = ref(window.innerWidth >= 1024)
  const isTallEnough = ref(window.innerHeight >= 500)

  const heroSelection = ref(false)
  const selectedSlot = ref({ team: 0, position: 0 })

  const showHeroSelection = (team, position) => {
    if (heroSelection.value === false) {
      heroSelection.value = true
      selectedSlot.value = { team: team, position: position }
    }
  }

  const selectHero = async id => {
    const teams = { 0: draftBarData.value.radiantPicks, 1: draftBarData.value.direPicks }
    teams[selectedSlot.value.team][selectedSlot.value.position] = id
    heroSelection.value = false
    selectedSlot.value = { team: 0, position: 0 }
    await updatePrediction(teams[0], teams[1])
  }

  const resetTeamPicks = async teamId => {
    const teams = { 0: draftBarData.value.radiantPicks, 1: draftBarData.value.direPicks }
    for (let i = 0; i < teams[teamId].length; i++) {
      teams[teamId][i] = -2
    }
    await updatePrediction(teams[0], teams[1])
  }

  const updatePrediction = async (radiantPicks, direPicks) => {
    // call api to predict with ai model
    draftBarData.value.radiantWinChance = Math.floor(Math.random() * 100) + 1 // TEMPORARY
  }

  const draftBarData = ref({
    radiantPicks: [-2, -2, -2, -2, -2],
    radiantBans: [0, 0, 0, 0, 0, 0, 0],
    direPicks: [-2, -2, -2, -2, -2],
    direBans: [0, 0, 0, 0, 0, 0, 0],
    radiantWinChance: 50,
    radiantTeam: '',
    direTeam: '',
    noBans: true,
    onClick: (team, position) => showHeroSelection(team, position),
  })

  const selectedHeroes = computed(() => {
    return draftBarData.value.radiantPicks.concat(draftBarData.value.direPicks)
  })

  const updateWindowSize = () => {
    isWideEnough.value = window.innerWidth >= 1024
    isTallEnough.value = window.innerHeight >= 500
  }

  const handleMenu = () => {
    router.push('/menu')
  }

  onMounted(async () => {
    window.addEventListener('resize', updateWindowSize)
    updateWindowSize ()
  })

  onUnmounted(() => {
    window.removeEventListener('resize', updateWindowSize)
  })

</script>

<style scoped>
.draft-prediction-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  height: 100%;
}

.content-grow {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.draftbar-warning {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-block: 7%;
  padding-inline: 16px;
  font-size: 16px;
  font-weight: 500;
  color: #888;
  text-align: center;
  border: 3px dashed #888;
}

.menu-btn-content {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Mohave', sans-serif;
  font-size: 16px;
}

.menu-btn {
  margin-left: 1.5%;
}

.hero-selection-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 999;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.title{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Mohave', sans-serif;
  font-size: 28px;
  text-align: center;
  gap: 20px;
}

.reset-btns{
  padding-inline: 3%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
</style>
