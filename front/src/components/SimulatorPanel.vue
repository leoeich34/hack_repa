<script setup lang="ts">
import { ref, watch } from 'vue'
import { AdjustmentsHorizontalIcon, ArrowPathIcon } from '@heroicons/vue/24/outline'

const emit = defineEmits(['update'])

const form = ref({
  incomeChange: 0,    // -50% ... +50%
  debtChange: 0,      // -100% ... +100%
  expensesChange: 0   // -50% ... +50% (Влияет на скоринг риска)
})

const isActive = ref(false)

watch(form, (newVal) => {
  if (!isActive.value) return
  // Если все по нулям — отправляем null, чтобы вернуть исходное состояние
  if (newVal.incomeChange === 0 && newVal.debtChange === 0 && newVal.expensesChange === 0) {
      emit('update', null)
  } else {
      emit('update', newVal)
  }
}, { deep: true })

const toggleSimulation = () => {
  isActive.value = !isActive.value
  if (!isActive.value) {
    reset()
  } else {
    emit('update', null) // Старт с "чистого листа"
  }
}

const reset = () => {
    form.value = { incomeChange: 0, debtChange: 0, expensesChange: 0 }
    emit('update', null)
}
</script>

<template>
  <div class="bg-white/60 backdrop-blur-xl border border-white/60 rounded-2xl p-6 shadow-sm transition-all duration-300 dark:bg-white/5 dark:border-white/10"
       :class="isActive ? 'ring-2 ring-[#EF3124] shadow-red-500/10' : ''">

    <div class="flex justify-between items-center mb-6">
      <div class="flex items-center gap-2">
        <div class="p-2 rounded-lg" :class="isActive ? 'bg-[#EF3124] text-white' : 'bg-gray-100 text-gray-500 dark:bg-gray-700'">
            <AdjustmentsHorizontalIcon class="w-5 h-5" />
        </div>
        <div>
            <h3 class="font-bold text-[#0B1F35] dark:text-white">AI Симулятор</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">Моделирование сценариев</p>
        </div>
      </div>

      <button @click="toggleSimulation" class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none" :class="isActive ? 'bg-[#EF3124]' : 'bg-gray-200 dark:bg-gray-700'">
        <span class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform" :class="isActive ? 'translate-x-6' : 'translate-x-1'" />
      </button>
    </div>

    <div v-if="isActive" class="space-y-5 animate-fade-in">

        <!-- Доход -->
        <div>
            <div class="flex justify-between text-xs font-medium mb-2 text-gray-700 dark:text-gray-300">
                <span>Доход</span>
                <span :class="form.incomeChange >= 0 ? 'text-green-500' : 'text-red-500'">{{ form.incomeChange > 0 ? '+' : ''}}{{ form.incomeChange }}%</span>
            </div>
            <input type="range" min="-50" max="50" step="5" v-model.number="form.incomeChange" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-500 dark:bg-gray-700">
        </div>

        <!-- Кредиты -->
        <div>
            <div class="flex justify-between text-xs font-medium mb-2 text-gray-700 dark:text-gray-300">
                <span>Кредитная нагрузка</span>
                <span :class="form.debtChange <= 0 ? 'text-green-500' : 'text-red-500'">{{ form.debtChange > 0 ? '+' : ''}}{{ form.debtChange }}%</span>
            </div>
            <input type="range" min="-100" max="100" step="10" v-model.number="form.debtChange" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-red-500 dark:bg-gray-700">
        </div>

        <!-- Расходы (Новый!) -->
        <div>
            <div class="flex justify-between text-xs font-medium mb-2 text-gray-700 dark:text-gray-300">
                <span>Ежемес. расходы</span>
                <span :class="form.expensesChange <= 0 ? 'text-green-500' : 'text-red-500'">{{ form.expensesChange > 0 ? '+' : ''}}{{ form.expensesChange }}%</span>
            </div>
            <input type="range" min="-30" max="30" step="5" v-model.number="form.expensesChange" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-orange-500 dark:bg-gray-700">
        </div>

        <button @click="reset" class="w-full py-1 text-[10px] text-gray-400 hover:text-[#EF3124] transition flex justify-center items-center gap-1">
            <ArrowPathIcon class="w-3 h-3" /> Сбросить параметры
        </button>
    </div>

    <div v-else class="text-sm text-gray-400 text-center py-4">Включите для прогноза</div>
  </div>
</template>