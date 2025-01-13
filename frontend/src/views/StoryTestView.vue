<template>
  <div class="story-test">
    <h2>Story Generator Test</h2>
    <div class="story-input">
      <textarea 
        v-model="storyInput"
        placeholder="Enter your user story description..."
        rows="4"
      ></textarea>
      <button 
        @click="generateStory"
        :disabled="isProcessing"
      >
        {{ isProcessing ? 'Processing...' : 'Generate Story' }}
      </button>
    </div>
    
    <div v-if="generatedStory" class="story-output">
      <h3>Generated Story</h3>
      <pre>{{ generatedStory }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const storyInput = ref('')
const generatedStory = ref('')
const isProcessing = ref(false)

const generateStory = async () => {
  isProcessing.value = true
  try {
    // TODO: Implement API call to backend
    // For now, just simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    generatedStory.value = `As a user\nI want to ${storyInput.value}\nSo that I can improve my workflow`
  } catch (error) {
    console.error('Error generating story:', error)
  } finally {
    isProcessing.value = false
  }
}
</script> 