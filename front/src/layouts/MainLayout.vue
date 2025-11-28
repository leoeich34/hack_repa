<script setup lang="ts">
import { useRoute } from 'vue-router'
import DynamicBackground from '../components/ui/DynamicBackground.vue'
import Floating3DObjects from '../components/ui/Floating3DObjects.vue'
import {
  MagnifyingGlassIcon,
  UserGroupIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  BuildingLibraryIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()

const menuItems = [
  { name: 'Поиск клиента', path: '/', icon: MagnifyingGlassIcon },
  { name: 'База клиентов', path: '#', icon: UserGroupIcon },
  { name: 'Аналитика', path: '#', icon: ChartBarIcon },
  { name: 'Настройки', path: '#', icon: Cog6ToothIcon },
]
</script>

<template>
  <!-- ВАЖНО: Убрали bg-[#F3F4F5], теперь фон прозрачный, чтобы было видно DynamicBackground -->
  <div class="flex h-screen font-sans overflow-hidden bg-transparent">

    <!-- Компонент фона (лежит самым нижним слоем) -->
    <DynamicBackground />

    <Floating3DObjects />

    <!-- Sidebar: z-50 чтобы был поверх всего -->
    <aside class="w-20 lg:w-64 bg-white/80 backdrop-blur-md border-r border-white/40 flex flex-col transition-all duration-300 relative z-50 shadow-2xl">
      <!-- Логотип -->
      <div class="h-20 flex items-center justify-center lg:justify-start lg:px-6 border-b border-gray-100/50">

        <!-- Иконка (Красный квадрат с буквой А) -->
        <div class="w-10 h-10 bg-[#EF3124] rounded-lg flex items-center justify-center text-white shadow-lg shadow-red-500/30 shrink-0 relative overflow-hidden group">
            <!-- Блик для красоты -->
            <div class="absolute inset-0 bg-gradient-to-tr from-black/10 to-transparent"></div>

            <!-- Векторная А -->
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="relative z-10">
                <path d="M12 2L4 22H8L10 17H14L16 22H20L12 2ZM11 14L12 11L13 14H11Z" fill="white"/>
                <rect x="5" y="23" width="14" height="2" fill="white"/> <!-- Подчеркивание -->
            </svg>
        </div>

        <!-- Текст -->
        <div class="hidden lg:block ml-3">
          <div class="font-bold text-[#0B1F35] tracking-wide text-lg leading-none">АЛЬФА</div>
          <div class="text-[10px] text-[#EF3124] uppercase tracking-[0.2em] font-bold mt-1">AI SYSTEM</div>
        </div>
      </div>

      <nav class="flex-1 py-6 space-y-2 px-3">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden"
          :class="route.path === item.path
            ? 'bg-[#0B1F35] text-white shadow-lg shadow-blue-900/20'
            : 'text-gray-600 hover:bg-red-50 hover:text-[#EF3124]'"
        >
          <component :is="item.icon" class="w-6 h-6 shrink-0" />
          <span class="hidden lg:block font-medium">{{ item.name }}</span>
          <div v-if="route.path === item.path" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-[#EF3124] rounded-r-full"></div>
        </router-link>
      </nav>

      <div class="p-4 border-t border-gray-100/50">
        <div class="flex items-center gap-3 p-2 rounded-xl hover:bg-white/50 cursor-pointer transition-colors">
          <img src="https://ui-avatars.com/api/?name=Manager&background=EF3124&color=fff" class="w-10 h-10 rounded-full shadow-sm" alt="Avatar">
          <div class="hidden lg:block overflow-hidden">
            <div class="text-sm font-bold text-[#0B1F35] truncate">Алексей С.</div>
            <div class="text-xs text-gray-400 truncate">Senior Manager</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Content: z-10 чтобы был над фоном -->
    <main class="flex-1 overflow-auto relative z-10">
      <div class="max-w-7xl mx-auto p-6 lg:p-10">
        <slot />
      </div>
    </main>
  </div>
</template>