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
          <v-icon icon="mdi-logout" size="24" class="logout-icon" />
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
  flex-direction: row;
  align-items: center;
  padding-inline: 1.5%;
}

.right-align {
  text-align: right;
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: end;
}

.title {
  font-size: 40px;
  font-family: 'Mohave', sans-serif;
  font-weight: bold;
}

.username {
  font-size: 24px;
  font-family: 'Mohave', sans-serif;
  font-weight: bold;
}

.logout-btn {
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

.logout-icon {
  width: 20px;
  height: 20px;
}
</style>
