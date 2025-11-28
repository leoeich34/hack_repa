import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  // Загружаем из localStorage или ставим дефолт
  const theme = ref(localStorage.getItem('theme') || 'light')
  const compactMode = ref(localStorage.getItem('compactMode') === 'true')

  // Уведомления (пока локально)
  const notifications = ref({
    email: true,
    push: false,
    weeklyReport: true
  })

  // ЛОГИКА ТЕМЫ
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    applyTheme()
  }

  const applyTheme = () => {
    // Добавляем класс 'dark' к тегу <html>
    if (theme.value === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('theme', theme.value)
  }

  // ЛОГИКА КОМПАКТНОСТИ
  const toggleCompact = () => {
    compactMode.value = !compactMode.value
    localStorage.setItem('compactMode', String(compactMode.value))
  }

  // При инициализации сразу применяем тему
  applyTheme()

  return {
    theme,
    compactMode,
    notifications,
    toggleTheme,
    toggleCompact
  }
})