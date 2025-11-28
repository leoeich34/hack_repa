import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const token = ref(localStorage.getItem('token') || '');
  const router = useRouter();

  const setAuth = (userData: any, tokenData: string) => {
    user.value = userData;
    token.value = tokenData;
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', tokenData);
  };

  const login = async (creds: any) => {
    const { data } = await axios.post('http://localhost:3000/api/auth/login', creds);
    setAuth(data.user, data.token);
  };

  const register = async (creds: any) => {
    const { data } = await axios.post('http://localhost:3000/api/auth/register', creds);
    setAuth(data.user, data.token);
  };

  const logout = () => {
    user.value = null;
    token.value = '';
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    window.location.href = '/welcome'; // Жесткий редирект
  };

  const updateUserData = async (data: { name: string, position: string, department: string }) => {
    // Отправляем запрос с токеном
    const response = await axios.put('http://localhost:3000/api/users/me', data, {
      headers: { Authorization: `Bearer ${token.value}` }
    });

    // Обновляем локальное состояние
    user.value = response.data.user;
    localStorage.setItem('user', JSON.stringify(user.value));
  };

  return { user, token, login, register, logout, updateUserData };

});