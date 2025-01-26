<template>
  <div class="test" :class="{ 'fade-in': mounted, 'fade-out': isExiting }">
    <div v-if="loading" class="loading">
      <v-progress-circular indeterminate />
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <v-btn to="/" color="primary">Return to Story Input</v-btn>
    </div>
    
    <div v-else-if="!analysis?.analysis" class="no-data">
      <p>No analysis data available. Please submit a story first.</p>
      <v-btn to="/" color="primary">Return to Story Input</v-btn>
    </div>
    
    <div v-else class="two-column-layout">
      <!-- Left Column -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2 class="page-title">Agile Review Modifications</h2>
          
          <EditableSection
            v-model="analysis.analysis.title"
            title="Story Title"
            type="single-line"
            placeholder="Enter story title..."
          />
          
          <EditableSection
            v-model="analysis.analysis.story"
            title="User Story"
            type="text"
            placeholder="Describe the user story..."
          />
          
          <EditableSection
            v-model="analysis.analysis.acceptance_criteria"
            title="Acceptance Criteria"
            type="list"
            placeholder="Enter each criterion on a new line..."
          />
        </div>
      </div>
      
      <!-- Right Column -->
      <div class="analysis-panel">
        <h2 class="page-title">Suggestions</h2>
        <div class="suggestions-list">
          <div v-for="(suggestion, index) in analysis.analysis.Suggestions || []"
               :key="index"
               class="suggestion-item">
            {{ suggestion }}
          </div>
        </div>

        <h2 class="page-title mt-8">INVEST Analysis</h2>
        <div class="invest-grid">
          <div v-for="(item, index) in analysis.analysis.INVESTAnalysis || []"
               :key="index"
               class="invest-item">
            <div class="invest-header">
              <div class="invest-letter">{{ item.letter }}</div>
              <div class="invest-title">{{ item.title }}</div>
            </div>
            <div class="invest-content">{{ item.content }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Replace the current action-buttons div with this sticky footer -->
    <div class="sticky-footer">
      <div class="footer-content">
        <div class="footer-buttons">
          <v-btn 
            color="success" 
            class="mr-4"
            @click="acceptAgileReview"
          >
            ACCEPT AGILE REVIEW
          </v-btn>
          <v-btn 
            color="primary"
            @click="requestTechnicalReview"
            :loading="reviewing"
            :disabled="!canRequestReview || !analysis.analysis"
          >
            REQUEST TECH REVIEW
          </v-btn>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showTransition" class="animation-container">
        <video 
          ref="videoPlayer"
          class="background-video" 
          autoplay 
          loop 
          muted 
          playsinline
        >
          <source src="/videos/AdobeStock_910543395.mp4" type="video/mp4">
          <source src="/videos/AdobeStock_910543395.webm" type="video/webm">
        </video>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import EditableSection from '@/components/EditableSection.vue'

const router = useRouter()
const analysis = ref(null)
const route = useRoute()
const error = ref(null)
const loading = ref(false)
const reviewing = ref(false)
const mounted = ref(false)
const showTransition = ref(false)
const isExiting = ref(false)
const videoPlayer = ref(null)

onMounted(() => {
  fetchAnalysis()
  setTimeout(() => {
    mounted.value = true
  }, 100)
})

const fetchAnalysis = async () => {
  loading.value = true
  error.value = null
  analysis.value = null // Reset analysis before fetching
  
  try {
    const storyId = route.params.id
    console.log('Starting fetchAnalysis with storyId:', storyId)
    
    const url = `${import.meta.env.VITE_API_URL}/stories/${storyId}?version=AGILE_COACH`
    console.log('Making GET request to:', url)
    
    const response = await axios.get(url)
    console.log('Response:', response.data)
    
    if (!response.data?.analysis) {
      throw new Error('Invalid data structure received')
    }
    
    analysis.value = response.data
    console.log('Set analysis value:', analysis.value)
    
  } catch (err) {
    console.error('Error in fetchAnalysis:', err)
    if (err.response) {
      console.error('Error response:', err.response.data)
    }
    error.value = err.message || 'Failed to load analysis'
  } finally {
    loading.value = false
  }
}

// Compute if we can request a review
const canRequestReview = computed(() => {
  if (!analysis.value || !analysis.value.analysis) return false
  
  return analysis.value.analysis.title && 
         analysis.value.analysis.story && 
         analysis.value.analysis.acceptance_criteria?.length > 0
})

const requestTechnicalReview = async () => {
  reviewing.value = true
  
  try {
    const storyId = route.params.id
    const payload = {
      story_id: storyId,
      tenant_id: "test-tenant-001",
      version: 'AGILE_COACH',
      analysis: analysis.value.analysis
    }
    
    console.log('Sending tech review request:', payload)
    
    // Show transition immediately
    showTransition.value = true
    isExiting.value = false
    
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/stories/tech-review`,
      payload
    )
    
    console.log('Technical review response:', response.data)
    
    // Start fading out after response
    isExiting.value = true
    
    // Wait for fade out animation before hiding video and navigating
    setTimeout(async () => {
      showTransition.value = false
      await router.push(`/tech/${storyId}`)
    }, 1000)
    
  } catch (err) {
    console.error('Error requesting technical review:', err)
    showTransition.value = false
    isExiting.value = false
    error.value = 'Failed to request technical review'
  } finally {
    reviewing.value = false
  }
}

const acceptAgileReview = async () => {
  try {
    // Add your accept logic here
    console.log('Accepting agile review')
    // Could navigate to next step or show confirmation
  } catch (error) {
    console.error('Error accepting agile review:', error)
  }
}

const isNegative = (content: string): boolean => {
  const negativeTerms = ['not', 'too vague', 'unclear', 'missing']
  return negativeTerms.some(term => content.toLowerCase().includes(term))
}
</script>

<style scoped>
/* Base layout */
.two-column-layout {
  display: grid !important; /* Force grid display */
  grid-template-columns: 1fr 1fr !important; /* Force two columns by default */
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

/* Content panels */
.primary-content-wrapper,
.analysis-panel {
  background: rgb(18, 18, 18);
  position: relative;
  z-index: 1;
}

/* Mobile responsive adjustments */
@media (max-width: 960px) {
  .two-column-layout {
    grid-template-columns: 1fr !important; /* Force single column */
    gap: 1rem;
    padding: 1rem;
    padding-bottom: 80px;
  }

  .primary-content-wrapper,
  .analysis-panel {
    width: 100% !important; /* Force full width */
    margin-bottom: 1rem;
  }

  .primary-content {
    padding-bottom: 80px;
  }

  .analysis-panel {
    margin-bottom: 80px;
  }

  .button-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(18, 18, 18, 0.95);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1rem;
    z-index: 1000;
    display: flex;
    justify-content: center;
  }
}

/* Additional small screen optimizations */
@media (max-width: 360px) {
  .two-column-layout {
    padding: 0.8rem;
  }

  .button-container {
    padding: 0.8rem;
  }
}

.test {
  display: block;
  width: 100%;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.fade-in {
  opacity: 1;
}

.test.fade-out {
  opacity: 0;
}

.primary-content-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.primary-content {
  flex: 1;
  padding-bottom: 5rem;
}

.story-form {
  background: rgba(30, 30, 30, 0.5);
  border-radius: 8px;
  padding: 1.5rem;
}

.page-title {
  color: #64B5F6;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 500;
}

.panel-title {
  color: #64B5F6;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.invest-grid {
  flex: 1;
  overflow-y: auto;
}

.invest-item {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 1rem;
  border-left: 4px solid #FFA726;
  margin-bottom: 0.5rem;
}

.invest-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.invest-letter {
  background: #FFA726;
  color: black;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.invest-title {
  font-size: 1.2rem;
  font-weight: 500;
}

.invest-content {
  color: rgba(255, 255, 255, 0.87);
  line-height: 1.6;
}

.criteria-item {
  display: flex;
  align-items: start;
  gap: 8px;
  margin-bottom: 8px;
}

.criteria-list {
  margin-bottom: 1rem;
}

/* Target Vuetify input components */
:deep(.v-field) {
  border-radius: 4px !important;
  padding: 0 !important;
}

:deep(.v-text-field),
:deep(.v-textarea) {
  width: 100% !important;
  margin-bottom: 0.75rem !important;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestion-item {
  margin-bottom: 1rem;
  font-size: 1rem;
  line-height: 1.6;
  background: rgba(33, 150, 243, 0.1);
  padding: 1.5rem;
  margin-bottom: 0.75rem;
  color: rgba(255, 255, 255, 0.87);
}

.edit-field {
  width: 100%;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: white;
  padding: 8px;
  font-size: 1rem;
  line-height: 1.6;
  resize: vertical;
}

.edit-field:focus {
  outline: none;
  border-color: #64B5F6;
}

.button-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.mb-8 {
  margin-bottom: 2rem;
}

.action-buttons {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.dark-panel {
  background: #333;
  padding: 1rem;
  margin: 1rem 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-size: 0.8rem;
}

.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(18, 18, 18, 0.9);
  padding: 1rem;
  z-index: 100;
}

.footer-content {
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
}

.footer-buttons {
  display: flex;
  gap: 1rem;
}

.animation-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.9);
  z-index: 1000;
}

.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 