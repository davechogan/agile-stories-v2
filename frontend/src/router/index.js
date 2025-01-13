import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '../views/StoryInput.vue'
import AgileResults from '../views/AgileResults.vue'
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
      component: AgileResults
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
