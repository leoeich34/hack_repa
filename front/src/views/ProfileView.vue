<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import { useNotification } from '../composables/useNotification'
import {
  UserCircleIcon, BriefcaseIcon, BuildingOfficeIcon, CheckBadgeIcon,
  TrophyIcon, FireIcon, StarIcon, ClockIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const { show } = useNotification()
const loading = ref(false)

const form = ref({
  name: '',
  position: '',
  department: '',
  email: ''
})

onMounted(() => {
  if (authStore.user) {
    form.value.name = authStore.user.name || ''
    form.value.position = authStore.user.position || ''
    form.value.department = authStore.user.department || ''
    form.value.email = authStore.user.email || ''
  }
})

const save = async () => {
  loading.value = true
  try {
    await authStore.updateUserData(form.value)
    show('Профиль успешно обновлен', 'success')
  } catch (e) {
    show('Не удалось сохранить изменения', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="animate-fade-in-up pb-10 max-w-5xl mx-auto">

    <!-- HEADER -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-[#0B1F35] dark:text-white">Личный кабинет</h1>
      <p class="text-gray-500 mt-1 dark:text-gray-400">Управление учетной записью и статистика</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-6">

        <!-- LEFT COLUMN: ID CARD -->
        <div class="md:col-span-4">
            <div class="bg-white/70 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm relative overflow-hidden group dark:bg-white/5 dark:border-white/10">

                <!-- BACKGROUND DECOR -->
                <div class="absolute top-0 left-0 w-full h-32 bg-gradient-to-br from-[#EF3124] to-[#B91C10] opacity-90"></div>
                <div class="absolute top-4 right-4 text-white/20">
                    <TrophyIcon class="w-24 h-24 rotate-12" />
                </div>

                <!-- AVATAR -->
                <div class="relative mt-12 mb-4 flex justify-center">
                    <div class="w-28 h-28 rounded-full border-4 border-white dark:border-[#1f2937] shadow-xl overflow-hidden bg-white relative z-10">
                        <img
                            :src="`https://ui-avatars.com/api/?name=${form.name}&background=0B1F35&color=fff&size=256`"
                            class="w-full h-full object-cover"
                            alt="Avatar"
                        >
                    </div>
                    <!-- Status Badge -->
                    <div class="absolute bottom-1 right-[30%] translate-x-1/2 w-6 h-6 bg-green-500 border-2 border-white dark:border-[#1f2937] rounded-full z-20" title="Online"></div>
                </div>

                <div class="text-center mb-6">
                    <h2 class="text-xl font-bold text-[#0B1F35] dark:text-white">{{ form.name || 'Сотрудник' }}</h2>
                    <p class="text-sm text-gray-500 dark:text-gray-300">{{ form.position || 'Должность не указана' }}</p>
                    <div class="mt-2 inline-flex items-center px-3 py-1 bg-red-50 text-[#EF3124] text-xs font-bold rounded-full dark:bg-red-900/30 dark:text-red-400 border border-red-100 dark:border-red-900/50">
                        TOP PERFORMER
                    </div>
                </div>

                <!-- STATS GRID -->
                <div class="grid grid-cols-2 gap-3">
                    <div class="bg-white/50 p-3 rounded-xl border border-gray-100 dark:bg-white/5 dark:border-white/5 text-center">
                        <div class="text-gray-400 text-[10px] uppercase font-bold tracking-wider">Скоринг</div>
                        <div class="text-xl font-bold text-[#0B1F35] dark:text-white">1,240</div>
                    </div>
                    <div class="bg-white/50 p-3 rounded-xl border border-gray-100 dark:bg-white/5 dark:border-white/5 text-center">
                        <div class="text-gray-400 text-[10px] uppercase font-bold tracking-wider">Эффективность</div>
                        <div class="text-xl font-bold text-green-500">98%</div>
                    </div>
                </div>
            </div>

            <!-- ACHIEVEMENTS (Gamification) -->
            <div class="mt-6 bg-white/70 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm dark:bg-white/5 dark:border-white/10">
                <h3 class="font-bold text-[#0B1F35] mb-4 flex items-center gap-2 dark:text-white">
                    <StarIcon class="w-5 h-5 text-yellow-500" /> Достижения
                </h3>
                <div class="space-y-3">
                    <div class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition dark:hover:bg-white/5">
                        <div class="p-2 bg-orange-100 text-orange-600 rounded-lg dark:bg-orange-900/30"><FireIcon class="w-5 h-5" /></div>
                        <div>
                            <div class="text-sm font-bold text-[#0B1F35] dark:text-white">Рекордная неделя</div>
                            <div class="text-xs text-gray-500 dark:text-gray-400">Обработано >100 заявок</div>
                        </div>
                    </div>
                    <div class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition dark:hover:bg-white/5">
                        <div class="p-2 bg-blue-100 text-blue-600 rounded-lg dark:bg-blue-900/30"><ClockIcon class="w-5 h-5" /></div>
                        <div>
                            <div class="text-sm font-bold text-[#0B1F35] dark:text-white">Пунктуальность</div>
                            <div class="text-xs text-gray-500 dark:text-gray-400">100% аптайм</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- RIGHT COLUMN: EDIT FORM -->
        <div class="md:col-span-8">
            <div class="bg-white/70 backdrop-blur-md border border-white/60 p-8 rounded-3xl shadow-sm h-full dark:bg-white/5 dark:border-white/10">
                <div class="flex justify-between items-center mb-8">
                    <h3 class="font-bold text-xl text-[#0B1F35] dark:text-white flex items-center gap-2">
                        <UserCircleIcon class="w-6 h-6 text-[#EF3124]" />
                        Редактирование профиля
                    </h3>
                </div>

                <form @submit.prevent="save" class="space-y-6">

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Имя -->
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-gray-500 uppercase tracking-wide dark:text-gray-400">ФИО</label>
                            <input v-model="form.name" type="text"
                                class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition dark:bg-white/5 dark:border-white/10 dark:text-white dark:focus:ring-white/10">
                        </div>

                        <!-- Email (Readonly) -->
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-gray-500 uppercase tracking-wide dark:text-gray-400">Email (Корпоративный)</label>
                            <input v-model="form.email" type="email" readonly
                                class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-500 cursor-not-allowed dark:bg-white/5 dark:border-white/5 dark:text-gray-500">
                        </div>

                        <!-- Должность -->
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-gray-500 uppercase tracking-wide dark:text-gray-400">Должность</label>
                            <div class="relative">
                                <BriefcaseIcon class="w-5 h-5 text-gray-400 absolute left-3 top-3.5" />
                                <input v-model="form.position" type="text"
                                    class="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition dark:bg-white/5 dark:border-white/10 dark:text-white dark:focus:ring-white/10">
                            </div>
                        </div>

                        <!-- Отдел -->
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-gray-500 uppercase tracking-wide dark:text-gray-400">Департамент</label>
                            <div class="relative">
                                <BuildingOfficeIcon class="w-5 h-5 text-gray-400 absolute left-3 top-3.5" />
                                <input v-model="form.department" type="text"
                                    class="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition dark:bg-white/5 dark:border-white/10 dark:text-white dark:focus:ring-white/10">
                            </div>
                        </div>
                    </div>

                    <!-- BIO / Notes -->
                    <div class="space-y-1">
                        <label class="text-xs font-bold text-gray-500 uppercase tracking-wide dark:text-gray-400">Заметки / Статус</label>
                        <textarea rows="4" placeholder="Напишите что-нибудь о себе..."
                            class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-100 focus:border-[#EF3124] outline-none transition resize-none dark:bg-white/5 dark:border-white/10 dark:text-white dark:focus:ring-white/10"></textarea>
                    </div>

                    <div class="pt-6 border-t border-gray-100 dark:border-white/10 flex justify-end">
                        <button
                            type="submit"
                            :disabled="loading"
                            class="px-8 py-3 bg-[#0B1F35] text-white font-bold rounded-xl hover:bg-black transition shadow-lg shadow-gray-200 dark:shadow-none flex items-center gap-2 disabled:opacity-70 dark:bg-white dark:text-[#0B1F35] dark:hover:bg-gray-200"
                        >
                            <span v-if="loading" class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full"></span>
                            <span v-else>Сохранить изменения</span>
                            <CheckBadgeIcon v-if="!loading" class="w-5 h-5" />
                        </button>
                    </div>

                </form>
            </div>
        </div>

    </div>
  </div>
</template>