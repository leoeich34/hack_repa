<script setup lang="ts">
import { ref } from 'vue'
import { useSettingsStore } from '../store/settings' // <-- Подключаем стор
import { useNotification } from '../composables/useNotification'
import {
  ComputerDesktopIcon,
  BellIcon,
  ShieldCheckIcon,
  ArrowPathIcon,
  MoonIcon,
  SunIcon
} from '@heroicons/vue/24/outline'

const settingsStore = useSettingsStore()
const { show } = useNotification()
const loading = ref(false)

// Сохранение (теперь это скорее имитация, т.к. Pinia сохраняет мгновенно)
const saveSettings = async () => {
  loading.value = true
  setTimeout(() => {
    show('Настройки успешно применены', 'success')
    loading.value = false
  }, 600)
}

const clearCache = () => {
  localStorage.clear()
  window.location.reload()
}
</script>

<template>
  <div class="animate-fade-in-up max-w-5xl mx-auto pb-10">

    <div class="mb-8">
      <h1 class="text-3xl font-bold text-[#0B1F35] dark:text-white">Настройки системы</h1>
      <p class="text-gray-500 mt-1">Персонализация интерфейса и параметры безопасности</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-6">

      <!-- ЛЕВАЯ КОЛОНКА -->
      <div class="md:col-span-8 space-y-6">

        <!-- Секция 1: Интерфейс -->
        <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm dark:bg-white/5 dark:border-gray-700">
           <h2 class="text-lg font-bold text-[#0B1F35] flex items-center gap-2 mb-4 dark:text-white">
              <ComputerDesktopIcon class="w-5 h-5 text-[#EF3124]" />
              Внешний вид
           </h2>

           <div class="space-y-4">
              <!-- ТЕМА -->
              <div class="flex items-center justify-between p-3 bg-white/50 rounded-xl border border-gray-100 dark:bg-gray-900/50 dark:border-gray-700">
                 <div class="flex items-center gap-3">
                    <div class="p-2 bg-gray-100 rounded-lg dark:bg-gray-800">
                       <SunIcon v-if="settingsStore.theme === 'light'" class="w-5 h-5 text-orange-500" />
                       <MoonIcon v-else class="w-5 h-5 text-indigo-400" />
                    </div>
                    <div>
                       <div class="font-medium text-[#0B1F35] dark:text-gray-200">Тема оформления</div>
                       <div class="text-xs text-gray-500">
                         {{ settingsStore.theme === 'light' ? 'Светлая тема' : 'Темная тема' }}
                       </div>
                    </div>
                 </div>

                 <!-- Реальный переключатель темы -->
                 <div class="flex bg-gray-200 p-1 rounded-lg cursor-pointer dark:bg-gray-700" @click="settingsStore.toggleTheme">
                    <button
                      class="px-3 py-1 rounded-md text-xs font-bold transition-all"
                      :class="settingsStore.theme === 'light' ? 'bg-white shadow-sm text-gray-800' : 'text-gray-500'"
                    >Light</button>
                    <button
                      class="px-3 py-1 rounded-md text-xs font-bold transition-all"
                      :class="settingsStore.theme === 'dark' ? 'bg-gray-600 shadow-sm text-white' : 'text-gray-500'"
                    >Dark</button>
                 </div>
              </div>

              <!-- КОМПАКТНЫЙ РЕЖИМ -->
              <div class="flex items-center justify-between p-3 bg-white/50 rounded-xl border border-gray-100 dark:bg-gray-900/50 dark:border-gray-700">
                 <div>
                    <div class="font-medium text-[#0B1F35] dark:text-gray-200">Компактный режим</div>
                    <div class="text-xs text-gray-500">Уменьшить отступы в интерфейсе</div>
                 </div>
                 <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" :checked="settingsStore.compactMode" @change="settingsStore.toggleCompact" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#EF3124]"></div>
                 </label>
              </div>
           </div>
        </div>

        <!-- Секция 2: Уведомления -->
        <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm dark:bg-white/5 dark:border-gray-700">
           <h2 class="text-lg font-bold text-[#0B1F35] flex items-center gap-2 mb-4 dark:text-white">
              <BellIcon class="w-5 h-5 text-[#EF3124]" />
              Уведомления
           </h2>

           <div class="space-y-4 divide-y divide-gray-100 dark:divide-gray-700">
              <div class="flex items-center justify-between py-2">
                 <span class="text-gray-700 dark:text-gray-300">Email рассылка</span>
                 <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="settingsStore.notifications.email" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#EF3124]"></div>
                 </label>
              </div>
              <div class="flex items-center justify-between py-2">
                 <span class="text-gray-700 dark:text-gray-300">Push-уведомления</span>
                 <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="settingsStore.notifications.push" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#EF3124]"></div>
                 </label>
              </div>
           </div>
        </div>

      </div>

      <!-- ПРАВАЯ КОЛОНКА -->
      <div class="md:col-span-4 space-y-6">

        <!-- Безопасность -->
        <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm dark:bg-white/5 dark:border-gray-700">
           <h2 class="text-lg font-bold text-[#0B1F35] flex items-center gap-2 mb-4 dark:text-white">
              <ShieldCheckIcon class="w-5 h-5 text-[#EF3124]" />
              Безопасность
           </h2>

           <form @submit.prevent class="space-y-3">
              <div>
                <label class="text-xs text-gray-500 font-medium">Новый пароль</label>
                <input type="password" class="w-full px-3 py-2 bg-white/50 border border-gray-200 rounded-lg text-sm focus:border-[#EF3124] outline-none dark:bg-gray-900/50 dark:border-gray-600 dark:text-white">
              </div>
              <button class="w-full py-2 bg-gray-100 text-gray-600 text-sm font-bold rounded-lg hover:bg-gray-200 transition dark:bg-gray-700 dark:text-gray-200">
                Обновить пароль
              </button>
           </form>

           <div class="mt-6 pt-4 border-t border-gray-100 dark:border-gray-700">
              <div class="flex items-center justify-between mb-2">
                 <span class="text-sm font-medium dark:text-gray-200">2FA Авторизация</span>
                 <input type="checkbox" checked class="accent-[#EF3124] w-4 h-4">
              </div>
              <p class="text-xs text-gray-400">Требовать код из SMS</p>
           </div>
        </div>

        <!-- Система -->
        <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm dark:bg-white/5 dark:border-gray-700">
            <h2 class="text-lg font-bold text-[#0B1F35] mb-4 dark:text-white">Система</h2>
            <button
              @click="clearCache"
              class="w-full py-2 flex items-center justify-center gap-2 border border-gray-300 rounded-xl text-gray-600 hover:bg-white hover:text-[#EF3124] hover:border-[#EF3124] transition text-sm font-medium dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
            >
              <ArrowPathIcon class="w-4 h-4" />
              Очистить кэш
            </button>
            <div class="text-center mt-3 text-xs text-gray-400">
               Версия: v2.0.4 (Beta)
            </div>
        </div>

      </div>
    </div>

    <!-- Кнопка сохранения -->
    <div class="flex justify-end mt-8">
       <button
         @click="saveSettings"
         :disabled="loading"
         class="bg-[#0B1F35] text-white px-8 py-3 rounded-xl font-bold shadow-xl hover:bg-black transition flex items-center gap-2 hover:scale-105 active:scale-95 dark:bg-[#EF3124]"
       >
         <span v-if="loading" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
         <span v-else>Сохранить изменения</span>
       </button>
    </div>

  </div>
</template>