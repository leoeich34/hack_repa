<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const menuItems = [
  { name: 'Поиск', path: '/', icon: '🔍' },
  { name: 'Клиенты', path: '#', icon: '👥' },
  { name: 'Аналитика', path: '#', icon: '📊' },
  { name: 'Настройки', path: '#', icon: '⚙️' },
]
</script>

<template>
  <div class="flex h-screen bg-[#F3F4F5]">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-6 flex items-center gap-2">
        <!-- Логотип (упрощенно) -->
        <div class="w-8 h-8 bg-[#EF3124] rounded-sm text-white flex items-center justify-center font-bold text-lg">A</div>
        <span class="font-bold text-[#0B1F35] tracking-wide">ALFA <span class="text-[#EF3124]">PREDICT</span></span>
      </div>

      <nav class="flex-1 px-4 space-y-2 mt-4">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors"
          :class="route.path === item.path ? 'bg-[#EF3124] text-white' : 'text-gray-600 hover:bg-gray-100'"
        >
          <span>{{ item.icon }}</span>
          {{ item.name }}
        </router-link>
      </nav>

      <div class="p-4 border-t border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">👨‍💼</div>
          <div>
            <div class="text-sm font-bold text-[#0B1F35]">Менеджер</div>
            <div class="text-xs text-gray-500">Отдел продаж</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <div class="max-w-7xl mx-auto p-8">
        <slot />
      </div>
    </main>
  </div>
</template>