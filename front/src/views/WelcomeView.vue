<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DynamicBackground from '../components/ui/DynamicBackground.vue'
import Floating3DObjects from '../components/ui/Floating3DObjects.vue'
import {
  ArrowRightIcon, BoltIcon, ChartBarIcon, ShieldCheckIcon,
  XMarkIcon, CommandLineIcon, CodeBracketIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const showDocs = ref(false) // Состояние модалки
</script>

<template>
  <div class="relative min-h-screen flex flex-col overflow-hidden font-sans text-[#0B1F35] dark:text-white">

    <!-- Фоны -->
    <DynamicBackground />
    <Floating3DObjects />

    <!-- Navbar -->
    <nav class="absolute top-0 w-full p-6 flex justify-between items-center z-20">
        <div class="flex items-center gap-2 font-black text-xl tracking-tight">
            <div class="w-10 h-10 bg-gradient-to-br from-[#EF3124] to-[#B91C10] rounded-xl flex items-center justify-center text-white shadow-lg">A</div>
            <span>ALFA <span class="text-[#EF3124]">HORIZON</span></span>
        </div>
        <div class="flex gap-4">
            <button @click="router.push('/auth?mode=login')" class="px-6 py-2 rounded-full border border-[#0B1F35]/10 hover:bg-white hover:shadow-lg transition dark:border-white/20 dark:hover:bg-white dark:hover:text-black font-bold text-sm backdrop-blur-md">
                Войти
            </button>
        </div>
    </nav>

    <!-- Content Grid -->
    <div class="flex-1 flex flex-col lg:flex-row items-center justify-center px-6 lg:px-20 relative z-10 pt-20">

      <!-- Left: Text -->
      <div class="flex-1 max-w-2xl text-center lg:text-left z-20">

        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/40 border border-white/50 text-[#EF3124] font-bold text-xs uppercase tracking-widest mb-8 backdrop-blur-md shadow-sm dark:bg-white/10 dark:border-white/10">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            System Online v2.1
        </div>

        <h1 class="text-6xl lg:text-8xl font-black tracking-tighter mb-6 leading-[1.1]">
          Видим <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#EF3124] to-orange-500">Будущее</span> <br>
          Клиентов
        </h1>

        <p class="text-xl text-gray-600 mb-10 leading-relaxed dark:text-gray-300 max-w-lg mx-auto lg:mx-0">
          Платформа предиктивной аналитики. <br>
          Точность скоринга <span class="font-bold text-[#0B1F35] dark:text-white">98.4%</span> благодаря технологиям CatBoost и SHAP.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <button @click="router.push('/auth?mode=register')" class="group px-8 py-4 bg-[#EF3124] text-white text-lg font-bold rounded-2xl hover:bg-[#D92D20] transition shadow-xl shadow-red-500/30 hover:scale-105 active:scale-95 flex items-center justify-center gap-2">
                Начать работу
                <ArrowRightIcon class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>

            <!-- КНОПКА ДОКУМЕНТАЦИИ -->
            <button
              @click="showDocs = true"
              class="px-8 py-4 bg-white/50 backdrop-blur-md border border-white/50 text-[#0B1F35] text-lg font-bold rounded-2xl hover:bg-white transition shadow-lg hover:scale-105 active:scale-95 dark:bg-white/10 dark:border-white/10 dark:text-white dark:hover:bg-white/20"
            >
                О проекте
            </button>
        </div>

        <!-- Features Mini Grid -->
        <div class="mt-16 grid grid-cols-3 gap-4 border-t border-gray-200/50 pt-8 dark:border-white/10">
            <div>
                <div class="font-black text-2xl text-[#0B1F35] dark:text-white">0.3s</div>
                <div class="text-xs text-gray-500 font-bold uppercase tracking-wide">Скорость</div>
            </div>
            <div>
                <div class="font-black text-2xl text-[#0B1F35] dark:text-white">150+</div>
                <div class="text-xs text-gray-500 font-bold uppercase tracking-wide">Факторов</div>
            </div>
            <div>
                <div class="font-black text-2xl text-[#0B1F35] dark:text-white">98%</div>
                <div class="text-xs text-gray-500 font-bold uppercase tracking-wide">Точность</div>
            </div>
        </div>
      </div>

      <!-- Right: 3D Cube -->
      <div class="flex-1 flex justify-center items-center h-[500px] perspective-wrapper relative w-full hidden lg:flex">
         <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
             <div class="orbit-ring ring-1"></div>
             <div class="orbit-ring ring-2"></div>
         </div>
         <div class="cube-scene">
            <div class="alfa-cube">
              <div class="cube-face face-front">A</div>
              <div class="cube-face face-back">L</div>
              <div class="cube-face face-right">F</div>
              <div class="cube-face face-left">A</div>
              <div class="cube-face face-top"></div>
              <div class="cube-face face-bottom"></div>
            </div>
         </div>
      </div>

    </div>

    <!-- Footer -->
    <div class="absolute bottom-6 w-full text-center text-xs text-gray-400 opacity-60">
      © 2025 d0ramilK1SS Team. Hackathon Edition.
    </div>

    <!-- ======================= -->
    <!-- МОДАЛЬНОЕ ОКНО DOCS -->
    <!-- ======================= -->
    <Transition name="modal">
      <div v-if="showDocs" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showDocs = false"></div>

          <!-- Modal Card -->
          <div class="relative bg-white dark:bg-[#0B1F35] w-full max-w-2xl rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 overflow-hidden flex flex-col max-h-[90vh]">

              <!-- Header -->
              <div class="p-6 border-b border-gray-100 dark:border-white/10 flex justify-between items-center bg-gray-50/50 dark:bg-white/5">
                  <h2 class="text-2xl font-black text-[#0B1F35] dark:text-white flex items-center gap-2">
                      <CommandLineIcon class="w-6 h-6 text-[#EF3124]" />
                      Технический стек
                  </h2>
                  <button @click="showDocs = false" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-white/10 transition">
                      <XMarkIcon class="w-6 h-6 text-gray-500" />
                  </button>
              </div>

              <!-- Body (Scrollable) -->
              <div class="p-8 overflow-y-auto">
                  <p class="text-gray-600 dark:text-gray-300 mb-6 text-lg leading-relaxed">
                      <b>Alfa Horizon</b> — это микросервисная архитектура для высоконагруженного скоринга.
                      Мы объединили мощь ML с гибкостью современного веба.
                  </p>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                      <div class="space-y-3">
                          <h3 class="font-bold text-[#0B1F35] dark:text-white flex items-center gap-2">
                              <BoltIcon class="w-5 h-5 text-yellow-500" /> Frontend
                          </h3>
                          <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 list-disc list-inside">
                              <li>Vue 3 + TypeScript + Vite</li>
                              <li>Tailwind CSS (Dark Mode)</li>
                              <li>Chart.js + 3D CSS Animations</li>
                              <li>HTML2PDF Report Generation</li>
                          </ul>
                      </div>
                      <div class="space-y-3">
                          <h3 class="font-bold text-[#0B1F35] dark:text-white flex items-center gap-2">
                              <ShieldCheckIcon class="w-5 h-5 text-green-500" /> Backend & ML
                          </h3>
                          <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 list-disc list-inside">
                              <li>Node.js + Express (Gateway)</li>
                              <li>Python FastAPI (Inference)</li>
                              <li>CatBoost Regressor</li>
                              <li>SHAP (Explainable AI)</li>
                          </ul>
                      </div>
                  </div>

                  <div class="bg-gray-50 dark:bg-white/5 p-4 rounded-xl border border-gray-100 dark:border-white/10 mb-6">
                      <h4 class="font-bold text-sm mb-2 text-[#0B1F35] dark:text-white">Ключевые фичи:</h4>
                      <div class="flex flex-wrap gap-2">
                          <span class="px-3 py-1 rounded-lg bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 text-xs font-bold">Симулятор "Что-Если"</span>
                          <span class="px-3 py-1 rounded-lg bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 text-xs font-bold">Генерация Досье (PDF)</span>
                          <span class="px-3 py-1 rounded-lg bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 text-xs font-bold">Интеграция CSV</span>
                          <span class="px-3 py-1 rounded-lg bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 text-xs font-bold">Умные офферы</span>
                      </div>
                  </div>
              </div>

              <!-- Footer -->
              <div class="p-6 border-t border-gray-100 dark:border-white/10 bg-gray-50/50 dark:bg-white/5 flex justify-end">
                  <a href="https://gitlab.com/d0ra_group/incoumingalpha" target="_blank"
                     class="flex items-center gap-2 px-6 py-3 bg-[#0B1F35] hover:bg-black text-white rounded-xl font-bold transition shadow-lg dark:bg-[#EF3124] dark:hover:bg-[#d92d20]">
                      <CodeBracketIcon class="w-5 h-5" />
                      Открыть репозиторий
                  </a>
              </div>

          </div>
      </div>
    </Transition>

  </div>
</template>

<style scoped>
/* Modal Transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-enter-from .relative {
  transform: scale(0.9) translateY(20px);
}
.modal-leave-to .relative {
  transform: scale(0.9) translateY(20px);
}

/* 3D CUBE STYLES */
.perspective-wrapper { perspective: 1000px; }
.cube-scene { width: 250px; height: 250px; position: relative; transform-style: preserve-3d; animation: float 6s ease-in-out infinite; }
.alfa-cube { width: 100%; height: 100%; position: absolute; transform-style: preserve-3d; animation: rotate 20s linear infinite; }

.cube-face {
  position: absolute; width: 250px; height: 250px;
  background: rgba(239, 49, 36, 0.05);
  border: 2px solid rgba(239, 49, 36, 0.4);
  display: flex; align-items: center; justify-content: center;
  font-size: 100px; font-weight: 900; color: #EF3124;
  backdrop-filter: blur(4px);
  box-shadow: 0 0 60px rgba(239, 49, 36, 0.1);
}

.face-front  { transform: rotateY(0deg) translateZ(125px); }
.face-back   { transform: rotateY(180deg) translateZ(125px); }
.face-right  { transform: rotateY(90deg) translateZ(125px); }
.face-left   { transform: rotateY(-90deg) translateZ(125px); }
.face-top    { transform: rotateX(90deg) translateZ(125px); }
.face-bottom { transform: rotateX(-90deg) translateZ(125px); }

.orbit-ring {
  position: absolute; border-radius: 50%; border: 1px solid #0B1F35;
  opacity: 0.1; transform: rotateX(70deg);
}
.ring-1 { width: 400px; height: 400px; animation: spin 15s linear infinite; }
.ring-2 { width: 600px; height: 600px; animation: spin 20s linear infinite reverse; }

@keyframes rotate { from { transform: rotateX(15deg) rotateY(0deg); } to { transform: rotateX(15deg) rotateY(360deg); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
@keyframes spin { from { transform: rotateX(70deg) rotateZ(0deg); } to { transform: rotateX(70deg) rotateZ(360deg); } }
</style>