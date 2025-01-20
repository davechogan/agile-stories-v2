<template>
  <div class="p-4">
    <div v-if="loading">Loading...</div>
    
    <div v-else-if="error">
      Error: {{ error }}
      <v-btn @click="router.push('/')" color="primary">Return Home</v-btn>
    </div>
    
    <div v-else-if="results">
      <pre>{{ JSON.stringify(results, null, 2) }}</pre>
    </div>
    
    <div v-else>
      <p>No results available</p>
      <v-btn @click="router.push('/')" color="primary">Return Home</v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStoryStore } from '@/stores/storyStore'
import { useRouter } from 'vue-router'

const storyStore = useStoryStore()
const router = useRouter()
const loading = ref(true)
const error = ref(null)
const results = ref(null)

onMounted(async () => {
  console.log('AgileReview mounted, currentStory:', storyStore.currentStory)
  
  try {
    if (!storyStore.currentStory?.story_id) {
      throw new Error('No story data available')
    }

    const { story_id, token } = storyStore.currentStory
    console.log('Fetching story:', story_id)

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/stories/${story_id}?version=AGILE_COACH`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )

    if (!response.ok) {
      throw new Error('Failed to fetch story results')
    }

    results.value = await response.json()
    console.log('Fetched results:', results.value)
    
  } catch (err) {
    console.error('Error:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script> 