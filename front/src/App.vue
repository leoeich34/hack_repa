<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from './layouts/MainLayout.vue'
import ToastNotification from './components/ui/ToastNotification.vue'

const route = useRoute()

// Вычисляем, какой лейаут использовать
const layout = computed(() => {
  return route.meta.layout === 'main' ? MainLayout : 'div'
})
</script>

<template>
  <ToastNotification />

  <!-- Динамический компонент: Либо MainLayout, либо пустой div -->
  <component :is="layout">

    <!-- Внутри лейауна рендерится страница -->
    <router-view v-slot="{ Component }">
      <transition name="page-fade" mode="out-in">
        <component :is="Component" :key="route.fullPath" />
      </transition>
    </router-view>

  </component>
</template>

<style>
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
  filter: blur(4px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  filter: blur(4px);
}
</style>