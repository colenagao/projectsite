import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import About from '@/components/About.vue'
import Navbar from '@/components/Navbar.vue'
import Project from '@/components/Project.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/navbar',
      name: 'navbar',
      component: Navbar
    },
    {
      path: '/project',
      name: 'project',
      component: Project
    },
  ]
})

export default router