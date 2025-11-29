<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient, type PredictionResponse } from '../services/apiClient'
import Income3DCard from '../components/Income3DCard.vue'
import SimulatorPanel from '../components/SimulatorPanel.vue'
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
const simulatedData = ref<PredictionResponse | null>(null)

// --- СЛОВАРЬ ПЕРЕВОДА ПРИЗНАКОВ ---
const featureDictionary: Record<string, string> = {
  // Основные
  'salary_6to12m_avg': 'Средняя зарплата (6-12 мес)',
  'gender': 'Пол клиента',
  'age': 'Возраст',
  'incomeValue': 'Текущий подтвержденный доход',
  'adminarea': 'Регион проживания',
  'city_smart_name': 'Город',
  'first_salary_income': 'Первый зафиксированный доход',
  'per_capita_income_rur_amt': 'Средний доход в регионе',

  // БКИ (Кредитная история)
  'hdb_bki_total_cc_max_limit': 'Лимит кредитных карт (БКИ)',
  'hdb_bki_total_products': 'Всего продуктов в банке',
  'fe_bki_total_limit': 'Общая кредитная нагрузка',
  'bki_total_max_limit': 'Максимальный одобренный кредит',
  'fe_bki_total_debt': 'Текущая задолженность',
  'hdb_bki_active_cc_max_limit': 'Лимит активной кредитки',
  'hdb_bki_total_max_limit': 'Общий кредитный лимит (все банки)',
  'hdb_bki_total_pil_max_limit': 'Лимит потребительских кредитов',

  // Обороты и транзакции (Turnover)
  'avg_cur_db_turn': 'Обороты по дебетовым картам',
  'avg_cur_cr_turn': 'Кредитовые обороты (среднее)',
  'turn_cur_cr_max_v2': 'Макс. поступления на счет',
  'turn_cur_cr_avg_act_v2': 'Активность поступлений',
  'turn_cur_cr_avg_v2': 'Средние поступления',
  'turn_cur_db_max_v2': 'Макс. списания (дебет)',
  'turn_cur_db_avg_act_v2': 'Активность по дебетовым картам',
  'turn_cur_cr_7avg_avg_v2': 'Поступления (скользящее среднее)',
  'curr_rur_amt_cm_avg': 'Средний остаток на счетах (RUB)',
  'turn_cur_cr_sum_v2': 'Суммарные поступления',

  // FE (Feature Engineering)
  'fe_salary_6to12_to_ils_3y': 'Динамика зарплаты (3 года)'
}

const getFeatureName = (techName: string) => {
  if (featureDictionary[techName]) return featureDictionary[techName]
  // Если перевода нет, делаем красиво из tech_name
  return techName.replace(/_/g, ' ')
}

const formatShapValue = (val: number) => {
  return new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 }).format(val)
}

// Загрузка
onMounted(async () => {
  try {
    const id = route.params.id as string
    data.value = await apiClient.getPrediction(id)
  } catch (e) {
    console.error(e)
    error.value = true
  } finally {
    setTimeout(() => loading.value = false, 600)
  }
})

// Симулятор
const handleSimulation = (changes: any) => {
  if (!data.value) return
  if (!changes) {
    simulatedData.value = null
    return
  }
  const base = JSON.parse(JSON.stringify(data.value))

  const incomeMult = 1 + (changes.incomeChange / 100)
  base.prediction.value = Math.round(base.prediction.value * incomeMult)

  const debtFactor = 1 - (changes.debtClosed / 100)
  base.business_metrics.pdn = Math.max(0, Math.round(base.business_metrics.pdn * debtFactor))

  if (base.business_metrics.pdn < 30) {
      base.business_metrics.risk_level = 'low'
      base.prediction.confidence = Math.min(99, base.prediction.confidence + 4)
  }

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

           <!-- 3D Карточка (С округлением процентов) -->
           <Income3DCard
             :amount="displayData.prediction.value"
             :confidence="Math.round(displayData.prediction.confidence)"
           />

           <!-- СИМУЛЯТОР -->
           <SimulatorPanel
             :initial-data="{ income: 0, debtLoad: 0, transactions: 0 }"
             @update="handleSimulation"
           />

           <!-- Метрики -->
           <div class="grid grid-cols-2 gap-4">
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

        <!-- ПРАВАЯ КОЛОНКА -->
        <div class="col-span-12 lg:col-span-5">
            <h3 class="font-bold text-[#0B1F35] text-xl mb-5 flex items-center gap-2 dark:text-white">
                <BriefcaseIcon class="w-6 h-6 text-[#EF3124]" />
                Рекомендации
                <span v-if="simulatedData" class="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full animate-pulse font-bold">AI Simulation</span>
            </h3>

            <div class="space-y-4">
                <transition-group name="list" tag="div" class="space-y-4">
                  <div v-for="offer in displayData.offers" :key="offer.id"
                       class="group bg-white/80 backdrop-blur-md p-6 rounded-2xl border border-white/60 shadow-sm hover:border-[#EF3124]/30 hover:shadow-xl hover:shadow-red-500/10 transition-all duration-300 cursor-pointer relative overflow-hidden dark:bg-white/5 dark:border-white/10"
                  >
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
                      <div v-if="offer.id === 99" class="absolute top-0 right-0 bg-[#EF3124] text-white text-[10px] px-2 py-1 rounded-bl-lg font-bold shadow-lg">NEW</div>
                  </div>
                </transition-group>
            </div>
        </div>

        <!-- SHAP Факторы (Скролл и Перевод) -->
        <div class="col-span-12 bg-white/80 backdrop-blur-md p-8 rounded-3xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
            <h3 class="font-bold text-[#0B1F35] text-xl mb-6 dark:text-white">Факторы влияния (SHAP)</h3>

            <!-- Обертка для скролла -->
            <div class="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                 <div v-for="factor in displayData.factors" :key="factor.name" class="flex items-center gap-4 text-sm">

                    <!-- 1. Название (Переведенное) -->
                    <span class="w-40 md:w-60 truncate text-gray-600 dark:text-gray-300" :title="factor.name">
                      {{ getFeatureName(factor.name) }}
                    </span>

                    <!-- 2. График -->
                    <div class="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden relative dark:bg-white/10">
                         <!-- Ось -->
                         <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-300 z-10 dark:bg-white/20"></div>

                         <div v-if="factor.value > 0"
                              class="absolute left-1/2 top-0 bottom-0 bg-green-500 rounded-r-full"
                              :style="{ width: (Math.abs(factor.value) / 50000 * 100) + '%' }"></div> <!-- Нормализация ширины (примерно) -->

                         <div v-else
                              class="absolute right-1/2 top-0 bottom-0 bg-red-400 rounded-l-full"
                              :style="{ width: (Math.abs(factor.value) / 50000 * 100) + '%' }"></div>
                    </div>

                    <!-- 3. Значение (Снова видно!) -->
                    <span class="w-24 text-right font-mono font-bold"
                          :class="factor.value > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-500 dark:text-red-400'">
                        {{ factor.value > 0 ? '+' : ''}}{{ formatShapValue(factor.value) }}
                    </span>
                 </div>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Кастомный скроллбар для списка факторов */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 20px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.8);
}

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