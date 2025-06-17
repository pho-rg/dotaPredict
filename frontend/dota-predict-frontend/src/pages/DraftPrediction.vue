<template>
  <div class="draft-prediction-container">
    <div class="content-grow">
      <HeaderBar v-if="isTallEnough && !twitchFullscreen" />

      <div v-if="isTallEnough && !twitchFullscreen" class="menu-btn">
        <v-btn color="#912728" flat @click="handleMenu">
          <div class="menu-btn-content">
            <v-icon icon="mdi-keyboard-return" size="24" />
            <span>Return to menu</span>
          </div>
        </v-btn>
      </div>

      <div v-if="isTallEnough" class="twitch-embed">
        <div v-if="!iframeSrc" class="livestream-integration">
          <span class="twitch-embed-title">IMPORT TWITCH LIVESTREAM</span>
          <div class="livestream-inputs">
            <input
              v-model="twitchUrl"
              placeholder="Enter the Twitch stream URL..."
              type="text"
            >
            <v-btn class="play-btn" color="#912728" flat @click="loadTwitchStream">
              <v-icon class="play-icon" icon="mdi-play" size="24" />
            </v-btn>
          </div>
        </div>

        <div v-if="iframeSrc" class="twitch-iframe-wrapper">
          <v-btn
            class="close-btn"
            color="#912728"
            flat
            @click="closeTwitchStream"
          >
            <v-icon class="btn-icon" icon="mdi-close" size="24" />
          </v-btn>

          <v-btn
            class="fullscreen-btn"
            color="#912728"
            flat
            @click="handleStreamFullscreen"
          >
            <v-icon class="fullscreen-icon" :icon="twitchFullscreen === true ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'" size="24" />
          </v-btn>

          <iframe
            allowfullscreen
            class="iframe"
            frameborder="0"
            :src="iframeSrc"
          />
        </div>
      </div>
    </div>

    <div class="draftbar-container">
      <DraftBar
        v-if="isWideEnough"
        :dire-bans="draftBarData.direBans"
        :dire-picks="draftBarData.direPicks"
        :dire-team="draftBarData.direTeam"
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
  import { onMounted, onUnmounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import HeaderBar from '@/components/HeaderBar.vue'
  import router from '../router/index.js'
  import { getOneMatch } from '../service/matchService.js'
  import { generateDraftBarData } from '../utils/match.js'
  import DraftBar from '/src/components/DraftBar.vue'

  const route = useRoute()

  const isWideEnough = ref(window.innerWidth >= 1024)
  const isTallEnough = ref(window.innerHeight >= 500)

  let intervalId = null

  const draftBarData = ref({
    radiantPicks: [-1, -1, -1, -1, -1],
    radiantBans: [0, 0, 0, 0, 0, 0, 0],
    direPicks: [-1, -1, -1, -1, -1],
    direBans: [0, 0, 0, 0, 0, 0, 0],
    radiantWinChance: 50,
    radiantTeam: '',
    direTeam: '',
  })

  const updateWindowSize = () => {
    isWideEnough.value = window.innerWidth >= 1024
    isTallEnough.value = window.innerHeight >= 500
  }

  const handleMenu = () => {
    router.push('/menu')
  }

  const fetchMatchData = async () => {
    const matchId = route.params.matchId
    const matchData = await getOneMatch(matchId)
    draftBarData.value = generateDraftBarData(matchData)
    if (!matchData.draft_in_progress && intervalId) { // stop updating if draft is done
      clearInterval(intervalId)
    }
  }

  onMounted(async () => {
    window.addEventListener('resize', updateWindowSize)
    updateWindowSize ()
    await fetchMatchData()
    intervalId = setInterval(fetchMatchData, 2000) // update match data every 2s
  })

  onUnmounted(() => {
    window.removeEventListener('resize', updateWindowSize)
    if (intervalId) clearInterval(intervalId)
  })

  const twitchUrl = ref('')
  const iframeSrc = ref('')
  const twitchFullscreen = ref(false)

  const loadTwitchStream = () => {
    const match = twitchUrl.value.match(/twitch\.tv\/([^/?]+)/)
    if (match && match[1]) {
      const channelName = match[1]
      iframeSrc.value = `https://player.twitch.tv/?channel=${channelName}&parent=${window.location.hostname}`
    } else {
      alert('Invalid Twitch URL')
    }
  }

  const closeTwitchStream = () => {
    iframeSrc.value = ''
    twitchFullscreen.value = false
  }

  const handleStreamFullscreen = () => {
    twitchFullscreen.value = !twitchFullscreen.value
  }

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

.twitch-embed {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-block: 20px;
}

.twitch-embed-title{
  font-family: 'Mohave', sans-serif;
  font-size: 28px;
  margin-bottom: 15px;
}

.livestream-integration {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.livestream-inputs{
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
}

.twitch-iframe-wrapper {
  height: 100%;
  position: relative;
}

input {
  padding: 0.75rem;
  border-radius: 10px;
  border: none;
  outline: none;
  font-size: 18px;
  background-color: #727272;
  color: white;
  min-width: 30vw;
  font-family: 'Mohave', sans-serif;
}

input::placeholder {
  color: white;
  opacity: 1;
}

.play-btn {
  min-width: 50px;
  height: 50px;
  width: 50px;
  margin-left: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.iframe{
  min-width: 50vw;
  height: 100%;
  border: 2px solid #912728
}
.close-btn, .fullscreen-btn {
  position: absolute;
  right: -18px;
  z-index: 2;
  min-width: 40px;
  height: 40px;
  width: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
}

.close-btn {
  top: -15px;
}

.fullscreen-btn {
  top: 35px;
}
</style>
