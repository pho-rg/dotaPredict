<template>
  <v-container class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2 class="title">Login</h2>

      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        @input="errorMessage = false"
        type="email"
        required
        placeholder="Enter your email"
      />

      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        @input="errorMessage = false"
        type="password"
        required
        placeholder="Enter your password"
      />

      <v-alert
        v-if="errorMessage"
        color=#994848
        icon="$error"
        text="Bad credentials"
        class="mb-1 py-1 px-3"
      ></v-alert>

      <div class="footer">
        <RouterLink to="/register" class="link">Create an account</RouterLink>
        <button type="submit" class="login-button">Login</button>
      </div>
    </form>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../service/authService'

const email = ref('')
const password = ref('')
const errorMessage = ref(false)
const router = useRouter()

const handleLogin = async () => {
  const success = await login({ email: email.value, password: password.value })
  if (success) router.push('/menu')
  else errorMessage.value = true
}
</script>

<style scoped>
.login-container {
  background-color: #404040;
  border-radius: 25px;
  padding: 2rem;
  width: 90%;
  max-width: 400px;
  box-sizing: border-box;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  color: white;
  font-family: 'Mohave', sans-serif;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.title {
  text-align: center;
  margin-bottom: 1rem;
}

input {
  padding: 0.75rem;
  border-radius: 10px;
  border: none;
  outline: none;
  font-size: 1rem;
  background-color: #727272;
  color: white;
}

input::placeholder {
  color: white;
  opacity: 1;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.link {
  color: #bbb;
  font-size: 0.9rem;
  text-decoration: underline;
  cursor: pointer;
}

.login-button {
  background-color: #930c0c;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #1f9535;
}
</style>
