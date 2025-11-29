<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient, type ClientListItem } from '../services/apiClient'
import * as XLSX from 'xlsx' // Библиотека для Excel
import {
  MagnifyingGlassIcon,
  ChevronRightIcon,
  ArrowsUpDownIcon,
  UserIcon,
  BanknotesIcon,
  ShieldExclamationIcon,
  XMarkIcon,
  ArrowDownTrayIcon // Иконка скачивания
} from '@heroicons/vue/24/outline'

const router = useRouter()
const clients = ref<ClientListItem[]>([])
const loading = ref(true)

// --- ФИЛЬТРЫ ---
const filters = ref({
  search: '',
  segment: 'All',
  risk: 'All',
  minIncome: ''
})

// --- СОРТИРОВКА ---
const sortState = ref({
  column: 'predicted_income',
  direction: 'desc'
})

// --- ЗАГРУЗКА ---
onMounted(async () => {
  try {
    clients.value = await apiClient.getClients()
  } finally {
    loading.value = false
  }
})

// --- ЛОГИКА ---
const resetFilters = () => {
  filters.value = { search: '', segment: 'All', risk: 'All', minIncome: '' }
}

const toggleSort = (column: string) => {
  if (sortState.value.column === column) {
    sortState.value.direction = sortState.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    sortState.value.column = column
    sortState.value.direction = 'desc'
  }
}

const filteredClients = computed(() => {
  let result = clients.value

  // Фильтрация
  if (filters.value.search) {
    const q = filters.value.search.toLowerCase()
    result = result.filter(c => c.name.toLowerCase().includes(q) || c.id.includes(q))
  }
  if (filters.value.segment !== 'All') {
    result = result.filter(c => c.segment === filters.value.segment)
  }
  if (filters.value.risk !== 'All') {
    result = result.filter(c => c.risk_level === filters.value.risk.toLowerCase())
  }
  if (filters.value.minIncome) {
    const min = parseInt(filters.value.minIncome)
    if (!isNaN(min)) {
      result = result.filter(c => c.predicted_income >= min)
    }
  }

  // Сортировка
  return result.sort((a: any, b: any) => {
    const col = sortState.value.column
    const dir = sortState.value.direction === 'asc' ? 1 : -1
    if (a[col] > b[col]) return 1 * dir
    if (a[col] < b[col]) return -1 * dir
    return 0
  })
})

const formatCurrency = (val: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)

const getRiskColor = (level: string) => {
  switch (level) {
    case 'low': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    case 'medium': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'high': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
    default: return 'bg-gray-100 text-gray-700'
  }
}

// --- ЭКСПОРТ В EXCEL ---
const exportToExcel = () => {
  // 1. Формируем данные для Excel (с русскими заголовками)
  const dataToExport = filteredClients.value.map(client => ({
    'ID Клиента': client.id,
    'ФИО': client.name,
    'Сегмент': client.segment,
    'Прогноз Дохода (₽)': client.predicted_income,
    'Уровень Риска': client.risk_level.toUpperCase(),
    'Последняя активность': client.last_active
  }))

  // 2. Создаем "Книгу" и "Лист"
  const worksheet = XLSX.utils.json_to_sheet(dataToExport)

  // Авто-ширина колонок (для красоты)
  const wscols = [
    { wch: 15 }, // ID
    { wch: 30 }, // ФИО
    { wch: 15 }, // Сегмент
    { wch: 20 }, // Доход
    { wch: 15 }, // Риск
    { wch: 20 }  // Активность
  ]
  worksheet['!cols'] = wscols

  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'База Клиентов')

  // 3. Скачиваем файл
  const date = new Date().toISOString().split('T')[0]
  XLSX.writeFile(workbook, `Alfa_Clients_Export_${date}.xlsx`)
}
</script>

