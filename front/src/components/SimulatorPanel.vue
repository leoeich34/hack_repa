<script setup lang="ts">
import { ref, watch } from 'vue'
import { AdjustmentsHorizontalIcon, ArrowPathIcon } from '@heroicons/vue/24/outline'

// Пропсы не обязательны для логики, но нужны для типизации
const props = defineProps<{
  initialData: { income: number; debtLoad: number; transactions: number }
}>()

// Событие, которое мы отправляем родителю (Дашборду)
const emit = defineEmits(['update'])

// Состояние ползунков
const form = ref({
  incomeChange: 0,    // Рост дохода в % (0..50)
  debtClosed: 0,      // Погашение долгов в % (0..100)
  transActivity: 0
})

const isActive = ref(false)

// ГЛАВНАЯ МАГИЯ: Следим за изменениями ползунков
watch(form, (newVal) => {
  if (!isActive.value) return
  // Отправляем новые значения родителю в реальном времени
  emit('update', newVal)
}, { deep: true })

// Включение/Выключение
const toggleSimulation = () => {
  isActive.value = !isActive.value
  if (!isActive.value) {
    // Если выключили - сбрасываем всё в ноль
    form.value = { incomeChange: 0, debtClosed: 0, transActivity: 0 }
    emit('update', null) // null говорит родителю: "покажи реальные данные"
  } else {
    emit('update', form.value)
  }
}
</script>

<template>
  <div class="bg-white/60 backdrop-blur-xl border border-white/60 rounded-2xl p-6 shadow-sm transition-all duration-300"
       :class="isActive ? 'ring-2 ring-[#EF3124] shadow-red-500/10' : ''">

    <!-- Заголовок и Переключатель (Toggle) -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex items-center gap-2">
        <div class="p-2 rounded-lg" :class="isActive ? 'bg-[#EF3124] text-white' : 'bg-gray-100 text-gray-500'">
            <AdjustmentsHorizontalIcon class="w-5 h-5" />
        </div>
        <div>
            <h3 class="font-bold text-[#0B1F35] dark:text-[#0B1F35]">AI Симулятор</h3>
            <p class="text-xs text-gray-500">Моделирование сценариев</p>
        </div>
      </div>

      <button
        @click="toggleSimulation"
        class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none"
        :class="isActive ? 'bg-[#EF3124]' : 'bg-gray-200'"
      >
        <span
            class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
            :class="isActive ? 'translate-x-6' : 'translate-x-1'"
        />
      </button>
    </div>

    <!-- Сами ползунки (показываем только если активен) -->
    <div v-if="isActive" class="space-y-6 animate-fade-in">

        <!-- Ползунок 1: Доход -->
        <div>
            <div class="flex justify-between text-sm mb-2 text-gray-700">
                <span>Рост официального дохода</span>
                <span class="font-bold text-[#EF3124]">+{{ form.incomeChange }}%</span>
            </div>
            <input type="range" min="0" max="50" step="5" v-model.number="form.incomeChange"
                   class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#EF3124]">
        </div>

        <!-- Ползунок 2: Долги -->
        <div>
            <div class="flex justify-between text-sm mb-2 text-gray-700">
                <span>Погашение кредитов</span>
                <span class="font-bold text-green-600">-{{ form.debtClosed }}%</span>
            </div>
            <input type="range" min="0" max="100" step="10" v-model.number="form.debtClosed"
                   class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-600">
        </div>
    </div>

    <div v-else class="text-sm text-gray-400 text-center py-4">
        Включите симулятор, чтобы увидеть прогноз.
    </div>

  </div>
</template>