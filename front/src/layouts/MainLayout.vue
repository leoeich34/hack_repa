<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSettingsStore } from '../store/settings'
import { useAuthStore } from '../store/auth'
import DynamicBackground from '../components/ui/DynamicBackground.vue'
import Floating3DObjects from '../components/ui/Floating3DObjects.vue'
import {
  MagnifyingGlassIcon,
  UserGroupIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const settingsStore = useSettingsStore()
const authStore = useAuthStore()

// ЛОГИКА ДИНАМИЧЕСКОГО САЙДБАРА
const isHovered = ref(false)
const isPinned = ref(true) // По умолчанию закреплен

// Меню раскрыто, если мышь наведена ИЛИ нажата кнопка "Закрепить"
const isExpanded = computed(() => isHovered.value || isPinned.value)

const togglePin = () => {
  isPinned.value = !isPinned.value
}

const goToProfile = () => {
  router.push('/profile')
}

const menuItems = [
  { name: 'Поиск клиента', path: '/', icon: MagnifyingGlassIcon },
  { name: 'База клиентов', path: '/clients', icon: UserGroupIcon },
  { name: 'Аналитика', path: '/analytics', icon: ChartBarIcon },
  { name: 'Настройки', path: '/settings', icon: Cog6ToothIcon },
]
</script>

<template>
  <div class="flex h-screen font-sans overflow-hidden bg-transparent transition-colors duration-300">

    <DynamicBackground />
    <Floating3DObjects />

    <!-- SIDEBAR -->
    <aside
      @mouseenter="isHovered = true"
      @mouseleave="isHovered = false"
      class="bg-white/80 backdrop-blur-md border-r border-white/40 flex flex-col transition-all duration-300 relative z-50 shadow-2xl dark:bg-[#0B1F35]/90 dark:border-white/10"
      :class="isExpanded ? 'w-64' : 'w-20'"
    >

      <!-- ЛОГОТИП -->
      <div class="h-20 flex items-center px-5 border-b border-gray-100/50 dark:border-white/10 relative overflow-hidden whitespace-nowrap">

        <!-- Иконка (всегда видна) -->
        <div class="w-10 h-10 bg-[#EF3124] rounded-lg flex items-center justify-center text-white shadow-lg shadow-red-500/30 shrink-0 relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-tr from-black/10 to-transparent"></div>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="relative z-10">
                <path d="M12 2L4 22H8L10 17H14L16 22H20L12 2ZM11 14L12 11L13 14H11Z" fill="white"/>
                <rect x="5" y="23" width="14" height="2" fill="white"/>
            </svg>
        </div>

        <!-- Текст (виден только при раскрытии) -->
        <div class="ml-3 transition-opacity duration-300" :class="isExpanded ? 'opacity-100' : 'opacity-0 w-0'">
          <div class="font-bold text-[#0B1F35] tracking-wide text-lg leading-none dark:text-white">Alfa</div>
          <div class="text-[10px] text-[#EF3124] uppercase tracking-[0.2em] font-bold mt-1">HORIZON</div>
        </div>

        <!-- Кнопка ЗАКРЕПЛЕНИЯ (Видна только когда меню раскрыто) -->
        <button
          v-if="isExpanded"
          @click.stop="togglePin"
          class="absolute right-4 p-1 rounded-md text-gray-400 hover:text-[#EF3124] hover:bg-black/5 dark:hover:bg-white/10 transition"
          :title="isPinned ? 'Открепить меню' : 'Закрепить меню'"
        >
           <ChevronDoubleLeftIcon v-if="isPinned" class="w-4 h-4" />
           <div v-else class="w-2 h-2 rounded-full bg-gray-400 group-hover:bg-[#EF3124]"></div> <!-- Точка, если не закреплено -->
        </button>
      </div>

      <!-- МЕНЮ -->
      <nav class="flex-1 py-6 space-y-2 px-3 overflow-x-hidden">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.path"
          class="flex items-center gap-3 rounded-xl transition-all duration-200 group relative overflow-hidden whitespace-nowrap"
          :class="[
            settingsStore.compactMode ? 'py-2' : 'py-3',
            isExpanded ? 'px-3' : 'justify-center px-0', // Центрируем иконку если свернуто

            route.path === item.path
              ? 'bg-[#0B1F35] text-white shadow-lg shadow-blue-900/20 dark:bg-[#EF3124] dark:shadow-red-900/40'
              : 'text-gray-600 hover:bg-red-50 hover:text-[#EF3124] dark:text-gray-300 dark:hover:bg-white/10 dark:hover:text-white'
          ]"
        >
          <component :is="item.icon" class="w-6 h-6 shrink-0" :title="!isExpanded ? item.name : ''" />

          <span
            class="font-medium transition-opacity duration-200"
            :class="isExpanded ? 'opacity-100' : 'opacity-0 w-0 hidden'"
          >
            {{ item.name }}
          </span>

          <!-- Полоска активного элемента -->
          <div v-if="route.path === item.path" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-[#EF3124] rounded-r-full dark:bg-white"></div>
        </router-link>
      </nav>

      <!-- ПРОФИЛЬ -->
      <div class="p-4 border-t border-gray-100/50 dark:border-white/10 overflow-hidden">
        <div
          @click="goToProfile"
          class="flex items-center gap-3 p-2 rounded-xl hover:bg-white/50 transition-colors cursor-pointer group select-none overflow-hidden dark:hover:bg-white/10"
          :class="!isExpanded ? 'justify-center' : ''"
        >
          <!-- Аватар -->
          <div class="w-10 h-10 rounded-full bg-[#0B1F35] text-white flex items-center justify-center font-bold shrink-0 text-sm dark:bg-white dark:text-[#0B1F35] relative">
             {{ authStore.user?.name?.[0]?.toUpperCase() || 'U' }}

             <!-- Индикатор онлайн (если свернуто) -->
             <div v-if="!isExpanded" class="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full"></div>
          </div>

          <!-- Текст + Кнопка выхода (Скрываем при сворачивании) -->
          <div class="flex items-center justify-between flex-1 min-w-0 transition-opacity duration-200"
               :class="isExpanded ? 'opacity-100' : 'opacity-0 w-0 hidden'">

             <div class="flex flex-col min-w-0">
                <div class="text-sm font-bold text-[#0B1F35] truncate w-24 dark:text-white" :title="authStore.user?.name">
                  {{ authStore.user?.name || 'User' }}
                </div>
                <div class="text-xs text-gray-500 truncate w-24 dark:text-gray-400">
                  {{ authStore.user?.position || 'Сотрудник' }}
                </div>
             </div>

             <button
                @click.stop="authStore.logout"
                class="p-1.5 text-gray-400 hover:text-[#EF3124] hover:bg-red-50 rounded-lg transition shrink-0 dark:hover:bg-white/20 dark:hover:text-white"
                title="Выйти"
             >
                <ArrowRightOnRectangleIcon class="w-5 h-5" />
             </button>
          </div>
        </div>
      </div>

    </aside>

    <!-- CONTENT -->
    <main class="flex-1 overflow-auto relative z-10">
      <div class="max-w-7xl mx-auto p-6 lg:p-10">
        <slot />
      </div>
    </main>
  </div>
</template>