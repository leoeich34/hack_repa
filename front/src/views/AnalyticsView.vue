<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { apiClient, type AnalyticsData } from '../services/apiClient'
import {
  ChartBarIcon, UsersIcon, BanknotesIcon, GlobeAmericasIcon, ArrowPathIcon
} from '@heroicons/vue/24/outline'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement
} from 'chart.js'
import { Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement)

const loading = ref(true)
const data = ref<AnalyticsData | null>(null)

onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  loading.value = true
  try {
    data.value = await apiClient.getAnalytics()
  } finally {
    setTimeout(() => loading.value = false, 600)
  }
}

const formatCurrency = (val: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)

const formatNumber = (val: number) =>
  new Intl.NumberFormat('ru-RU').format(val)

// --- ГРАФИК 1: ГИСТОГРАММА ---
const incomeChartData = computed(() => {
  if (!data.value) return { labels: [], datasets: [] }
  return {
    labels: Object.keys(data.value.incomeDist),
    datasets: [{
      label: 'Клиентов',
      data: Object.values(data.value.incomeDist),
      backgroundColor: '#EF3124',
      borderRadius: 4,
      barThickness: 30
    }]
  }
})

const incomeChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: {
        grid: { color: 'rgba(0,0,0,0.05)', drawBorder: false },
        border: { display: false }
    },
    x: {
        grid: { display: false },
        border: { display: false }
    }
  }
}

// --- ГРАФИК 2: СЕГМЕНТЫ (ПОНЧИК) ---
const segmentChartData = computed(() => {
  if (!data.value) return { labels: [], datasets: [] }
  return {
    labels: ['Mass', 'Middle', 'Premium'],
    datasets: [{
      data: [data.value.segments.Mass, data.value.segments.Middle, data.value.segments.Premium],
      backgroundColor: ['#9CA3AF', '#EF3124', '#0B1F35'],
      borderWidth: 0,
      hoverOffset: 5
    }]
  }
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: {
    legend: {
        // ИСПРАВЛЕНИЕ: Легенда снизу для идеального центрирования
        position: 'bottom' as const,
        labels: { usePointStyle: true, boxWidth: 8, padding: 15, font: { size: 11 } }
    }
  },
  layout: { padding: 0 }
}

// --- ГРАФИК 3: РЕГИОНЫ ---
const regionChartData = computed(() => {
  if (!data.value) return { labels: [], datasets: [] }
  return {
    labels: data.value.topRegions.map(r => r.name),
    datasets: [{
      label: 'Клиентов',
      data: data.value.topRegions.map(r => r.count),
      backgroundColor: '#0B1F35',
      borderRadius: 4,
      barThickness: 12
    }]
  }
})

const regionChartOptions = {
  indexAxis: 'y' as const,
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
      x: { display: false },
      y: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { size: 11 } }
      }
  }
}
</script>

<template>
  <div class="animate-fade-in-up pb-10">

    <!-- HEADER -->
    <div class="flex justify-between items-end mb-8">
        <div>
            <h1 class="text-3xl font-bold text-[#0B1F35] dark:text-white">Аналитика портфеля</h1>
            <p class="text-gray-500 mt-1 dark:text-gray-400">Обзорная статистика по всей базе клиентов</p>
        </div>
        <button @click="loadData" class="p-2 bg-white border rounded-xl hover:bg-gray-50 text-gray-500 dark:bg-white/10 dark:border-white/10 dark:text-white dark:hover:bg-white/20 transition">
            <ArrowPathIcon class="w-5 h-5" :class="loading ? 'animate-spin' : ''" />
        </button>
    </div>

    <!-- SKELETON -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div v-for="i in 4" :key="i" class="h-32 bg-gray-200 rounded-2xl animate-pulse dark:bg-white/5"></div>
    </div>

    <div v-else-if="data">

        <!-- KPI -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
                <div class="flex items-center gap-3 mb-2">
                    <div class="p-2 bg-blue-50 text-blue-600 rounded-lg dark:bg-blue-900/30 dark:text-blue-400"><UsersIcon class="w-5 h-5" /></div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Всего клиентов</span>
                </div>
                <div class="text-3xl font-bold text-[#0B1F35] dark:text-white">{{ formatNumber(data.totalClients) }}</div>
            </div>

            <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
                <div class="flex items-center gap-3 mb-2">
                    <div class="p-2 bg-green-50 text-green-600 rounded-lg dark:bg-green-900/30 dark:text-green-400"><BanknotesIcon class="w-5 h-5" /></div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Средний доход</span>
                </div>
                <div class="text-3xl font-bold text-[#0B1F35] dark:text-white">{{ formatCurrency(data.avgIncome) }}</div>
            </div>

            <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
                <div class="flex items-center gap-3 mb-2">
                    <div class="p-2 bg-red-50 text-red-600 rounded-lg dark:bg-red-900/30 dark:text-red-400"><ChartBarIcon class="w-5 h-5" /></div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Портфель (мес.)</span>
                </div>
                <div class="text-3xl font-bold text-[#0B1F35] dark:text-white">{{ (data.totalPortfolio / 1000000000).toFixed(2) }} млрд ₽</div>
            </div>

            <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
                <div class="flex items-center gap-3 mb-2">
                    <div class="p-2 bg-purple-50 text-purple-600 rounded-lg dark:bg-purple-900/30 dark:text-purple-400"><GlobeAmericasIcon class="w-5 h-5" /></div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Регионов</span>
                </div>
                <div class="text-3xl font-bold text-[#0B1F35] dark:text-white">{{ data.topRegions.length }}+</div>
            </div>
        </div>

        <!-- CHARTS GRID -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">

            <!-- 1. Income -->
            <div class="lg:col-span-2 bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10 flex flex-col">
                <h3 class="font-bold text-[#0B1F35] mb-6 dark:text-white">Распределение по доходам</h3>
                <div class="flex-1 min-h-[400px]">
                    <Bar :data="incomeChartData" :options="incomeChartOptions" />
                </div>
            </div>

            <!-- 2. Segments & Regions -->
            <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10 flex flex-col justify-between">

                <!-- Пончик -->
                <div>
                    <h3 class="font-bold text-[#0B1F35] mb-4 dark:text-white">Сегментация</h3>
                    <!-- Увеличил высоту до 250px для легенды снизу -->
                    <div class="h-[250px] flex justify-center relative">
                        <Doughnut :data="segmentChartData" :options="doughnutOptions" />

                        <!-- Текст по центру -->
                        <!-- ИСПРАВЛЕНИЕ: Убран pr-12, теперь центрируется идеально -->
                        <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none pb-8">
                            <span class="text-3xl font-bold text-[#0B1F35] dark:text-white">{{ Math.round(data.segments.Premium / data.totalClients * 100) }}%</span>
                            <span class="text-[10px] text-gray-400 uppercase tracking-widest">Premium</span>
                        </div>
                    </div>
                </div>

                <div class="border-t border-gray-100 my-2 dark:border-white/10"></div>

                <!-- Регионы -->
                <div>
                    <h4 class="font-bold text-sm mb-4 dark:text-white">Топ регионов</h4>
                    <div class="h-[150px]">
                        <Bar :data="regionChartData" :options="regionChartOptions" />
                    </div>
                </div>
            </div>

        </div>

    </div>
  </div>
</template>