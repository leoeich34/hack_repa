<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const clientId = ref('12345')
const loading = ref(false)
const result = ref<any>(null)

const getPrediction = async () => {
  loading.value = true
  result.value = null
  try {
    // Стучимся на наш локальный бэк
    const { data } = await axios.get(`http://localhost:3000/api/clients/${clientId.value}/predict`)
    result.value = data
  } catch (e) {
    alert('Ошибка соединения с бэком')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen p-10 flex flex-col items-center">
    <!-- Логотип (текстом) -->
    <h1 class="text-4xl font-bold text-alfa-dark mb-8">
      Альфа <span class="text-alfa-red">Предикт</span>
    </h1>

    <!-- Форма ввода -->
    <div class="bg-white p-6 rounded-xl shadow-lg w-full max-w-md">
      <label class="block text-sm font-medium text-gray-700 mb-2">ID Клиента</label>
      <div class="flex gap-2">
        <input
          v-model="clientId"
          type="text"
          class="border border-gray-300 rounded-lg p-2 flex-1 focus:outline-none focus:border-alfa-red"
        >
        <button
          @click="getPrediction"
          class="bg-alfa-red text-white px-4 py-2 rounded-lg font-medium hover:bg-red-600 transition disabled:opacity-50"
          :disabled="loading"
        >
          {{ loading ? 'Считаем...' : 'Рассчитать' }}
        </button>
      </div>
    </div>

    <!-- Результат (Карточка) -->
    <div v-if="result" class="mt-8 w-full max-w-2xl animate-fade-in">

      <!-- Прогноз -->
      <div class="bg-white p-8 rounded-2xl shadow-sm border-l-4 border-alfa-red flex justify-between items-center">
        <div>
          <div class="text-gray-500 text-sm">Прогноз дохода</div>
          <div class="text-5xl font-bold text-alfa-dark mt-1">
            {{ result.prediction.value.toLocaleString() }} ₽
          </div>
        </div>
        <div class="text-right">
          <div class="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full inline-block">
            Точность {{ result.prediction.confidence }}%
          </div>
        </div>
      </div>

      <!-- Факторы (SHAP) -->
      <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="factor in result.factors" :key="factor.name" class="bg-white p-4 rounded-xl shadow-sm">
          <div class="text-sm font-bold">{{ factor.name }}</div>
          <div class="text-xs text-gray-500">{{ factor.desc }}</div>
          <div class="h-1 w-full bg-gray-100 mt-2 rounded overflow-hidden">
            <div
              class="h-full"
              :class="factor.value > 0 ? 'bg-green-500' : 'bg-red-500'"
              :style="{ width: Math.abs(factor.value) * 5 + '%' }"
            ></div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>