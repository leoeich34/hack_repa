<script setup lang="ts">
import { onMounted, ref } from 'vue'

// Типы объектов
type ShapeType = 'cube' | 'ring' | 'cross'

interface FloatingObject {
  id: number
  type: ShapeType
  x: number
  y: number
  scale: number
  duration: number
  delay: number
  depth: number // Параллакс эффект (чем меньше, тем дальше)
}

const objects = ref<FloatingObject[]>([])

// Генерация случайных объектов
onMounted(() => {
  const count = 12 // Количество объектов
  for (let i = 0; i < count; i++) {
    objects.value.push({
      id: i,
      type: Math.random() > 0.6 ? 'cube' : (Math.random() > 0.5 ? 'ring' : 'cross'),
      x: Math.random() * 100, // Позиция по горизонтали %
      y: Math.random() * 100, // Позиция по вертикали %
      scale: 0.5 + Math.random() * 1.5, // Размер в пикселях
      duration: 15 + Math.random() * 20, // Скорость полета (сек)
      delay: Math.random() * -20, // Чтобы они уже были на экране при старте
      depth: 0.2 + Math.random() * 0.8 // Прозрачность/размытие
    })
  }
})
</script>

<template>
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-5 perspective-container">

    <div
      v-for="obj in objects"
      :key="obj.id"
      class="absolute object-wrapper"
      :style="{
        left: `${obj.x}%`,
        top: `${obj.y}%`,
        transform: `scale(${obj.scale})`, /* Масштабируем весь объект */
        width: '50px',  /* Фиксированный базовый размер */
        height: '50px',
        animationDuration: `${obj.duration}s`,
        animationDelay: `${obj.delay}s`,
        opacity: obj.depth,
        filter: `blur(${(1 - obj.depth) * 4}px)`, // Дальние объекты размыты
        zIndex: Math.floor(obj.depth * 10) // Сортировка слоев
      }"
    >

      <!-- ТИП 1: КУБИК -->
      <div v-if="obj.type === 'cube'" class="shape-3d cube">
        <div class="face front"></div>
        <div class="face back"></div>
        <div class="face right"></div>
        <div class="face left"></div>
        <div class="face top"></div>
        <div class="face bottom"></div>
      </div>

      <!-- ТИП 2: КОЛЬЦО -->
      <div v-if="obj.type === 'ring'" class="shape-3d ring"></div>

      <!-- ТИП 3: КРЕСТИК (PLUS) -->
      <div v-if="obj.type === 'cross'" class="shape-3d cross">
        <div class="bar h-bar"></div>
        <div class="bar v-bar"></div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.perspective-container {
  perspective: 1000px;
}

/* Анимация пролета */
@keyframes float-around {
  0% { transform: translateY(0) rotateX(0) rotateY(0); }
  25% { transform: translateY(-50px) rotateX(45deg) rotateY(45deg); }
  50% { transform: translateY(0) rotateX(90deg) rotateY(90deg); }
  75% { transform: translateY(50px) rotateX(135deg) rotateY(135deg); }
  100% { transform: translateY(0) rotateX(180deg) rotateY(180deg); }
}

.object-wrapper {
  transform-style: preserve-3d;
  animation: float-around linear infinite;
}

.shape-3d {
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

/* --- STYLES: CUBE --- */
.cube .face {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1); /* Полупрозрачный белый */
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 10px rgba(239, 49, 36, 0.1); /* Красное свечение */
}

/* Красный акцент для некоторых граней */
.cube .face:nth-child(even) {
  background: rgba(239, 49, 36, 0.05);
  border-color: rgba(239, 49, 36, 0.2);
}

.cube .front  { transform: rotateY(0deg) translateZ(25px); }
.cube .back   { transform: rotateY(180deg) translateZ(25px); }
.cube .right  { transform: rotateY(90deg) translateZ(25px); }
.cube .left   { transform: rotateY(-90deg) translateZ(25px); }
.cube .top    { transform: rotateX(90deg) translateZ(25px); }
.cube .bottom { transform: rotateX(-90deg) translateZ(25px); }

/* --- STYLES: RING --- */
.ring {
  border: 4px solid rgba(239, 49, 36, 0.4);
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(239, 49, 36, 0.2);
}

/* --- STYLES: CROSS --- */
.cross .bar {
  position: absolute;
  background: linear-gradient(45deg, #EF3124, #ff8000);
  opacity: 0.8;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(239, 49, 36, 0.4);
}

.cross .h-bar {
  width: 100%;
  height: 20%;
  top: 40%;
  left: 0;
}

.cross .v-bar {
  width: 20%;
  height: 100%;
  left: 40%;
  top: 0;
}
</style>