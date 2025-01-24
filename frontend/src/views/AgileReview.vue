<template>
  <div class="test">
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
          <h2 class="page-title">Improved Title</h2>
          <div class="dark-panel mb-8">
            <textarea
              v-model="analysis.analysis.title"
              class="edit-field"
              rows="1"
            ></textarea>
          </div>

          <h2 class="page-title">Improved Story</h2>
          <div class="dark-panel mb-8">
            <textarea
              v-model="analysis.analysis.story"
              class="edit-field"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <h2 class="page-title">Acceptance Criteria</h2>
            <div class="criteria-list">
              <div v-if="analysis.analysis.acceptance_criteria"
                   v-for="(criterion, index) in analysis.analysis.acceptance_criteria" 
                   :key="index"
                   class="criteria-item">
                <v-textarea
                  :value="criterion"
                  @input="(e) => updateCriterion(index, e)"
                  variant="outlined"
                  auto-grow
                  rows="1"
                />
                <v-btn 
                  icon="mdi-delete" 
                  size="small"
                  color="error" 
                  variant="text"
                  @click="removeCriterion(index)"
                />
              </div>
              <v-btn 
                prepend-icon="mdi-plus"
                variant="text"
                @click="addCriterion"
                :disabled="!analysis.analysis.acceptance_criteria"
              >
                Add Criteria
              </v-btn>
            </div>
          </div>

          <!-- Single button for tech review -->
          <div class="action-buttons">
            <v-btn
              @click="requestTechnicalReview"
              color="primary"
              :loading="reviewing"
              :disabled="!canRequestReview || !analysis.analysis"
            >
              Request Technical Review
            </v-btn>
          </div>
        </div>
      </div>
      
      <!-- Right Column -->
      <div class="analysis-panel">
        <h3 class="panel-title">Suggestions</h3>
        <div class="dark-panel mb-8">
          <ul class="suggestions-list">
            <li v-for="(suggestion, index) in analysis.analysis.Suggestions || []"
                :key="index"
                class="suggestion-item">
              {{ suggestion }}
            </li>
          </ul>
        </div>

        <h3 class="panel-title">INVEST Analysis</h3>
        <div class="invest-grid">
          <div v-for="(item, index) in analysis.analysis.INVESTAnalysis || []"
               :key="index"
               class="invest-item">
            <div class="invest-header">
              <span class="invest-letter">{{ item.letter }}</span>
              <span class="invest-title">{{ item.title }}</span>
            </div>
            <div class="invest-content">{{ item.content }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { mockAnalysisResult } from '@/mocks/mockAnalysisData'
import { useStoryStore } from '@/stores/storyStore'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const storyStore = useStoryStore()
const analysis = ref(null)
const route = useRoute()
const error = ref(null)
const loading = ref(false)
const reviewing = ref(false)

onMounted(() => {
  fetchAnalysis()
})

// Comment out or remove the redirect logic
/*
watch(analysis, (newValue) => {
  if (!newValue) {
    router.push('/')
  }
})
*/

// Story editing
const editingStory = ref(false)
const editedStory = ref('')

const startEditingStory = () => {
  editedStory.value = mockAnalysisResult.analysis.story
  editingStory.value = true
}

const saveStory = () => {
  mockAnalysisResult.analysis.story = editedStory.value
  editingStory.value = false
}

const cancelEditStory = () => {
  editingStory.value = false
}

// Acceptance Criteria editing
const editingAC = ref(false)
const editedAC = ref('')

const startEditingAC = () => {
  editedAC.value = mockAnalysisResult.analysis.acceptance_criteria.join('\n')
  editingAC.value = true
}

const saveAC = () => {
  mockAnalysisResult.analysis.acceptance_criteria = editedAC.value
    .split('\n')
    .filter(line => line.trim()) // Remove empty lines
  editingAC.value = false
}

const cancelEditAC = () => {
  editingAC.value = false
}

// Parse INVEST analysis into structured data
const investAnalysis = [
  {
    letter: 'I',
    title: 'Independent',
    content: 'The user story is independent, as it does not seem to depend on any other user story for its implementation.'
  },
  {
    letter: 'N',
    title: 'Negotiable',
    content: 'The story is not very negotiable as it is not clear on what exactly the notification bell should do, or what exactly broadcasting a message entails.'
  },
  {
    letter: 'V',
    title: 'Valuable',
    content: 'The value to the user is not clearly stated. Why should the user care about this new notification bell?'
  },
  {
    letter: 'E',
    title: 'Estimable',
    content: 'The story is too vague to be reliably estimated. We don\'t know what "broadcasting a message" involves.'
  },
  {
    letter: 'S',
    title: 'Small',
    content: 'The story is not small, as it seems to involve several different features or functionalities.'
  },
  {
    letter: 'T',
    title: 'Testable',
    content: 'The acceptance criteria are too vague to be testable. What does it mean for everyone to "get it" and "read it"?'
  }
]

// Add this function to detect negative feedback
const isNegative = (content: string): boolean => {
  const negativeTerms = ['not', 'too vague', 'unclear', 'missing'];
  return negativeTerms.some(term => content.toLowerCase().includes(term));
}

const updateCriterion = (index, value) => {
  if (analysis.value?.analysis?.acceptance_criteria) {
    analysis.value.analysis.acceptance_criteria[index] = value
  }
}

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
    console.log('Requesting technical review for story:', storyId)
    
    const payload = {
      story_id: storyId,
      tenant_id: "test-tenant-001",
      version: 'AGILE_COACH',
      analysis: analysis.value.analysis
    }
    
    console.log('Sending tech review request:', payload)
    
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/stories/tech-review`,
      payload
    )
    
    console.log('Technical review response:', response.data)
    
    // Navigate to tech review page with correct path
    router.push(`/tech/${storyId}`)
    
  } catch (err) {
    console.error('Error requesting technical review:', err)
    if (err.response) {
      console.error('Error response:', err.response.data)
    }
    error.value = 'Failed to request technical review'
  } finally {
    reviewing.value = false
  }
}
</script>

<style scoped>
/* Copy all styles from OLD-AgileReview.vue */
.test {
  display: block;
  width: 100%;
}

.test > .two-column-layout {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
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
  padding-left: 1.5rem;
  position: relative;
  font-size: 1rem;
  line-height: 1.6;
}

.suggestion-item::before {
  content: "•";
  color: #FFA726;
  position: absolute;
  left: 0;
}

@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }
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
</style> 