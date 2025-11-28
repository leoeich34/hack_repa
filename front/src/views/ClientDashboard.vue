<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient } from '../services/apiClient'
import MainLayout from '../layouts/MainLayout.vue'

const route = useRoute()
const loading = ref(true)
const data = ref<any>(null)

// Загружаем данные при входе на страницу
onMounted(async () => {
  try {
    // Берем ID из URL
    const id = route.params.id as string
    data.value = await apiClient.getPrediction(id)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <MainLayout>
    <!-- Загрузка -->
    <div v-if="loading" class="flex flex-col items-center justify-center h-[60vh]">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#EF3124]"></div>
      <p class="mt-4 text-gray-500">Анализируем данные клиента...</p>
    </div>

    <!-- Контент -->
    <div v-else-if="data" class="animate-fade-in">
      <!-- Заголовок -->
      <header class="flex justify-between items-end mb-8">
        <div>
          <h1 class="text-3xl font-bold text-[#0B1F35]">Клиент #{{ route.params.id }}</h1>
          <p class="text-gray-500 mt-1">Дата обновления: Только что</p>
        </div>
        <div class="flex gap-2">
            <button class="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm hover:bg-gray-50">Скачать отчет</button>
            <button class="px-4 py-2 bg-[#0B1F35] text-white rounded-lg text-sm hover:bg-gray-800">История</button>
        </div>
      </header>

      <!-- Сетка виджетов -->
      <div class="grid grid-cols-12 gap-6">

        <!-- Главная карточка: Прогноз дохода -->
        <div class="col-span-12 md:col-span-8 lg:col-span-6 bg-white p-6 rounded-2xl shadow-sm border border-gray-100 relative overflow-hidden">
             <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-transparent to-red-50 rounded-bl-full"></div>
             <h3 class="text-gray-500 text-sm uppercase tracking-wider font-medium mb-1">Прогнозируемый доход</h3>
             <div class="flex items-baseline gap-3">
                 <span class="text-5xl font-bold text-[#0B1F35] tracking-tight">
                     {{ data.prediction.value.toLocaleString() }} ₽
                 </span>
                 <span class="text-sm bg-green-100 text-green-700 px-2 py-1 rounded-md font-medium">
                     High Confidence
                 </span>
             </div>

             <div class="mt-6 flex gap-4">
                 <div class="flex-1 bg-gray-50 p-3 rounded-lg">
                     <div class="text-xs text-gray-500 mb-1">ПДН (Нагрузка)</div>
                     <div class="text-xl font-bold" :class="data.business_metrics.pdn > 50 ? 'text-red-500' : 'text-green-600'">
                         {{ data.business_metrics.pdn }}%
                     </div>
                 </div>
                 <div class="flex-1 bg-gray-50 p-3 rounded-lg">
                     <div class="text-xs text-gray-500 mb-1">Сегмент</div>
                     <div class="text-xl font-bold text-[#0B1F35]">{{ data.business_metrics.segment }}</div>
                 </div>
             </div>
        </div>

        <!-- Рекомендации (Офферы) -->
        <div class="col-span-12 md:col-span-4 lg:col-span-6 space-y-4">
            <h3 class="font-bold text-gray-700">Персональные предложения</h3>

            <div v-for="offer in data.offers" :key="offer.id"
                 class="bg-white p-5 rounded-xl border border-gray-200 hover:border-[#EF3124] transition-colors cursor-pointer group">
                <div class="flex justify-between items-start">
                    <div>
                        <div class="font-bold text-lg text-[#0B1F35] group-hover:text-[#EF3124] transition-colors">
                            {{ offer.title }}
                        </div>
                        <p class="text-sm text-gray-500 mt-1">{{ offer.text }}</p>
                    </div>
                    <div class="bg-red-50 p-2 rounded-full group-hover:bg-[#EF3124] group-hover:text-white transition-colors">
                        ↗
                    </div>
                </div>
            </div>
        </div>

        <!-- SHAP Факторы (На всю ширину снизу) -->
        <div class="col-span-12 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h3 class="font-bold text-gray-800 mb-4">Факторы влияния на доход</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
                <div v-for="factor in data.factors" :key="factor.name" class="flex items-center text-sm">
                    <span class="w-1/3 text-gray-600">{{ factor.name }}</span>
                    <div class="flex-1 mx-3 h-2 bg-gray-100 rounded-full overflow-hidden flex">
                        <!-- Визуализация влево/вправо -->
                        <div class="w-1/2 flex justify-end bg-gray-100 border-r border-white">
                             <div v-if="factor.value < 0" class="h-full bg-red-400 rounded-l-full" :style="{ width: Math.abs(factor.value) * 5 + '%' }"></div>
                        </div>
                        <div class="w-1/2 bg-gray-100">
                             <div v-if="factor.value > 0" class="h-full bg-green-500 rounded-r-full" :style="{ width: factor.value * 5 + '%' }"></div>
                        </div>
                    </div>
                    <span class="w-12 text-right font-medium" :class="factor.value > 0 ? 'text-green-600' : 'text-red-500'">
                        {{ factor.value > 0 ? '+' : ''}}{{ factor.value }}
                    </span>
                </div>
            </div>
        </div>

      </div>
    </div>
  </MainLayout>
</template>