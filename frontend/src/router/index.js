import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '../views/StoryInput.vue'
import AgileReview from '../views/AgileReview.vue'
import TechReview from '../views/TechReview.vue'
import Estimates from '../views/Estimates.vue'
import TestTechReviewView from '../views/TestTechReviewView.vue'
import TestTechReview from '../views/TestTechReview.vue'
import TestAgileResults from '../views/TestAgileResults.vue'
import Settings from '@/views/Settings.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'story-input',
      component: StoryInput
    },
    {
      path: '/agile',
      name: 'agile',
      component: AgileReview
    },
    {
      path: '/agile/:id',
      name: 'agile-review',
      component: AgileReview,
      props: true
    },
    {
      path: '/tech',
      name: 'tech',
      component: TechReview
    },
    {
      path: '/tech/:id',
      name: 'tech-review',
      component: TechReview,
      props: true
    },
    {
      path: '/estimates/:id',
      name: 'estimates',
      component: Estimates,
      props: true
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
    {
      path: '/settings',
      component: Settings
    }
  ]
})

// Handle navigation from workflow_signal_handler
window.addEventListener('message', (event) => {
  if (event.data.action === 'NAVIGATE') {
    router.push(event.data.path)
  }
})

export default router