<template>
  <div class="animate-fade-in-up pb-10">

    <!-- ЗАГОЛОВОК И ДЕЙСТВИЯ -->
    <div class="flex flex-col md:flex-row justify-between items-end mb-6 gap-4">
      <div>
        <h1 class="text-3xl font-bold text-[#0B1F35] dark:text-white">База клиентов</h1>
        <p class="text-gray-500 mt-1 dark:text-gray-400">
          Найдено записей: <span class="font-bold text-[#0B1F35] dark:text-white">{{ filteredClients.length }}</span>
        </p>
      </div>

      <div class="flex gap-4 items-center">
          <button @click="resetFilters" class="text-sm text-[#EF3124] hover:underline flex items-center gap-1" v-if="filters.search || filters.segment !== 'All' || filters.risk !== 'All' || filters.minIncome">
            <XMarkIcon class="w-4 h-4" /> Сбросить
          </button>

          <!-- КНОПКА ЭКСПОРТА -->
          <button
            @click="exportToExcel"
            class="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl shadow-md transition font-medium text-sm"
            title="Скачать таблицу в Excel"
          >
            <ArrowDownTrayIcon class="w-5 h-5" />
            Экспорт в Excel
          </button>
      </div>
    </div>

    <!-- ПАНЕЛЬ ФИЛЬТРОВ -->
    <div class="bg-white/70 backdrop-blur-md border border-white p-4 rounded-2xl shadow-sm mb-6 dark:bg-white/5 dark:border-white/10">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

        <!-- Поиск -->
        <div class="relative">
           <MagnifyingGlassIcon class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
           <input v-model="filters.search" type="text" placeholder="Поиск по имени / ID" class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition text-sm dark:bg-[#1f2937] dark:border-gray-700 dark:text-white dark:focus:ring-white/10">
        </div>

        <!-- Сегмент -->
        <div class="relative">
           <UserIcon class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
           <select v-model="filters.segment" class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl outline-none cursor-pointer hover:border-gray-300 text-sm appearance-none dark:bg-[#1f2937] dark:border-gray-700 dark:text-white">
              <option value="All">Все сегменты</option>
              <option value="Premium">Premium</option>
              <option value="Middle">Middle</option>
              <option value="Mass">Mass</option>
           </select>
        </div>

        <!-- Риск -->
        <div class="relative">
           <ShieldExclamationIcon class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
           <select v-model="filters.risk" class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl outline-none cursor-pointer hover:border-gray-300 text-sm appearance-none dark:bg-[#1f2937] dark:border-gray-700 dark:text-white">
              <option value="All">Любой риск</option>
              <option value="low">Low (Низкий)</option>
              <option value="medium">Medium (Средний)</option>
              <option value="high">High (Высокий)</option>
           </select>
        </div>

        <!-- Доход -->
        <div class="relative">
           <BanknotesIcon class="absolute left-3 top-3 w-5 h-5 text-gray-400" />
           <input v-model="filters.minIncome" type="number" placeholder="Доход от..." class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition text-sm dark:bg-[#1f2937] dark:border-gray-700 dark:text-white dark:focus:ring-white/10">
        </div>

      </div>
    </div>

    <!-- ТАБЛИЦА -->
    <div class="bg-white/70 backdrop-blur-md border border-white rounded-2xl shadow-sm overflow-hidden dark:bg-white/5 dark:border-white/10">
      <div class="grid grid-cols-12 gap-4 p-4 border-b border-gray-100 bg-gray-50/50 text-xs font-bold text-gray-500 uppercase tracking-wider dark:border-white/10 dark:bg-white/5 dark:text-gray-400">
         <div class="col-span-4 cursor-pointer hover:text-[#EF3124] flex items-center gap-1 transition-colors" @click="toggleSort('name')">
            Клиент <ArrowsUpDownIcon class="w-3 h-3" :class="sortState.column === 'name' ? 'text-[#EF3124]' : 'opacity-30'" />
         </div>
         <div class="col-span-2 hidden md:block cursor-pointer hover:text-[#EF3124] transition-colors" @click="toggleSort('segment')">
            Сегмент
         </div>
         <div class="col-span-3 cursor-pointer hover:text-[#EF3124] flex items-center gap-1 transition-colors" @click="toggleSort('predicted_income')">
            Доход (ML) <ArrowsUpDownIcon class="w-3 h-3" :class="sortState.column === 'predicted_income' ? 'text-[#EF3124]' : 'opacity-30'" />
         </div>
         <div class="col-span-2 cursor-pointer hover:text-[#EF3124] transition-colors" @click="toggleSort('risk_level')">
            Риск
         </div>
         <div class="col-span-2 md:col-span-1"></div>
      </div>

      <div v-if="loading" class="p-12 flex justify-center">
         <div class="animate-spin rounded-full h-8 w-8 border-2 border-[#EF3124] border-t-transparent"></div>
      </div>

      <div v-else-if="filteredClients.length === 0" class="p-12 text-center text-gray-400">
         Ничего не найдено по вашим фильтрам
      </div>

      <div v-else class="divide-y divide-gray-50 dark:divide-white/5">
         <div
           v-for="client in filteredClients"
           :key="client.id"
           @click="router.push(`/client/${client.id}`)"
           class="grid grid-cols-12 gap-4 p-4 items-center hover:bg-white/80 transition-all cursor-pointer group relative overflow-hidden dark:hover:bg-white/10"
         >
            <div v-if="client.risk_level === 'high'" class="absolute left-0 top-0 bottom-0 w-1 bg-red-500"></div>

            <div class="col-span-4 flex items-center gap-3 pl-2">
               <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shadow-sm shrink-0 transition-transform group-hover:scale-105"
                    :class="client.segment === 'Premium'
                        ? 'bg-gradient-to-br from-gray-800 to-black text-[#D4AF37] border border-[#D4AF37]/50'
                        : 'bg-white border border-gray-200 text-gray-500 dark:bg-white/10 dark:border-white/10 dark:text-white'">
                  {{ client.name[0] }}
               </div>
               <div class="min-w-0">
                  <div class="font-bold text-[#0B1F35] truncate group-hover:text-[#EF3124] transition-colors dark:text-white">{{ client.name }}</div>
                  <div class="text-[10px] text-gray-400 font-mono">ID: {{ client.id }}</div>
               </div>
            </div>

            <div class="col-span-2 hidden md:flex items-center">
               <span class="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border"
                 :class="client.segment === 'Premium'
                    ? 'bg-black text-[#D4AF37] border-[#D4AF37]/30 shadow-sm dark:bg-white dark:text-black dark:border-transparent'
                    : (client.segment === 'Middle'
                        ? 'bg-blue-50 text-blue-700 border-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800'
                        : 'bg-gray-50 text-gray-600 border-gray-200 dark:bg-white/5 dark:text-gray-400 dark:border-white/10')">
                 {{ client.segment }}
               </span>
            </div>

            <div class="col-span-3 font-mono font-medium text-[#0B1F35] text-sm dark:text-white">
               {{ formatCurrency(client.predicted_income) }}
            </div>

            <div class="col-span-2 flex items-center">
               <span class="px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1.5"
                     :class="getRiskColor(client.risk_level)">
                  <div class="w-1.5 h-1.5 rounded-full bg-current"></div>
                  {{ client.risk_level.toUpperCase() }}
               </span>
            </div>

            <div class="col-span-1 flex justify-end text-gray-300 group-hover:text-[#EF3124] group-hover:translate-x-1 transition-all">
               <ChevronRightIcon class="w-5 h-5" />
            </div>
         </div>
      </div>

      <div class="p-4 border-t border-gray-100 flex justify-between items-center text-sm text-gray-500 dark:border-white/10 dark:text-gray-400" v-if="filteredClients.length > 0">
          <div>Показано {{ filteredClients.length }} записей</div>
      </div>

    </div>

  </div>
</template>