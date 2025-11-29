<script setup lang="ts">
import { ref } from 'vue'
import { useSettingsStore } from '../store/settings'
import { useNotification } from '../composables/useNotification'
import {
  ComputerDesktopIcon, BellIcon, ShieldCheckIcon,
  ArrowPathIcon, MoonIcon, SunIcon, SwatchIcon
} from '@heroicons/vue/24/outline'

const settingsStore = useSettingsStore()
const { show } = useNotification()
const loading = ref(false)

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
  <div class="animate-fade-in-up max-w-4xl mx-auto pb-10">

    <div class="mb-10">
      <h1 class="text-3xl font-bold text-[#0B1F35] dark:text-white">Настройки</h1>
      <p class="text-gray-500 mt-1 dark:text-gray-400">Персонализация и безопасность</p>
    </div>

    <!-- MAIN GRID -->
    <div class="space-y-6">

      <!-- SECTION 1: APPEARANCE -->
      <div class="bg-white/70 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm dark:bg-white/5 dark:border-white/10">
         <div class="flex items-center gap-3 mb-6">
            <div class="p-2 bg-blue-50 text-blue-600 rounded-xl dark:bg-blue-900/30 dark:text-blue-400"><SwatchIcon class="w-6 h-6" /></div>
            <h2 class="text-xl font-bold text-[#0B1F35] dark:text-white">Внешний вид</h2>
         </div>

         <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Theme Card -->
            <div class="p-4 rounded-2xl border border-gray-100 dark:border-white/5 bg-white/50 dark:bg-white/5 flex justify-between items-center cursor-pointer transition hover:border-gray-300 dark:hover:border-white/20"
                 @click="settingsStore.toggleTheme">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center transition-colors"
                         :class="settingsStore.theme === 'light' ? 'bg-orange-100 text-orange-500' : 'bg-gray-700 text-gray-400'">
                        <SunIcon class="w-6 h-6" />
                    </div>
                    <div>
                        <div class="font-bold text-[#0B1F35] dark:text-white">Светлая</div>
                        <div class="text-xs text-gray-500 dark:text-gray-400">Классический вид</div>
                    </div>
                </div>
                <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                     :class="settingsStore.theme === 'light' ? 'border-[#EF3124] bg-[#EF3124]' : 'border-gray-300 dark:border-gray-600'">
                     <div v-if="settingsStore.theme === 'light'" class="w-2 h-2 bg-white rounded-full"></div>
                </div>
            </div>

            <!-- Dark Theme Card -->
            <div class="p-4 rounded-2xl border border-gray-100 dark:border-white/5 bg-white/50 dark:bg-white/5 flex justify-between items-center cursor-pointer transition hover:border-gray-300 dark:hover:border-white/20"
                 @click="settingsStore.toggleTheme">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center transition-colors"
                         :class="settingsStore.theme === 'dark' ? 'bg-indigo-100 text-indigo-500' : 'bg-gray-200 text-gray-400'">
                        <MoonIcon class="w-6 h-6" />
                    </div>
                    <div>
                        <div class="font-bold text-[#0B1F35] dark:text-white">Темная</div>
                        <div class="text-xs text-gray-500 dark:text-gray-400">Для работы ночью</div>
                    </div>
                </div>
                <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                     :class="settingsStore.theme === 'dark' ? 'border-[#EF3124] bg-[#EF3124]' : 'border-gray-300 dark:border-gray-600'">
                     <div v-if="settingsStore.theme === 'dark'" class="w-2 h-2 bg-white rounded-full"></div>
                </div>
            </div>
         </div>

         <div class="mt-6 pt-6 border-t border-gray-100 dark:border-white/10 flex items-center justify-between">
             <div>
                <div class="font-bold text-[#0B1F35] dark:text-white">Компактный режим</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">Уменьшить отступы в таблицах</div>
             </div>
             <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" :checked="settingsStore.compactMode" @change="settingsStore.toggleCompact" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#EF3124] dark:bg-gray-700"></div>
             </label>
         </div>
      </div>

      <!-- SECTION 2: NOTIFICATIONS -->
      <div class="bg-white/70 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm dark:bg-white/5 dark:border-white/10">
         <div class="flex items-center gap-3 mb-6">
            <div class="p-2 bg-purple-50 text-purple-600 rounded-xl dark:bg-purple-900/30 dark:text-purple-400"><BellIcon class="w-6 h-6" /></div>
            <h2 class="text-xl font-bold text-[#0B1F35] dark:text-white">Уведомления</h2>
         </div>

         <div class="space-y-4">
            <div class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition dark:hover:bg-white/5">
                <span class="text-gray-700 font-medium dark:text-gray-200">Email рассылка</span>
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="settingsStore.notifications.email" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#EF3124] dark:bg-gray-700"></div>
                </label>
            </div>
            <div class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition dark:hover:bg-white/5">
                <span class="text-gray-700 font-medium dark:text-gray-200">Push-уведомления</span>
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="settingsStore.notifications.push" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#EF3124] dark:bg-gray-700"></div>
                </label>
            </div>
         </div>
      </div>

      <!-- SECTION 3: SECURITY & SYSTEM -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white/70 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm dark:bg-white/5 dark:border-white/10">
             <div class="flex items-center gap-3 mb-6">
                <div class="p-2 bg-green-50 text-green-600 rounded-xl dark:bg-green-900/30 dark:text-green-400"><ShieldCheckIcon class="w-6 h-6" /></div>
                <h2 class="text-xl font-bold text-[#0B1F35] dark:text-white">Безопасность</h2>
             </div>
             <div class="space-y-3">
                <button class="w-full py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 font-bold hover:bg-gray-100 transition dark:bg-white/5 dark:border-white/10 dark:text-white dark:hover:bg-white/10">
                    Сменить пароль
                </button>
                <div class="flex items-center justify-between px-2">
                    <span class="text-sm text-gray-500 dark:text-gray-400">2FA Авторизация</span>
                    <span class="text-sm font-bold text-green-600 dark:text-green-400">Активно</span>
                </div>
             </div>
          </div>

          <div class="bg-white/70 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm dark:bg-white/5 dark:border-white/10 flex flex-col justify-between">
             <div class="flex items-center gap-3 mb-4">
                <div class="p-2 bg-gray-100 text-gray-600 rounded-xl dark:bg-gray-700 dark:text-gray-300"><ComputerDesktopIcon class="w-6 h-6" /></div>
                <h2 class="text-xl font-bold text-[#0B1F35] dark:text-white">Система</h2>
             </div>

             <div class="text-center mb-4">
                 <div class="text-sm text-gray-500 dark:text-gray-400">Версия приложения</div>
                 <div class="text-lg font-mono font-bold text-[#0B1F35] dark:text-white">v2.1.0 (Stable)</div>
             </div>

             <button
                @click="clearCache"
                class="w-full py-3 border border-red-200 text-red-600 rounded-xl font-bold hover:bg-red-50 transition flex items-center justify-center gap-2 dark:border-red-900/50 dark:bg-red-900/10 dark:hover:bg-red-900/30"
             >
                <ArrowPathIcon class="w-5 h-5" /> Сбросить кэш
             </button>
          </div>
      </div>

    </div>

    <!-- Floating Save Button -->
    <div class="fixed bottom-8 right-8 z-30">
       <button
         @click="saveSettings"
         :disabled="loading"
         class="bg-[#0B1F35] text-white px-8 py-4 rounded-full font-bold shadow-2xl hover:bg-black transition flex items-center gap-3 hover:scale-105 active:scale-95 dark:bg-white dark:text-[#0B1F35]"
       >
         <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-current border-t-transparent rounded-full"></span>
         <span v-else>Сохранить</span>
       </button>
    </div>

  </div>
</template>