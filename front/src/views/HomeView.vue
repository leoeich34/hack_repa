<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import {
  ArrowRightIcon,
  MagnifyingGlassIcon,
  BoltIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const clientId = ref('')
const isFocused = ref(false)

const search = () => {
  if (clientId.value) {
    router.push(`/client/${clientId.value}`)
  }
}

const features = [
  {
    title: 'Real-time Scoring',
    desc: 'Мгновенный расчет кредитного потенциала',
    icon: BoltIcon
  },
  {
    title: 'Explainable AI',
    desc: 'Прозрачная интерпретация факторов (SHAP)',
    icon: CpuChipIcon
  },
  {
    title: 'Secure Data',
    desc: 'Обработка данных в закрытом контуре',
    icon: ShieldCheckIcon
  }
]
</script>

<template>
  <MainLayout>
    <div class="flex flex-col min-h-[85vh] relative">

      <!-- ВЕРХНЯЯ ЧАСТЬ: Герой -->
      <div class="flex-1 flex flex-col lg:flex-row items-center justify-center gap-12 lg:gap-24 relative z-10 pt-10">

        <!-- Левая часть: Текст -->
        <div class="flex-1 max-w-xl text-center lg:text-left z-20">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/40 border border-white/50 text-[#EF3124] font-bold text-xs uppercase tracking-widest mb-8 backdrop-blur-md shadow-sm hover:bg-white/60 transition-colors cursor-default">
            <span class="w-2 h-2 rounded-full bg-[#EF3124] animate-pulse"></span>
            Alfa AI Prediction 2.0
          </div>

          <h1 class="text-5xl lg:text-7xl font-bold text-[#0B1F35] leading-tight mb-6 tracking-tight">
            Будущее <br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#EF3124] to-[#B91C10]">уже здесь</span>
          </h1>

          <p class="text-lg text-gray-600 mb-10 leading-relaxed max-w-md mx-auto lg:mx-0">
            Платформа предиктивной аналитики для формирования персональных предложений с точностью до 98%.
          </p>

          <!-- Поле поиска -->
          <div
            class="relative group transition-all duration-300"
            :class="isFocused ? 'scale-105' : ''"
          >
            <div class="absolute -inset-1 bg-gradient-to-r from-[#EF3124] to-orange-500 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>

            <div class="relative flex items-center bg-white rounded-2xl p-2 shadow-xl ring-1 ring-gray-900/5">
              <div class="pl-4 text-gray-400">
                <MagnifyingGlassIcon class="w-6 h-6" />
              </div>
              <input
                v-model="clientId"
                type="text"
                class="flex-1 p-4 bg-transparent outline-none text-[#0B1F35] font-medium text-lg placeholder-gray-400"
                placeholder="ID клиента (например, 777)"
                @focus="isFocused = true"
                @blur="isFocused = false"
                @keyup.enter="search"
              >
              <button
                @click="search"
                class="bg-[#EF3124] hover:bg-[#D92D20] text-white p-4 rounded-xl transition-colors shadow-lg shadow-red-500/30 flex items-center gap-2 font-bold group/btn"
              >
                <span>Найти</span>
                <ArrowRightIcon class="w-5 h-5 group-hover/btn:translate-x-1 transition-transform" />
              </button>
            </div>
          </div>

          <div class="mt-8 flex items-center justify-center lg:justify-start gap-4 text-sm text-gray-500 font-medium">
            <span class="opacity-60">Быстрый поиск:</span>
            <button @click="clientId='1024'; search()" class="px-3 py-1 bg-white/60 border border-white rounded-md shadow-sm hover:text-[#EF3124] hover:border-[#EF3124]/30 transition">1024</button>
            <button @click="clientId='777'; search()" class="px-3 py-1 bg-white/60 border border-white rounded-md shadow-sm hover:text-[#EF3124] hover:border-[#EF3124]/30 transition">777</button>
          </div>
        </div>

        <!-- Правая часть: 3D Сцена -->
        <div class="flex-1 flex justify-center items-center h-[500px] hidden lg:flex perspective-wrapper relative">

           <!-- Плавающие виджеты (Добавляют наполненности) -->
           <div class="absolute top-20 right-10 z-10 glass-widget animate-float-slow">
              <div class="text-xs text-gray-500">Model Accuracy</div>
              <div class="text-xl font-bold text-green-600 flex items-center gap-1">
                98.4% <ChartBarIcon class="w-4 h-4"/>
              </div>
           </div>

           <div class="absolute bottom-32 left-10 z-10 glass-widget animate-float-delayed">
              <div class="text-xs text-gray-500">Active Node</div>
              <div class="text-sm font-bold text-[#0B1F35] flex items-center gap-1">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                Moscow-East-1
              </div>
           </div>

           <!-- КУБ -->
           <div class="cube-scene">
              <div class="alfa-cube">
                <div class="cube-face face-front">A</div>
                <div class="cube-face face-back">L</div>
                <div class="cube-face face-right">F</div>
                <div class="cube-face face-left">A</div>
                <div class="cube-face face-top"></div>
                <div class="cube-face face-bottom"></div>
              </div>
              <div class="orbit-ring ring-inner"></div>
              <div class="orbit-ring ring-outer"></div>
           </div>
        </div>
      </div>

      <!-- НИЖНЯЯ ЧАСТЬ: Преимущества (Заполняем пустоту) -->
      <div class="mt-auto pt-12 pb-6 grid grid-cols-1 md:grid-cols-3 gap-6 z-20">
        <div
          v-for="(feat, idx) in features"
          :key="idx"
          class="bg-white/40 backdrop-blur-md border border-white/60 p-5 rounded-2xl flex items-start gap-4 hover:bg-white/60 transition-colors shadow-sm"
        >
          <div class="w-10 h-10 rounded-lg bg-[#EF3124]/10 text-[#EF3124] flex items-center justify-center shrink-0">
            <component :is="feat.icon" class="w-6 h-6" />
          </div>
          <div>
            <h3 class="font-bold text-[#0B1F35]">{{ feat.title }}</h3>
            <p class="text-sm text-gray-600 mt-1 leading-snug">{{ feat.desc }}</p>
          </div>
        </div>
      </div>

    </div>
  </MainLayout>
</template>

<style scoped>
.glass-widget {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 12px 20px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.perspective-wrapper {
  perspective: 1000px;
}

.cube-scene {
  width: 200px;
  height: 200px;
  position: relative;
  transform-style: preserve-3d;
  animation: sceneFloat 6s ease-in-out infinite;
}

.alfa-cube {
  width: 100%;
  height: 100%;
  position: absolute;
  transform-style: preserve-3d;
  animation: cubeSpin 20s linear infinite;
}

.cube-face {
  position: absolute;
  width: 200px;
  height: 200px;
  background: rgba(239, 49, 36, 0.03);
  border: 1px solid rgba(239, 49, 36, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
  font-weight: bold;
  color: #EF3124;
  backdrop-filter: blur(4px);
  box-shadow: 0 0 40px rgba(239, 49, 36, 0.05);
}

.face-front  { transform: rotateY(0deg) translateZ(100px); }
.face-back   { transform: rotateY(180deg) translateZ(100px); }
.face-right  { transform: rotateY(90deg) translateZ(100px); }
.face-left   { transform: rotateY(-90deg) translateZ(100px); }
.face-top    { transform: rotateX(90deg) translateZ(100px); }
.face-bottom { transform: rotateX(-90deg) translateZ(100px); }

.orbit-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border-radius: 50%;
  border: 1px solid #0B1F35;
  transform: translate(-50%, -50%) rotateX(70deg);
  opacity: 0.1;
  pointer-events: none;
}
.ring-inner { width: 320px; height: 320px; animation: ringSpin 12s linear infinite reverse; }
.ring-outer { width: 480px; height: 480px; animation: ringSpin 20s linear infinite; }

@keyframes cubeSpin {
  from { transform: rotateX(10deg) rotateY(0deg); }
  to { transform: rotateX(10deg) rotateY(360deg); }
}
@keyframes ringSpin {
  from { transform: translate(-50%, -50%) rotateX(70deg) rotateZ(0deg); }
  to { transform: translate(-50%, -50%) rotateX(70deg) rotateZ(360deg); }
}
@keyframes sceneFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
@keyframes float-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
@keyframes float-delayed {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(15px); }
}
.animate-float-slow { animation: float-slow 5s ease-in-out infinite; }
.animate-float-delayed { animation: float-delayed 7s ease-in-out infinite; }
</style>