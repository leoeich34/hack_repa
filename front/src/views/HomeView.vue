<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const router = useRouter()
const clientId = ref('')

const search = () => {
  if (clientId.value) {
    router.push(`/client/${clientId.value}`)
  }
}
</script>

<template>
  <MainLayout>
    <div class="flex flex-col items-center justify-center h-[80vh]">
      <div class="text-center mb-10">
        <h1 class="text-4xl font-bold text-[#0B1F35] mb-4">
          Поиск клиента
        </h1>
        <p class="text-gray-500 max-w-md mx-auto">
          Введите ID клиента для расчета скоринга, прогноза дохода и получения персональных предложений.
        </p>
      </div>

      <div class="bg-white p-2 rounded-2xl shadow-lg flex w-full max-w-lg border border-gray-100">
        <input
          v-model="clientId"
          type="text"
          placeholder="Например: 10245"
          @keyup.enter="search"
          class="flex-1 px-6 py-4 text-lg outline-none text-[#0B1F35] placeholder-gray-300 rounded-xl"
        >
        <button
          @click="search"
          class="bg-[#EF3124] hover:bg-[#D92D20] text-white px-8 py-3 rounded-xl font-medium transition-all transform active:scale-95"
        >
          Найти
        </button>
      </div>

      <!-- Быстрые подсказки (для демо) -->
      <div class="mt-8 flex gap-3 text-sm text-gray-400">
        <span>Популярные:</span>
        <button @click="clientId='101'; search()" class="hover:text-[#EF3124] underline">101</button>
        <button @click="clientId='555'; search()" class="hover:text-[#EF3124] underline">555</button>
      </div>
    </div>
  </MainLayout>
</template>