<script setup lang="ts">
import { useRouter } from 'vue-router'
import DynamicBackground from '../components/ui/DynamicBackground.vue'
import Floating3DObjects from '../components/ui/Floating3DObjects.vue'

const router = useRouter()
</script>

<template>
  <div class="relative min-h-screen flex flex-col items-center justify-center overflow-hidden font-sans text-[#0B1F35]">

    <!-- Фоны -->
    <DynamicBackground />
    <Floating3DObjects />

    <!-- Главный контент -->
    <div class="relative z-10 flex flex-col items-center text-center px-4">

      <!-- Гигантский логотип-куб -->
      <div class="perspective-container mb-12">
        <div class="huge-cube">
          <div class="face front">A</div>
          <div class="face back">L</div>
          <div class="face right">F</div>
          <div class="face left">A</div>
          <div class="face top"></div>
          <div class="face bottom"></div>
        </div>
        <!-- Декоративные кольца -->
        <div class="orbit-ring ring-1"></div>
        <div class="orbit-ring ring-2"></div>
      </div>

      <h1 class="text-6xl md:text-8xl font-bold tracking-tighter mb-6">
        ALFA <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#EF3124] to-orange-500">AI</span>
      </h1>

      <p class="text-xl md:text-2xl text-gray-600 max-w-2xl mb-12 leading-relaxed">
        Система предиктивного скоринга следующего поколения. <br>
        Точность. Скорость. Персонализация.
      </p>

      <div class="flex gap-6">
        <button
          @click="router.push('/auth?mode=login')"
          class="px-10 py-4 bg-[#0B1F35] text-white text-lg font-bold rounded-2xl hover:bg-black transition shadow-xl hover:scale-105 active:scale-95"
        >
          Войти
        </button>
        <button
          @click="router.push('/auth?mode=register')"
          class="px-10 py-4 bg-white/50 backdrop-blur-md border border-white text-[#0B1F35] text-lg font-bold rounded-2xl hover:bg-white transition shadow-lg hover:scale-105 active:scale-95"
        >
          Регистрация
        </button>
      </div>

    </div>

    <!-- Футер -->
    <div class="absolute bottom-8 text-sm text-gray-400">
      © 2025 Alfa Hackathon Team. Designed for the Future.
    </div>

  </div>
</template>

<style scoped>
.perspective-container {
  perspective: 1200px;
  width: 200px;
  height: 200px;
  position: relative;
}

.huge-cube {
  width: 100%;
  height: 100%;
  position: absolute;
  transform-style: preserve-3d;
  animation: hugeSpin 20s linear infinite;
}

.face {
  position: absolute;
  width: 200px;
  height: 200px;
  background: rgba(239, 49, 36, 0.1);
  border: 2px solid rgba(239, 49, 36, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 100px;
  font-weight: 900;
  color: #EF3124;
  backdrop-filter: blur(5px);
  box-shadow: 0 0 50px rgba(239, 49, 36, 0.2);
}

.front  { transform: rotateY(0deg) translateZ(100px); }
.back   { transform: rotateY(180deg) translateZ(100px); }
.right  { transform: rotateY(90deg) translateZ(100px); }
.left   { transform: rotateY(-90deg) translateZ(100px); }
.top    { transform: rotateX(90deg) translateZ(100px); }
.bottom { transform: rotateX(-90deg) translateZ(100px); }

.orbit-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border-radius: 50%;
  border: 1px solid #0B1F35;
  transform: translate(-50%, -50%) rotateX(70deg);
  opacity: 0.2;
}
.ring-1 { width: 350px; height: 350px; animation: ringRotate 15s linear infinite reverse; }
.ring-2 { width: 500px; height: 500px; animation: ringRotate 25s linear infinite; }

@keyframes hugeSpin {
  from { transform: rotateX(15deg) rotateY(0deg); }
  to { transform: rotateX(15deg) rotateY(360deg); }
}
@keyframes ringRotate {
  from { transform: translate(-50%, -50%) rotateX(70deg) rotateZ(0deg); }
  to { transform: translate(-50%, -50%) rotateX(70deg) rotateZ(360deg); }
}
</style>