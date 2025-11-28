<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient, type ClientListItem } from '../services/apiClient'
import {
  MagnifyingGlassIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const clients = ref<ClientListItem[]>([])
const loading = ref(true)
const searchQuery = ref('')
const filterSegment = ref('All')

onMounted(async () => {
  try {
    clients.value = await apiClient.getClients()
  } finally {
    loading.value = false
  }
})

const filteredClients = computed(() => {
  return clients.value.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          client.id.includes(searchQuery.value)
    const matchesFilter = filterSegment.value === 'All' || client.segment === filterSegment.value

    return matchesSearch && matchesFilter
  })
})

const formatCurrency = (val: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
</script>

<template>
    <div class="animate-fade-in-up">

      <!-- Шапка -->
      <div class="flex flex-col md:flex-row justify-between items-end mb-8 gap-4">
        <div>
          <!-- dark:text-white -->
          <h1 class="text-3xl font-bold text-[#0B1F35] dark:text-white">База клиентов</h1>
          <p class="text-gray-500 mt-1 dark:text-gray-400">Всего найдено: {{ filteredClients.length }}</p>
        </div>

        <div class="flex gap-3 w-full md:w-auto">
           <!-- Поиск: dark:bg-white/5 dark:border-white/10 dark:text-white -->
           <div class="relative flex-1 md:w-64">
              <MagnifyingGlassIcon class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по имени или ID..."
                class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition dark:bg-white/5 dark:border-white/10 dark:text-white dark:focus:ring-white/10"
              >
           </div>

           <!-- Фильтр -->
           <select v-model="filterSegment" class="px-4 py-2.5 bg-white border border-gray-200 rounded-xl outline-none cursor-pointer hover:border-gray-300 dark:bg-[#1f2937] dark:border-white/10 dark:text-white">
              <option value="All">Все сегменты</option>
              <option value="Premium">Premium</option>
              <option value="Middle">Middle</option>
              <option value="Mass">Mass</option>
           </select>
        </div>
      </div>

      <!-- Таблица: dark:bg-white/5 dark:border-white/10 -->
      <div class="bg-white/70 backdrop-blur-md border border-white rounded-2xl shadow-sm overflow-hidden dark:bg-white/5 dark:border-white/10">

        <!-- Заголовки: dark:border-white/10 -->
        <div class="grid grid-cols-12 gap-4 p-4 border-b border-gray-100 text-xs font-bold text-gray-400 uppercase tracking-wider dark:border-white/10">
           <div class="col-span-4 md:col-span-3">Клиент</div>
           <div class="col-span-2 hidden md:block">Сегмент</div>
           <div class="col-span-3">Прогноз дохода</div>
           <div class="col-span-2">Риск</div>
           <div class="col-span-2 md:col-span-1"></div>
        </div>

        <div v-if="loading" class="p-8 text-center text-gray-400">
           Загрузка списка...
        </div>

        <!-- Список: dark:divide-white/5 -->
        <div v-else class="divide-y divide-gray-50 dark:divide-white/5">
           <div
             v-for="client in filteredClients"
             :key="client.id"
             @click="router.push(`/client/${client.id}`)"
             class="grid grid-cols-12 gap-4 p-4 items-center hover:bg-white/80 transition-colors cursor-pointer group dark:hover:bg-white/10"
           >
              <!-- Имя + Аватар -->
              <div class="col-span-4 md:col-span-3 flex items-center gap-3">
                 <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-lg font-bold text-gray-500 overflow-hidden dark:bg-white/10 dark:text-gray-300">
                    {{ client.name[0] }}
                 </div>
                 <div class="min-w-0">
                    <div class="font-bold text-[#0B1F35] truncate group-hover:text-[#EF3124] transition-colors dark:text-white">{{ client.name }}</div>
                    <div class="text-xs text-gray-400">ID: {{ client.id }}</div>
                 </div>
              </div>

              <!-- Сегмент -->
              <div class="col-span-2 hidden md:flex items-center">
                 <span class="px-2 py-1 rounded-md text-xs font-medium"
                   :class="client.segment === 'Premium' ? 'bg-black text-white dark:bg-white dark:text-black' : 'bg-gray-100 text-gray-600 dark:bg-white/10 dark:text-gray-300'">
                   {{ client.segment }}
                 </span>
              </div>

              <!-- Доход -->
              <div class="col-span-3 font-mono font-medium text-[#0B1F35] dark:text-white">
                 {{ formatCurrency(client.predicted_income) }}
              </div>

              <!-- Риск -->
              <div class="col-span-3 md:col-span-2 flex items-center">
                 <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full"
                        :class="client.risk_level === 'low' ? 'bg-green-500' : (client.risk_level === 'medium' ? 'bg-yellow-500' : 'bg-red-500')"></div>
                    <span class="text-sm capitalize"
                        :class="client.risk_level === 'low' ? 'text-green-700 dark:text-green-400' : (client.risk_level === 'medium' ? 'text-yellow-700 dark:text-yellow-400' : 'text-red-700 dark:text-red-400')">
                        {{ client.risk_level }}
                    </span>
                 </div>
              </div>

              <!-- Стрелка -->
              <div class="col-span-2 md:col-span-1 flex justify-end text-gray-300 group-hover:text-[#EF3124] transition-all">
                 <ChevronRightIcon class="w-5 h-5" />
              </div>
           </div>
        </div>
      </div>

    </div>
</template>