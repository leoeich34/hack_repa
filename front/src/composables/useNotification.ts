import { ref } from 'vue'

const isVisible = ref(false)
const message = ref('')
const type = ref<'success' | 'error'>('success')

export function useNotification() {
  const show = (msg: string, msgType: 'success' | 'error' = 'success') => {
    message.value = msg
    type.value = msgType
    isVisible.value = true

    // Скрываем через 3 секунды
    setTimeout(() => {
      isVisible.value = false
    }, 3000)
  }

  return {
    isVisible,
    message,
    type,
    show
  }
}