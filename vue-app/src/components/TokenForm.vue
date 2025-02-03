<template>
  <div>
    <h1>Вход</h1>
    <form @submit.prevent="getToken">
      <div>
        <label for="username">Ваш Oid:</label>
        <input id="username" v-model="username" type="text" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input id="password" v-model="password" type="password" required />
      </div>
      <button type="submit">Получить токен</button>
    </form>
    <div v-if="token">
      <h2>Ваш токен:</h2>
      <p>{{ token }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      token: ''
    };
  },
  methods: {
    async getToken() {
      try {
        const params = new URLSearchParams();
        params.append('grant_type', 'password');
        params.append('username', this.username);
        params.append('password', this.password);
        params.append('scope', '');
        params.append('client_id', 'string');
        params.append('client_secret', 'string');

        const response = await axios.post('http://localhost:8001/api/token', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
          }
        });

        // Сохраняем токен в state приложения
        this.token = response.data.access_token;

        // Сохраняем токен в cookie
        document.cookie = `access_token=${this.token}; path=/; max-age=3600`; // expires in 1 hour

        // Сохраняем токен в sessionStorage
        sessionStorage.setItem('access_token', this.token);

        console.log('Токен сохранен в cookie и sessionStorage:', this.token);
      } catch (error) {
        console.error('Ошибка при получении токена:', error);
      }
    }
  }
};
</script>

<style scoped>
form {
  margin-bottom: 20px;
}
</style>
