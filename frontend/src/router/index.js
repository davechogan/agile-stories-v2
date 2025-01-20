import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '../views/StoryInput.vue'
import AgileReview from '../views/AgileReview.vue'
import TechReview from '../views/TechReview.vue'
import Estimates from '../views/Estimates.vue'
import { useStoryStore } from '@/stores/storyStore'

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
      name: 'agile-review',
      component: AgileReview,
      beforeEnter: (to, from, next) => {
        const storyStore = useStoryStore()
        console.log('Navigation guard checking story:', storyStore.currentStory)
        
        if (!storyStore.currentStory?.story_id) {
          console.log('No story_id found, redirecting to /')
          next('/')
        } else {
          console.log('Story found, allowing navigation to /agile')
          next()
        }
      }
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

// Handle navigation from workflow_signal_handler
window.addEventListener('message', (event) => {
  if (event.data.action === 'NAVIGATE') {
    router.push(event.data.path)
  }
})

export default router
