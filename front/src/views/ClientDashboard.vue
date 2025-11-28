<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient, type PredictionResponse } from '../services/apiClient'
import MainLayout from '../layouts/MainLayout.vue'
import Income3DCard from '../components/Income3DCard.vue'
import {
  BriefcaseIcon,
  CreditCardIcon,
  CheckBadgeIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const loading = ref(true)
const data = ref<PredictionResponse | null>(null)

onMounted(async () => {
  try {
    const id = route.params.id as string
    data.value = await apiClient.getPrediction(id)
  } catch (e) {
    console.error(e)
  } finally {
    setTimeout(() => loading.value = false, 500) // Искусственная задержка для красоты лоадера
  }
})
</script>

<template>
  <MainLayout>
    <!-- Красивый Лоадер -->
    <div v-if="loading" class="flex flex-col items-center justify-center h-[70vh]">
      <div class="relative w-24 h-24">
        <div class="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
        <div class="absolute inset-0 border-4 border-[#EF3124] rounded-full border-t-transparent animate-spin"></div>
        <div class="absolute inset-0 flex items-center justify-center font-bold text-[#0B1F35] animate-pulse">AI</div>
      </div>
      <p class="mt-6 text-gray-400 font-medium animate-pulse">Анализируем большие данные...</p>
    </div>

    <div v-else-if="data" class="animate-fade-in-up">
      <!-- Шапка -->
      <header class="flex flex-col md:flex-row md:justify-between md:items-end mb-10 gap-4">
        <div>
          <h1 class="text-4xl font-bold text-[#0B1F35] flex items-center gap-3">
            Клиент #{{ route.params.id }}
            <CheckBadgeIcon class="w-8 h-8 text-blue-500" />
          </h1>
          <p class="text-gray-500 mt-2 text-lg">Полный финансовый профиль и скоринг</p>
        </div>
        <div class="flex gap-3">
            <button class="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium hover:bg-gray-50 text-gray-700 transition-colors shadow-sm">
                <ArrowPathIcon class="w-4 h-4" /> Обновить
            </button>
        </div>
      </header>

      <div class="grid grid-cols-12 gap-8">

        <!-- Левая колонка: 3D Карточка + Метрики -->
        <div class="col-span-12 lg:col-span-7 space-y-8">
           <!-- 3D Компонент -->
           <Income3DCard
             :amount="data.prediction.value"
             :confidence="data.prediction.confidence"
           />

           <!-- Второстепенные метрики -->
           <div class="grid grid-cols-2 gap-4">
              <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition-shadow">
                  <div class="text-gray-400 text-sm font-medium">ПДН (Нагрузка)</div>
                  <div class="text-3xl font-bold mt-2" :class="data.business_metrics.pdn > 50 ? 'text-[#EF3124]' : 'text-green-600'">
                      {{ data.business_metrics.pdn }}%
                  </div>
                  <div class="w-full bg-gray-100 h-1.5 rounded-full mt-3 overflow-hidden">
                      <div class="h-full bg-current rounded-full" :style="{ width: data.business_metrics.pdn + '%' }"></div>
                  </div>
              </div>
              <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition-shadow">
                  <div class="text-gray-400 text-sm font-medium">Сегмент риска</div>
                  <div class="text-3xl font-bold text-[#0B1F35] mt-2 capitalize">{{ data.business_metrics.risk_level }}</div>
                  <div class="text-xs text-gray-400 mt-3">Обновлено сегодня</div>
              </div>
           </div>
        </div>

        <!-- Правая колонка: Офферы -->
        <div class="col-span-12 lg:col-span-5">
            <h3 class="font-bold text-[#0B1F35] text-xl mb-5 flex items-center gap-2">
                <BriefcaseIcon class="w-6 h-6 text-[#EF3124]" />
                Рекомендации
            </h3>

            <div class="space-y-4">
                <div v-for="offer in data.offers" :key="offer.id"
                     class="group bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:border-[#EF3124]/30 hover:shadow-xl hover:shadow-red-500/10 transition-all duration-300 cursor-pointer relative overflow-hidden">

                    <!-- Эффект при наведении -->
                    <div class="absolute inset-0 bg-gradient-to-r from-red-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>

                    <div class="relative z-10 flex gap-4">
                        <div class="w-12 h-12 rounded-full bg-red-50 text-[#EF3124] flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                            <CreditCardIcon class="w-6 h-6" />
                        </div>
                        <div>
                            <div class="font-bold text-lg text-[#0B1F35]">{{ offer.title }}</div>
                            <p class="text-sm text-gray-500 mt-1 leading-relaxed">{{ offer.text }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SHAP (Снизу) -->
        <div class="col-span-12 bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
            <h3 class="font-bold text-[#0B1F35] text-xl mb-6">Факторы влияния (SHAP)</h3>
            <!-- Тут можно оставить старый код или улучшить его позже -->
            <div class="space-y-4">
                 <div v-for="factor in data.factors" :key="factor.name" class="flex items-center gap-4">
                    <span class="w-32 text-sm text-gray-500 truncate">{{ factor.name }}</span>
                    <div class="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden relative">
                         <!-- Центр -->
                         <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-300 z-10"></div>

                         <div v-if="factor.value > 0"
                              class="absolute left-1/2 top-0 bottom-0 bg-green-500 rounded-r-full"
                              :style="{ width: (factor.value * 5) + '%' }"></div>

                         <div v-else
                              class="absolute right-1/2 top-0 bottom-0 bg-red-400 rounded-l-full"
                              :style="{ width: (Math.abs(factor.value) * 5) + '%' }"></div>
                    </div>
                    <span class="w-16 text-right font-mono font-bold text-sm" :class="factor.value > 0 ? 'text-green-600' : 'text-red-500'">
                        {{ factor.value > 0 ? '+' : ''}}{{ factor.value }}
                    </span>
                 </div>
            </div>
        </div>

      </div>
    </div>
  </MainLayout>
</template>

<style>
/* Простая анимация появления */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}
</style>