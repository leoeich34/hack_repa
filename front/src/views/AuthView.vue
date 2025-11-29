<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useNotification } from '../composables/useNotification'
import DynamicBackground from '../components/ui/DynamicBackground.vue'
import { ArrowRightIcon } from '@heroicons/vue/24/solid'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { show } = useNotification()

const isLogin = ref(route.query.mode !== 'register')
const form = ref({ email: '', password: '', name: '' })
const loading = ref(false)

const submit = async () => {
  loading.value = true
  try {
    if (isLogin.value) {
      await authStore.login({ email: form.value.email, password: form.value.password })
      show('Добро пожаловать в Horizon', 'success')
    } else {
      await authStore.register(form.value)
      show('Аккаунт успешно создан', 'success')
    }
    setTimeout(() => router.push('/'), 500)
  } catch (e: any) {
    show(e.response?.data?.message || 'Ошибка сервера', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden font-sans text-[#0B1F35] dark:text-white">
    <DynamicBackground />

    <div class="w-full max-w-md p-8 relative z-10 animate-fade-in-up">

      <!-- Лого -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2 font-black text-2xl tracking-tight mb-2">
            <div class="w-10 h-10 bg-gradient-to-br from-[#EF3124] to-[#B91C10] rounded-xl flex items-center justify-center text-white shadow-lg">A</div>
            <span>ALFA <span class="text-[#EF3124]">HORIZON</span></span>
        </div>
        <p class="text-gray-500 dark:text-gray-400">Войдите, чтобы получить доступ к аналитике</p>
      </div>

      <!-- Карточка формы -->
      <div class="bg-white/70 backdrop-blur-xl border border-white/60 p-8 rounded-3xl shadow-2xl dark:bg-[#0B1F35]/60 dark:border-white/10">

        <!-- Табы -->
        <div class="flex p-1 bg-gray-100 rounded-xl mb-6 dark:bg-white/10">
            <button @click="isLogin = true" class="flex-1 py-2 text-sm font-bold rounded-lg transition-all" :class="isLogin ? 'bg-white shadow text-[#0B1F35] dark:bg-[#0B1F35] dark:text-white' : 'text-gray-500 dark:text-gray-400'">Вход</button>
            <button @click="isLogin = false" class="flex-1 py-2 text-sm font-bold rounded-lg transition-all" :class="!isLogin ? 'bg-white shadow text-[#0B1F35] dark:bg-[#0B1F35] dark:text-white' : 'text-gray-500 dark:text-gray-400'">Регистрация</button>
        </div>

        <form @submit.prevent="submit" class="space-y-5">
          <div v-if="!isLogin" class="animate-fade-in">
             <label class="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1 block">Имя сотрудника</label>
             <input v-model="form.name" type="text" required class="input-field" placeholder="Иван Иванов">
          </div>

          <div>
             <label class="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1 block">Email</label>
             <input v-model="form.email" type="email" required class="input-field" placeholder="corp@alfa.ru">
          </div>

          <div>
             <label class="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1 block">Пароль</label>
             <input v-model="form.password" type="password" required class="input-field" placeholder="••••••••">
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-4 bg-[#EF3124] text-white font-bold rounded-xl hover:bg-[#D92D20] transition shadow-lg shadow-red-500/20 flex justify-center items-center gap-2 group mt-4 disabled:opacity-70"
          >
            <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
            <span v-else>{{ isLogin ? 'Войти в систему' : 'Создать аккаунт' }}</span>
            <ArrowRightIcon v-if="!loading" class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </form>
      </div>

      <div class="mt-8 text-center text-xs text-gray-400">
        Protected by Alfa Security Shield
      </div>

    </div>
  </div>
</template>

<style scoped>
.input-field {
    @apply w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:border-[#EF3124] focus:ring-4 focus:ring-red-500/10 outline-none transition font-medium dark:bg-white/5 dark:border-white/10 dark:text-white dark:focus:ring-white/10;
}
</style>