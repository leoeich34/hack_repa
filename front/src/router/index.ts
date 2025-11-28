import { createRouter, createWebHistory } from 'vue-router'
// Импортируем наши реальные .vue файлы
import HomeView from '../views/HomeView.vue'
import ClientDashboard from '../views/ClientDashboard.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/client/:id',
      name: 'dashboard',
      component: ClientDashboard
    }
  ]
})

export default router