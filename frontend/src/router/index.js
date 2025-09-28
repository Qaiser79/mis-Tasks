import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import RecordsView from '../views/RecordsView.vue'

const routes= [
    { path: '/', name: 'Dashboard', component: DashboardView},
    {path: '/records', name: 'Records', component: RecordsView}
]

const router= createRouter({
    history: createWebHistory(),
    routes
})

export default router