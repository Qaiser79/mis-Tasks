<template>
  <div class="login-wrapper">
    <div class="login-card">
      <i class="fas fa-user-circle login-icon"></i>
      <h2 class="login-title">Welcome Back</h2>
      <form @submit.prevent="submitLogin" class="login-form">
        <input
          v-model="username"
          placeholder="Username"
          class="login-input"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="login-input"
        />
        <button type="submit" class="login-button">Login</button>
        <p v-if="error" class="login-error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    submitLogin() {
      axios.post('http://127.0.0.1:8000/login', {
        username: this.username,
        password: this.password
      })
      .then(res => {
        localStorage.setItem('currentUser', JSON.stringify(res.data))
        const role = res.data.role
        if (role === 'admin') {
            this.$router.push('/dashboard')
          } else {
            this.$router.push('/editor-dashboard')
          }
      })
      .catch(() => {
        this.error = 'Invalid credentials'
      })
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to right, #f0f4f8, #d9e2ec);
}

.login-card {
  background-color: #ffffff;
  padding: 2rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-icon {
  font-size: 3rem;
  color: #007bff;
  display: block;
  text-align: center;
  margin-bottom: 1rem;
}

.login-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.login-input {
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.login-input:focus {
  border-color: #007bff;
  outline: none;
}

.login-button {
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #0056b3;
}

.login-error {
  margin-top: 1rem;
  color: #d9534f;
  text-align: center;
}

</style>