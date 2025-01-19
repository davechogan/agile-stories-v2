import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '../views/StoryInput.vue'
import AgileReview from '../views/AgileReview.vue'
import TechReview from '../views/TechReview.vue'
import Estimates from '../views/Estimates.vue'
import TestTechReviewView from '../views/TestTechReviewView.vue'
import TestTechReview from '../views/TestTechReview.vue'
import TestAgileResults from '../views/TestAgileResults.vue'

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
    },
    {
      path: '/test-tech-review-view',
      name: 'test-tech-review-view',
      component: TestTechReviewView
    },
    {
      path: '/test-tech-review',
      name: 'test-tech-review',
      component: TestTechReview
    },
    {
      path: '/test-agile-results',
      name: 'test-agile-results',
      component: TestAgileResults
    },
  ]
})

export default router
