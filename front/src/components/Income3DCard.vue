<script setup lang="ts">
import { ArrowTrendingUpIcon, WalletIcon } from '@heroicons/vue/24/solid'

defineProps<{
  amount: number
  confidence: number
}>()

const formatCurrency = (val: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
</script>

<template>
  <div class="relative group perspective-1000">
    <!-- Основной контейнер с 3D эффектом -->
    <div class="relative bg-gradient-to-br from-[#0B1F35] to-[#162D47] rounded-3xl p-8 text-white shadow-2xl shadow-blue-900/30 transition-transform duration-500 hover:-translate-y-2 hover:rotate-x-2 overflow-hidden">

      <!-- Декоративные круги (Glass effect) -->
      <div class="absolute -top-10 -right-10 w-40 h-40 bg-[#EF3124] rounded-full blur-[60px] opacity-40"></div>
      <div class="absolute bottom-0 left-0 w-32 h-32 bg-blue-500 rounded-full blur-[50px] opacity-20"></div>

      <!-- Контент -->
      <div class="relative z-10">
        <div class="flex justify-between items-start mb-6">
          <div class="bg-white/10 backdrop-blur-md px-3 py-1 rounded-lg border border-white/10 text-xs font-medium text-gray-300 flex items-center gap-2">
            <WalletIcon class="w-4 h-4 text-[#EF3124]" />
            ML Forecast v2.0
          </div>
          <div class="flex items-center gap-1 text-green-400 text-sm font-bold bg-green-500/10 px-2 py-1 rounded-md border border-green-500/20">
            <ArrowTrendingUpIcon class="w-4 h-4" />
            {{ confidence }}% точность
          </div>
        </div>

        <div class="space-y-1">
          <div class="text-gray-400 text-sm font-medium uppercase tracking-widest">Прогноз дохода</div>
          <div class="text-4xl lg:text-5xl font-bold tracking-tight text-white drop-shadow-lg">
            {{ formatCurrency(amount) }}
          </div>
        </div>

        <div class="mt-8 pt-6 border-t border-white/10 flex justify-between items-end">
          <div class="text-xs text-gray-400 max-w-[200px]">
            Рассчитано на основе 150+ факторов, включая транзакции и кредитную историю.
          </div>
          <button class="bg-[#EF3124] hover:bg-[#D92D20] text-white px-6 py-2 rounded-xl text-sm font-bold shadow-lg shadow-red-600/30 transition-all active:scale-95">
            Подробнее
          </button>
        </div>
      </div>
    </div>

    <!-- Тень снизу для реализма -->
    <div class="absolute -bottom-4 left-10 right-10 h-4 bg-black/20 blur-xl rounded-full transition-all duration-500 group-hover:blur-2xl group-hover:w-[90%] group-hover:left-[5%]"></div>
  </div>
</template>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}
.rotate-x-2 {
  transform: rotateX(2deg);
}
</style>