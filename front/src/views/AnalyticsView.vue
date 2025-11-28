<script setup lang="ts">
import { computed } from 'vue'
import { useSettingsStore } from '../store/settings'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement
} from 'chart.js'
import { Doughnut, Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, PointElement, LineElement)

const settingsStore = useSettingsStore()

// Вычисляем цвет текста для графиков в зависимости от темы
const textColor = computed(() => settingsStore.theme === 'dark' ? '#FFFFFF' : '#0B1F35')
const gridColor = computed(() => settingsStore.theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)')

// 1. График: Сегменты
const segmentData = {
  labels: ['Premium', 'Middle', 'Mass'],
  datasets: [{
    backgroundColor: ['#0B1F35', '#EF3124', '#9CA3AF'],
    data: [15, 35, 50],
    borderWidth: 0
  }]
}

// Опции делаем вычисляемыми, чтобы они реагировали на смену темы
const segmentOptions = computed(() => ({
  responsive: true,
  cutout: '75%',
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { color: textColor.value } // Адаптивный цвет
    }
  },
  borderColor: settingsStore.theme === 'dark' ? 'transparent' : '#fff'
}))

// 2. График: Точность
const accuracyData = {
  labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
  datasets: [{
    label: 'Точность модели (%)',
    backgroundColor: 'rgba(239, 49, 36, 0.2)',
    borderColor: '#EF3124',
    data: [92, 93, 94.5, 94.2, 96, 98],
    tension: 0.4,
    fill: true,
    pointBackgroundColor: '#EF3124'
  }]
}

const accuracyOptions = computed(() => ({
  responsive: true,
  scales: {
    y: {
      min: 80,
      max: 100,
      grid: { color: gridColor.value },
      ticks: { color: textColor.value }
    },
    x: {
      grid: { display: false },
      ticks: { color: textColor.value }
    }
  },
  plugins: {
    legend: {
      labels: { color: textColor.value }
    }
  }
}))
</script>

<template>
  <div class="animate-fade-in-up pb-10">
    <h1 class="text-3xl font-bold text-[#0B1F35] mb-8 dark:text-white">Аналитика портфеля</h1>

    <!-- KPI Карточки: dark:bg-white/5 dark:border-white/10 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white/70 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
         <div class="text-gray-500 text-sm dark:text-gray-400">Всего клиентов</div>
         <div class="text-3xl font-bold text-[#0B1F35] mt-2 dark:text-white">14,205</div>
      </div>
      <div class="bg-white/70 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
         <div class="text-gray-500 text-sm dark:text-gray-400">Средний доход</div>
         <div class="text-3xl font-bold text-[#0B1F35] mt-2 dark:text-white">84.5k ₽</div>
      </div>
      <div class="bg-white/70 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
         <div class="text-gray-500 text-sm dark:text-gray-400">Качество (WMAE)</div>
         <div class="text-3xl font-bold text-green-600 mt-2 dark:text-green-400">2.4%</div>
      </div>
       <div class="bg-white/70 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
         <div class="text-gray-500 text-sm dark:text-gray-400">Одобрено кредитов</div>
         <div class="text-3xl font-bold text-[#EF3124] mt-2">~1.2B ₽</div>
      </div>
    </div>

    <!-- Графики -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

      <!-- График 1 -->
      <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm min-h-[400px] dark:bg-white/5 dark:border-white/10">
         <h3 class="font-bold text-lg mb-4 text-[#0B1F35] dark:text-white">Сегментация базы</h3>
         <div class="h-[300px] flex justify-center relative">
            <Doughnut :data="segmentData" :options="segmentOptions" />
            <!-- Число в центре пончика -->
            <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span class="text-3xl font-bold text-[#0B1F35] dark:text-white">3</span>
                <span class="text-xs text-gray-500">Сегмента</span>
            </div>
         </div>
      </div>

      <!-- График 2 -->
      <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm min-h-[400px] dark:bg-white/5 dark:border-white/10">
         <h3 class="font-bold text-lg mb-4 text-[#0B1F35] dark:text-white">Динамика качества модели</h3>
         <div class="h-[300px]">
            <Line :data="accuracyData" :options="accuracyOptions" />
         </div>
      </div>

    </div>
  </div>
</template>