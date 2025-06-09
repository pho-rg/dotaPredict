<template>
  <div class="draft-prediction-container">
    <div class="content-grow">
      <HeaderBar />
    </div>

    <div class="draftbar-container">
        <DraftBar
        v-if="isWideEnough"
        :radiantPicks="[2, 6, 12, -1, null]"
        :radiantBans="[1, 5, 7, null, null, null, null]"
        :direPicks="[16, 25, 9, 31, null]"
        :direBans="[14, 3, 28, 23, 11, null, null]"
        :radiantWinChance="57.3"
        radiantTeam="Lyon Demons"
        direTeam="STe ESPORT"
        />
        <div v-else class="draftbar-warning">
            <v-icon icon="mdi-monitor-screenshot" size="36" class="mr-4" />
            <span>Please enlarge the window to view the draft.</span>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import DraftBar from '/src/components/DraftBar.vue'
import HeaderBar from "@/components/HeaderBar.vue";

const isWideEnough = ref(window.innerWidth >= 1024)

const updateWidth = () => {
  isWideEnough.value = window.innerWidth >= 1024
}

onMounted(() => {
  window.addEventListener('resize', updateWidth)
  updateWidth()
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWidth)
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
</style>
