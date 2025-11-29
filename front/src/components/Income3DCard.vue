<script setup lang="ts">
import { ArrowTrendingUpIcon, WalletIcon } from '@heroicons/vue/24/solid'

defineProps<{
  amount: number,
  confidence: number
}>()

const formatCurrency = (val: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
</script>

<template>
  <div class="relative group perspective-1000">
    <div class="relative bg-gradient-to-br from-[#0B1F35] to-[#162D47] rounded-3xl p-8 text-white shadow-2xl shadow-blue-900/30 transition-transform duration-500 hover:-translate-y-2 hover:rotate-x-2 overflow-hidden">

      <div class="absolute -top-10 -right-10 w-40 h-40 bg-[#EF3124] rounded-full blur-[60px] opacity-40"></div>
      <div class="absolute bottom-0 left-0 w-32 h-32 bg-blue-500 rounded-full blur-[50px] opacity-20"></div>

      <div class="relative z-10">
        <div class="flex justify-between items-start mb-6">
          <div class="bg-white/10 backdrop-blur-md px-3 py-1 rounded-lg border border-white/10 text-xs font-medium text-gray-300 flex items-center gap-2">
            <WalletIcon class="w-4 h-4 text-[#EF3124]" />
            ML CatBoostRegressor
          </div>
          <!-- УБРАЛИ БЛОК С ТОЧНОСТЬЮ -->
        </div>

        <div class="space-y-1">
          <div class="text-gray-400 text-sm font-medium uppercase tracking-widest">Прогноз дохода</div>
          <div class="text-4xl lg:text-5xl font-bold tracking-tight text-white drop-shadow-lg">
            {{ formatCurrency(amount) }}
          </div>
        </div>

        <div class="mt-8 pt-6 border-t border-white/10 flex justify-between items-end">
          <div class="text-xs text-gray-400 max-w-[200px]">
            Рассчитано на основе транзакций и кредитной истории.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>