import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'
import HomeView from '../views/HomeView.vue'
import ClientDashboard from '../views/ClientDashboard.vue'
import WelcomeView from '../views/WelcomeView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'
import ClientsView from '../views/ClientsView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import SettingsView from '../views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      // ВАЖНО: Добавили layout: 'main'
      meta: { requiresAuth: true, layout: 'main' }
    },
    {
      path: '/clients',
      name: 'clients',
      component: ClientsView,
      meta: { requiresAuth: true, layout: 'main' }
    },
    {
      path: '/client/:id',
      name: 'dashboard',
      component: ClientDashboard,
      meta: { requiresAuth: true, layout: 'main' }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true, layout: 'main' }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
      meta: { requiresAuth: true, layout: 'main' }
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: { requiresAuth: true, layout: 'main' }
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: WelcomeView
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView
    }
  ]
})

// GUARD: Проверка перед каждым переходом
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token

  // Если маршрут требует входа, а мы не вошли -> на Welcome
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/welcome')
  }
  // Если мы уже вошли и пытаемся попасть на Welcome/Auth -> на Главную
  else if ((to.path === '/welcome' || to.path === '/auth') && isAuthenticated) {
    next('/')
  }
  else {
    next()
  }
})

export default router