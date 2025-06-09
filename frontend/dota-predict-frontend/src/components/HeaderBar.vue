<template>
  <v-container class="headerbar-container" fluid>
    <v-row align="center" justify="space-between">
      <v-col>
        <div class="title">
          <p>DOTAPREDICT</p>
        </div>
      </v-col>
      <v-col class="right-align">
        <span class="username">{{ userName }}</span>
        <v-btn class="logout-btn" color="#912728" flat @click="handleLogout">
          <img class="logout-icon" src="../assets/logout-icon.png" />
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
  import { onMounted, ref } from 'vue'
  import router from '../router/index.js'
  import { getUsername } from '../service/authService.js'
  import { logout } from '../utils/auth.js'

  const userName = ref('')

  const fetchUserName = async () => {
    try {
      const data = await getUsername()
      userName.value = data.name
    } catch (error) {
      console.error('Failed to retrieve username', error)
    }
  }

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  onMounted(fetchUserName)
</script>
<style scoped>
.headerbar-container {
  display: flex;
}

.right-align {
  text-align: right;
}

.title {
  font-size: 40px;
  font-family: 'Mohave', sans-serif;
  font-weight: bold;
}

.username {
  font-size: 20px;
  font-family: 'Mohave', sans-serif;
  font-weight: bold;
}

.logout-btn {
  min-width: auto;
  bottom: 4px;
  margin-left: 15px;
  border-radius: 50%;
}

.logout-icon {
  width: 15px;
  height: 15px;
}
</style>
