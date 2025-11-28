<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient, type PredictionResponse } from '../services/apiClient'
import Income3DCard from '../components/Income3DCard.vue'
//import SimulatorPanel from '../components/SimulatorPanel.vue'
import {
  BriefcaseIcon,
  CreditCardIcon,
  CheckBadgeIcon,
  ArrowPathIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const loading = ref(true)
const data = ref<PredictionResponse | null>(null)
const error = ref(false)

// Состояние симуляции
const simulatedData = ref<PredictionResponse | null>(null)

// Загрузка данных
onMounted(async () => {
  try {
    const id = route.params.id as string
    data.value = await apiClient.getPrediction(id)
  } catch (e) {
    console.error(e)
    error.value = true
  } finally {
    // Небольшая задержка для красоты анимации лоадера
    setTimeout(() => loading.value = false, 600)
  }
})

// Логика Симулятора: обработка изменений ползунков
const handleSimulation = (changes: any) => {
  if (!data.value) return

  // Если симулятор выключили (null) - сбрасываем
  if (!changes) {
    simulatedData.value = null
    return
  }

  // Клонируем исходные данные, чтобы не мутировать оригинал
  const base = JSON.parse(JSON.stringify(data.value))

  // 1. Рост дохода
  const incomeMult = 1 + (changes.incomeChange / 100)
  base.prediction.value = Math.round(base.prediction.value * incomeMult)

  // 2. Закрытие долгов (снижает ПДН)
  const debtFactor = 1 - (changes.debtClosed / 100)
  base.business_metrics.pdn = Math.max(0, Math.round(base.business_metrics.pdn * debtFactor))

  // Логика изменения риска и уверенности
  if (base.business_metrics.pdn < 30) {
      base.business_metrics.risk_level = 'low'
      // Увеличиваем уверенность модели, так как клиент стал надежнее
      base.prediction.confidence = Math.min(99, base.prediction.confidence + 4)
  }

  // 3. Динамические офферы (При высоком доходе добавляем Premium)
  if (base.prediction.value > 250000 && !base.offers.find((o: any) => o.id === 99)) {
      base.offers.unshift({
          id: 99,
          title: 'Alfa Only',
          text: 'Премиальное обслуживание, консьерж и проходы в бизнес-залы',
          is_best: true
      })
  }

  simulatedData.value = base
}

// Что отображать: реальные данные или симуляцию
const displayData = computed(() => simulatedData.value || data.value)

const refresh = () => window.location.reload()
</script>

<template>
  <div class="animate-fade-in-up">

    <!-- ЛОАДЕР -->
    <div v-if="loading" class="flex flex-col items-center justify-center h-[70vh]">
      <div class="relative w-24 h-24">
        <div class="absolute inset-0 border-4 border-gray-200 rounded-full dark:border-gray-700"></div>
        <div class="absolute inset-0 border-4 border-[#EF3124] rounded-full border-t-transparent animate-spin"></div>
        <div class="absolute inset-0 flex items-center justify-center font-bold text-[#0B1F35] animate-pulse dark:text-white">AI</div>
      </div>
      <p class="mt-6 text-gray-400 font-medium animate-pulse">Анализируем большие данные...</p>
    </div>

    <!-- ОШИБКА -->
    <div v-else-if="error" class="flex flex-col items-center justify-center h-[60vh] text-center">
      <ExclamationTriangleIcon class="w-20 h-20 text-red-400 mb-4 opacity-80" />
      <h3 class="text-2xl font-bold text-[#0B1F35] dark:text-white">Ошибка загрузки</h3>
      <p class="text-gray-500 mb-6 mt-2">Не удалось получить прогноз. Возможно, Backend не запущен.</p>
      <button @click="refresh" class="px-6 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition text-gray-700 dark:bg-white/10 dark:border-white/10 dark:text-white dark:hover:bg-white/20">
        Попробовать снова
      </button>
    </div>

    <!-- КОНТЕНТ -->
    <div v-else-if="displayData" class="pb-10">

      <!-- Шапка -->
      <header class="flex flex-col md:flex-row md:justify-between md:items-end mb-10 gap-4">
        <div>
          <h1 class="text-4xl font-bold text-[#0B1F35] flex items-center gap-3 dark:text-white">
            Клиент #{{ route.params.id }}
            <CheckBadgeIcon class="w-8 h-8 text-blue-500" />
          </h1>
          <p class="text-gray-500 mt-2 text-lg dark:text-gray-400">Полный финансовый профиль и скоринг</p>
        </div>
        <div class="flex gap-3">
            <button
              @click="refresh"
              class="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium hover:bg-gray-50 text-gray-700 transition-colors shadow-sm dark:bg-white/5 dark:border-white/10 dark:text-white dark:hover:bg-white/10"
            >
                <ArrowPathIcon class="w-4 h-4" /> Обновить данные
            </button>
        </div>
      </header>

      <div class="grid grid-cols-12 gap-8">

        <!-- ЛЕВАЯ КОЛОНКА -->
        <div class="col-span-12 lg:col-span-7 space-y-8">

           <!-- 3D Карточка (Передаем актуальные данные) -->
           <Income3DCard
             :amount="displayData.prediction.value"
             :confidence="displayData.prediction.confidence"
           />

           <!-- СИМУЛЯТОР -->
           <!-- Передаем начальные нули, так как логика внутри симулятора сама считает дельту -->
           <SimulatorPanel
             :initial-data="{ income: 0, debtLoad: 0, transactions: 0 }"
             @update="handleSimulation"
           />

           <!-- Метрики (Glassmorphism + Dark Mode) -->
           <div class="grid grid-cols-2 gap-4">
              <!-- Карточка ПДН -->
              <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 flex flex-col justify-between hover:shadow-md transition-all duration-500 dark:bg-white/5 dark:border-white/10">
                  <div class="text-gray-400 text-sm font-medium">ПДН (Нагрузка)</div>
                  <div class="text-3xl font-bold mt-2 transition-colors duration-300"
                       :class="displayData.business_metrics.pdn > 50 ? 'text-[#EF3124]' : 'text-green-600 dark:text-green-400'">
                      {{ displayData.business_metrics.pdn }}%
                  </div>
                  <div class="w-full bg-gray-100 h-1.5 rounded-full mt-3 overflow-hidden dark:bg-white/10">
                      <div class="h-full bg-current rounded-full transition-all duration-500" :style="{ width: displayData.business_metrics.pdn + '%' }"></div>
                  </div>
              </div>

              <!-- Карточка Сегмента -->
              <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 flex flex-col justify-between hover:shadow-md transition-shadow dark:bg-white/5 dark:border-white/10">
                  <div class="text-gray-400 text-sm font-medium">Сегмент риска</div>
                  <div class="text-3xl font-bold text-[#0B1F35] mt-2 capitalize dark:text-white">
                    {{ displayData.business_metrics.risk_level }}
                  </div>
                  <div class="text-xs text-gray-400 mt-3 flex items-center gap-2">
                     <span v-if="simulatedData" class="flex w-2 h-2 bg-orange-500 rounded-full animate-pulse"></span>
                     {{ simulatedData ? 'Расчетный прогноз' : 'Данные из БКИ' }}
                  </div>
              </div>
           </div>
        </div>

        <!-- ПРАВАЯ КОЛОНКА: Офферы -->
        <div class="col-span-12 lg:col-span-5">
            <h3 class="font-bold text-[#0B1F35] text-xl mb-5 flex items-center gap-2 dark:text-white">
                <BriefcaseIcon class="w-6 h-6 text-[#EF3124]" />
                Рекомендации
                <span v-if="simulatedData" class="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full animate-pulse font-bold">AI Simulation</span>
            </h3>

            <div class="space-y-4">
                <!-- Анимация списка -->
                <transition-group name="list" tag="div" class="space-y-4">
                  <div v-for="offer in displayData.offers" :key="offer.id"
                       class="group bg-white/80 backdrop-blur-md p-6 rounded-2xl border border-white/60 shadow-sm hover:border-[#EF3124]/30 hover:shadow-xl hover:shadow-red-500/10 transition-all duration-300 cursor-pointer relative overflow-hidden dark:bg-white/5 dark:border-white/10"
                  >
                      <!-- Эффект подсветки -->
                      <div class="absolute inset-0 bg-gradient-to-r from-red-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity dark:from-white/5"></div>

                      <div class="relative z-10 flex gap-4">
                          <div class="w-12 h-12 rounded-full bg-red-50 text-[#EF3124] flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform dark:bg-white/10">
                              <CreditCardIcon class="w-6 h-6" />
                          </div>
                          <div>
                              <div class="font-bold text-lg text-[#0B1F35] dark:text-white">{{ offer.title }}</div>
                              <p class="text-sm text-gray-500 mt-1 leading-relaxed dark:text-gray-400">{{ offer.text }}</p>
                          </div>
                      </div>

                      <!-- Бейджик New -->
                      <div v-if="offer.id === 99" class="absolute top-0 right-0 bg-[#EF3124] text-white text-[10px] px-2 py-1 rounded-bl-lg font-bold shadow-lg">NEW</div>
                  </div>
                </transition-group>
            </div>
        </div>

        <!-- SHAP (Снизу) -->
        <div class="col-span-12 bg-white/80 backdrop-blur-md p-8 rounded-3xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
            <h3 class="font-bold text-[#0B1F35] text-xl mb-6 dark:text-white">Факторы влияния (SHAP)</h3>

            <div class="space-y-4">
                 <div v-for="factor in displayData.factors" :key="factor.name" class="flex items-center gap-4">
                    <span class="w-32 text-sm text-gray-500 truncate dark:text-gray-400" :title="factor.name">{{ factor.name }}</span>
                    <div class="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden relative dark:bg-white/10">
                         <!-- Центр -->
                         <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-300 z-10 dark:bg-white/20"></div>

                         <div v-if="factor.value > 0"
                              class="absolute left-1/2 top-0 bottom-0 bg-green-500 rounded-r-full"
                              :style="{ width: (factor.value * 5) + '%' }"></div>

                         <div v-else
                              class="absolute right-1/2 top-0 bottom-0 bg-red-400 rounded-l-full"
                              :style="{ width: (Math.abs(factor.value) * 5) + '%' }"></div>
                    </div>
                    <span class="w-16 text-right font-mono font-bold text-sm" :class="factor.value > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-500 dark:text-red-400'">
                        {{ factor.value > 0 ? '+' : ''}}{{ factor.value }}
                    </span>
                 </div>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Анимации для списка офферов */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-active {
  position: absolute;
}
</style>