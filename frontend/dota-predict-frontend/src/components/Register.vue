<template>
  <div class="register-box">
    <form @submit.prevent="handleRegister" class="register-form">
      <h2 class="title">Register</h2>

      <label for="name">Name</label>
      <input
        id="name"
        v-model="name"
        @input="errorMessage = ''"
        type="text"
        required
        placeholder="Enter your name"
      />

      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        @input="errorMessage = ''"
        type="email"
        required
        placeholder="Enter your email"
      />

      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        @input="errorMessage = ''"
        type="password"
        required
        placeholder="Enter your password"
      />

      <label for="confirmPassword">Confirm Password</label>
      <input
        id="confirmPassword"
        v-model="confirmPassword"
        @input="errorMessage = ''"
        type="password"
        required
        placeholder="Confirm your password"
      />

      <v-alert
        v-if="errorMessage"
        color="#994848"
        icon="$error"
        :text="errorMessage"
        class="mb-1 py-1 px-3 dense-alert"
        density="compact"
      ></v-alert>

      <div class="footer">
        <RouterLink to="/login" class="link">Already have an account? Login</RouterLink>
        <button type="submit" class="register-button">Register</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../service/authService'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const router = useRouter()

const handleRegister = async () => {
  const formData = {
    name: name.value,
    email: email.value,
    password: password.value,
    confirmPassword: confirmPassword.value,
  }

  try {
    await register(formData)
    router.push('/login')
  } catch (err) {
    const status = err?.response?.status
    const detail = err?.response?.data?.detail
    console.log(status)
    console.log(detail)

    if (status === 412 && detail === 'Passwords do not match.') {
      errorMessage.value = 'Passwords do not match.'
    } else if (status === 400 && detail === 'Email already registered.') {
      errorMessage.value = 'This email is already registered.'
    } else if (status === 400 && detail === 'All fields are required.') {
      errorMessage.value = 'Please fill in all the fields.'
    } else {
      errorMessage.value = detail || 'Unexpected error during registration.'
    }
  }
}
</script>

<style scoped>
.register-box {
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

.register-form {
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

.register-button {
  background-color: #930c0c;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-button:hover {
  background-color: #1F9535FF;
}

.dense-alert {
  font-size: 0.75rem;
  line-height: 1rem;
}

.dense-alert .v-icon {
  font-size: 1rem !important;
}
</style>
