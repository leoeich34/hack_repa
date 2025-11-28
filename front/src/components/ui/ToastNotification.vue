<script setup lang="ts">
import { useNotification } from '../../composables/useNotification'
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/24/solid'

const { isVisible, message, type } = useNotification()
</script>

<template>
  <Transition name="toast">
    <div v-if="isVisible" class="fixed top-6 left-1/2 -translate-x-1/2 z-[100] flex items-center gap-3 px-6 py-4 rounded-2xl glass-toast shadow-2xl">

      <!-- Иконка -->
      <div class="p-1 rounded-full bg-white/20">
        <CheckCircleIcon v-if="type === 'success'" class="w-6 h-6 text-white" />
        <ExclamationCircleIcon v-else class="w-6 h-6 text-white" />
      </div>

      <!-- Текст -->
      <div>
        <div class="font-bold text-white text-sm tracking-wide">
          {{ type === 'success' ? 'Успешно' : 'Ошибка' }}
        </div>
        <div class="text-white/80 text-xs font-medium">
          {{ message }}
        </div>
      </div>

      <!-- Декоративное свечение -->
      <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-white/10 to-transparent pointer-events-none"></div>
    </div>
  </Transition>
</template>

<style scoped>
.glass-toast {
  background: rgba(11, 31, 53, 0.85); /* Темно-синий фон */
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-width: 320px;
}

/* Анимация появления сверху */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>