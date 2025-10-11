import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import RecordsView from '../views/RecordsView.vue'
import LoginPage from '../views/LoginPage.vue'
import EditorDashboard from '../views/EditorDashboard.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginPage },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/records',
    name: 'Records',
    component: RecordsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/editor-dashboard',
    name: 'EditorDashboard',
    component: EditorDashboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Navigation guard
router.beforeEach((to, from, next) => {
  const user= JSON.parse(localStorage.getItem('currentUser'))
  
  if (to.meta.requiresAuth && !user) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && user) {
    // Redirect logged-in users based on role
    if (user.role === 'admin') {
      next({ name: 'Dashboard' })
    } else {
      next({ name: 'EditorDashboard' })
    }
  } else {
    next()
  }
})

export default router
