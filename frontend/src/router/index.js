import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '../views/StoryInput.vue'
import AgileReview from '../views/AgileReview.vue'
import TechReview from '../views/TechReview.vue'
import Estimates from '../views/Estimates.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: StoryInput
    },
    {
      path: '/agile',
      name: 'agile',
      component: AgileReview
    },
    {
      path: '/tech',
      name: 'tech',
      component: TechReview
    },
    {
      path: '/estimates',
      name: 'estimates',
      component: Estimates
    }
  ]
})

export default router
