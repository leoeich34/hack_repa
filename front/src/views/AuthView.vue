<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import DynamicBackground from '../components/ui/DynamicBackground.vue'
import { useNotification } from '../composables/useNotification'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Режим: login или register
const isLogin = ref(route.query.mode !== 'register')
const form = ref({ email: '', password: '', name: '' })
const loading = ref(false)
const error = ref('')
const { show } = useNotification()

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
}

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    if (isLogin.value) {
      await authStore.login({ email: form.value.email, password: form.value.password })
      show('Добро пожаловать в мир технологий', 'success')
    } else {
      await authStore.register(form.value)
      show('Аккаунт успешно создан', 'success')
    }

    // Небольшая задержка перед переходом, чтобы юзер увидел галочку (опционально)
    setTimeout(() => {
        router.push('/')
    }, 500)

  } catch (e: any) {
    error.value = e.response?.data?.message || 'Ошибка сервера'
    // Можно и ошибку показать красиво
    show(error.value, 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden">
    <DynamicBackground />

    <div class="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-full max-w-md border border-white relative z-10 animate-fade-in-up">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-[#0B1F35] mb-2">
          {{ isLogin ? 'Вход в систему' : 'Регистрация' }}
        </h2>
        <p class="text-gray-500 text-sm">Alfa AI Scoring System</p>
      </div>

      <form @submit.prevent="submit" class="space-y-4">
        <div v-if="!isLogin">
           <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
           <input v-model="form.name" type="text" required class="w-full px-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:border-[#EF3124] focus:ring-2 focus:ring-red-100 outline-none transition">
        </div>

        <div>
           <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
           <input v-model="form.email" type="email" required class="w-full px-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:border-[#EF3124] focus:ring-2 focus:ring-red-100 outline-none transition">
        </div>

        <div>
           <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
           <input v-model="form.password" type="password" required class="w-full px-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:border-[#EF3124] focus:ring-2 focus:ring-red-100 outline-none transition">
        </div>

        <div v-if="error" class="text-red-500 text-sm text-center bg-red-50 p-2 rounded-lg">
            {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-4 bg-[#EF3124] text-white font-bold rounded-xl hover:bg-[#D92D20] transition shadow-lg shadow-red-500/30 flex justify-center"
        >
          <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
          <span v-else>{{ isLogin ? 'Войти' : 'Создать аккаунт' }}</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <button @click="toggleMode" class="text-sm text-gray-500 hover:text-[#EF3124] underline">
          {{ isLogin ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти' }}
        </button>
      </div>
    </div>
  </div>
</template>