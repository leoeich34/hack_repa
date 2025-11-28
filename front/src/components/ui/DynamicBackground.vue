<template>
  <!-- Базовый фон: Светло-серый (Light) / Глубокий Темно-синий (Dark) -->
  <div class="fixed inset-0 overflow-hidden pointer-events-none -z-10 bg-[#F3F4F5] dark:bg-[#060e1a] transition-colors duration-500">

    <!-- ГРАДИЕНТ (Пелена сверху) -->
    <!-- Light: Белый туман сверху вниз -->
    <!-- Dark: Полностью прозрачный (чтобы не было белой пелены) или легкий черный градиент -->
    <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-white via-white/80 to-transparent dark:from-[#060e1a] dark:via-[#060e1a]/50 dark:to-transparent opacity-90 dark:opacity-100 transition-colors duration-500"></div>

    <!-- ШАР 1 (Красный) -->
    <!-- Light: mix-blend-multiply (для сочности на белом) -->
    <!-- Dark: dark:mix-blend-screen (для свечения на черном) + увеличили opacity -->
    <div class="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-[#EF3124] rounded-full filter blur-[80px] animate-blob
                mix-blend-multiply opacity-20
                dark:mix-blend-screen dark:opacity-30"></div>

    <!-- ШАР 2 (Оранжевый) -->
    <div class="absolute top-[-10%] right-[-10%] w-[50vw] h-[50vw] bg-orange-400 rounded-full filter blur-[80px] animate-blob animation-delay-2000
                mix-blend-multiply opacity-20
                dark:mix-blend-screen dark:opacity-30"></div>

    <!-- ШАР 3 (Синий - глубина) -->
    <div class="absolute -bottom-32 left-[20%] w-[60vw] h-[60vw] bg-blue-200 rounded-full filter blur-[100px] animate-blob animation-delay-4000
                mix-blend-multiply opacity-30
                dark:bg-blue-900 dark:mix-blend-screen dark:opacity-20"></div>

    <!-- ШУМ (Текстура) -->
    <!-- В темной теме делаем шум чуть менее заметным -->
    <div class="absolute inset-0 opacity-[0.03] dark:opacity-[0.05] dark:invert"
         style="background-image: url('data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E');">
    </div>
  </div>
</template>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 10s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
</style>