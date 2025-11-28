<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MainLayout from '../layouts/MainLayout.vue'
import { useAuthStore } from '../store/auth'
import { useNotification }  from '../composables/useNotification'
import {
  UserCircleIcon,
  BriefcaseIcon,
  BuildingOfficeIcon,
  CheckBadgeIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const { show } = useNotification()
const loading = ref(false)

// Форма
const form = ref({
  name: '',
  position: '',
  department: ''
})

// Заполняем форму текущими данными
onMounted(() => {
  if (authStore.user) {
    form.value.name = authStore.user.name || ''
    form.value.position = authStore.user.position || ''
    form.value.department = authStore.user.department || ''
  }
})

// Сохранение
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
    <div class="max-w-4xl mx-auto animate-fade-in-up">

      <!-- Заголовок -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-[#0B1F35]">Профиль сотрудника</h1>
        <p class="text-gray-500">Управление личными данными и настройками доступа</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

        <!-- Левая колонка: Карточка Аватара -->
        <div class="md:col-span-1">
          <div class="bg-white/70 backdrop-blur-md border border-white p-6 rounded-2xl shadow-sm text-center relative overflow-hidden group">

            <!-- Декор на фоне -->
            <div class="absolute top-0 left-0 w-full h-24 bg-gradient-to-b from-red-50 to-transparent"></div>

            <!-- Аватар -->
            <div class="relative inline-block mb-4 mt-4">
              <img
                :src="`https://ui-avatars.com/api/?name=${form.name}&background=EF3124&color=fff&size=128`"
                class="w-24 h-24 rounded-full border-4 border-white shadow-lg relative z-10"
                alt="Avatar"
              >
              <!-- Статус "Онлайн" -->
              <div class="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-2 border-white rounded-full z-20" title="Online"></div>
            </div>

            <h2 class="font-bold text-xl text-[#0B1F35]">{{ form.name || 'Сотрудник' }}</h2>
            <p class="text-sm text-gray-500 mb-4">{{ form.position || 'Должность не указана' }}</p>

            <!-- Геймификация -->
            <div class="bg-gray-50 rounded-xl p-3 text-left">
               <div class="text-xs text-gray-400 uppercase font-bold mb-2">Статистика</div>
               <div class="flex justify-between items-center text-sm mb-1">
                  <span>Скоринг:</span>
                  <span class="font-bold">142</span>
               </div>
               <div class="flex justify-between items-center text-sm">
                  <span>Уровень:</span>
                  <span class="font-bold text-[#EF3124]">Pro</span>
               </div>
               <!-- XP Bar -->
               <div class="w-full h-1.5 bg-gray-200 rounded-full mt-2 overflow-hidden">
                  <div class="h-full bg-[#EF3124] w-[70%]"></div>
               </div>
            </div>

          </div>
        </div>

        <!-- Правая колонка: Форма -->
        <div class="md:col-span-2">
          <div class="bg-white/70 backdrop-blur-md border border-white p-8 rounded-2xl shadow-sm">
            <h3 class="font-bold text-lg mb-6 flex items-center gap-2">
              <UserCircleIcon class="w-6 h-6 text-[#EF3124]" />
              Личные данные
            </h3>

            <form @submit.prevent="save" class="space-y-6">

              <!-- Имя -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">ФИО</label>
                <div class="relative">
                   <input v-model="form.name" type="text" class="w-full pl-4 pr-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:border-[#EF3124] focus:ring-2 focus:ring-red-100 outline-none transition">
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Должность -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Должность</label>
                  <div class="relative">
                     <BriefcaseIcon class="w-5 h-5 text-gray-400 absolute left-3 top-3.5" />
                     <input v-model="form.position" type="text" placeholder="Например: Менеджер" class="w-full pl-10 pr-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:border-[#EF3124] focus:ring-2 focus:ring-red-100 outline-none transition">
                  </div>
                </div>

                <!-- Отдел -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Отдел</label>
                  <div class="relative">
                     <BuildingOfficeIcon class="w-5 h-5 text-gray-400 absolute left-3 top-3.5" />
                     <input v-model="form.department" type="text" placeholder="Например: Продажи" class="w-full pl-10 pr-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:border-[#EF3124] focus:ring-2 focus:ring-red-100 outline-none transition">
                  </div>
                </div>
              </div>

              <div class="pt-4 border-t border-gray-100">
                 <button
                    type="submit"
                    :disabled="loading"
                    class="px-8 py-3 bg-[#0B1F35] text-white font-bold rounded-xl hover:bg-black transition shadow-lg flex items-center gap-2 disabled:opacity-70"
                 >
                    <span v-if="loading" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
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