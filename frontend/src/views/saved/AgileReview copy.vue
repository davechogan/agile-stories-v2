<template>
  <div class="two-column-layout">
    <!-- Left Column -->
    <div class="primary-content-wrapper">
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
      
      <div v-else class="primary-content">
        <div class="story-section">
          <h2>{{ analysis.analysis.title }}</h2>
          <div class="editable-content">
            <p>{{ analysis.analysis.story }}</p>
          </div>
          
          <h3>Acceptance Criteria</h3>
          <div v-for="(criterion, index) in analysis.analysis.acceptance_criteria"
               :key="index"
               class="criteria-item editable-content">
            <v-textarea
              :value="criterion"
              @input="(e) => updateCriterion(index, e)"
              variant="outlined"
              auto-grow
              rows="1"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Right Column -->
    <div class="analysis-panel">
      <!-- INVEST Analysis -->
      <div v-if="analysis?.analysis?.INVESTAnalysis">
        <h3>INVEST Analysis</h3>
        <div class="invest-grid">
          <div v-for="(item, index) in analysis.analysis.INVESTAnalysis"
               :key="index"
               :class="['invest-item', { warning: isNegative(item.content) }]">
            <div class="invest-header">
              <span class="invest-letter">{{ item.letter }}</span>
              <h4>{{ item.title }}</h4>
            </div>
            <p>{{ item.content }}</p>
          </div>
        </div>
      </div>
      
      <!-- Suggestions -->
      <div v-if="analysis?.analysis?.Suggestions">
        <h3>Suggestions</h3>
        <div class="suggestions-list">
          <div v-for="(suggestion, index) in analysis.analysis.Suggestions"
               :key="index"
               class="suggestion-item">
            <p class="suggestion-content">{{ suggestion }}</p>
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
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useRoute } from 'vue-router'

const router = useRouter()
const storyStore = useStoryStore()
const analysis = ref(null)
const route = useRoute()
const error = ref(null)
const loading = ref(false)

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
</script>

<style>
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: 100vh;
  position: relative;
}

.primary-content-wrapper {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.primary-content {
  position: sticky;
  top: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
  flex-grow: 1;
}

.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.editable-content {
  position: relative;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  transition: all 0.3s ease;
}

.edit-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.editable-content:hover .edit-btn {
  opacity: 1;
}

.story-section h3 {
  color: #64B5F6;
  margin-top: 2rem;
}

.story-section h3:first-child {
  margin-top: 0;
}

.editable-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: rgba(255, 255, 255, 0.87);
  font-family: inherit;
  margin: 0;
  line-height: 1.6;
}

.editable-content ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.editable-content li {
  color: rgba(255, 255, 255, 0.87);
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}

.editable-content li:before {
  content: "•";
  color: #64B5F6;
  position: absolute;
  left: 0;
}

/* Keep existing invest-grid styles */
.invest-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-top: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }
  
  .primary-content {
    position: relative;
    top: 0;
    max-height: none;
  }
  
  .analysis-panel {
    margin-top: 2rem;
  }
}

/* Updated Analysis Panel Styles */
.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.analysis-panel h3 {
  color: #64B5F6;
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

/* INVEST Grid Refinements */
.invest-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.invest-item {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1.25rem;
  border-left: 3px solid #64B5F6;
  transition: transform 0.2s ease;
}

.invest-item.warning {
  border-left-color: #FFA726;
  background: rgba(255, 167, 38, 0.1);
}

.invest-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.invest-letter {
  background: #64B5F6;
  color: #1E1E1E;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 0.75rem;
}

.warning .invest-letter {
  background: #FFA726;
}

/* Suggestions Refinements */
.suggestions-list {
  display: grid;
  gap: 1rem;
}

.suggestion-item {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1.25rem;
  border-left: 3px solid #64B5F6;
}

.suggestion-header {
  color: #64B5F6;
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.suggestion-content {
  color: rgba(255, 255, 255, 0.87);
  line-height: 1.6;
}

/* Hover effects */
.invest-item:hover, 
.suggestion-item:hover {
  transform: translateY(-2px);
}

/* Responsive adjustments */
@media (max-width: 1400px) {
  .invest-grid {
    grid-template-columns: 1fr;
  }
}

.edit-textarea {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

/* Style the textarea */
:deep(.v-field__input) {
  color: rgba(255, 255, 255, 0.87) !important;
  font-family: inherit !important;
  line-height: 1.6 !important;
}

:deep(.v-field) {
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.sticky-footer {
  position: fixed;
  bottom: 0;
  width: calc(50% - 2rem);
  background: linear-gradient(
    to top,
    rgba(30, 30, 30, 1) 0%,
    rgba(30, 30, 30, 0.9) 70%,
    rgba(30, 30, 30, 0) 100%
  );
  padding: 1rem 0;
  margin-top: -4rem;
  pointer-events: none;
  z-index: 10;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  pointer-events: auto;
  padding: 0 2rem;
}

.footer-hint {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

/* Update responsive styles */
@media (max-width: 1024px) {
  .primary-content {
    position: relative;
    top: 0;
    max-height: none;
  }
  
  .sticky-footer {
    position: fixed;
    width: 100%;
    left: 0;
    right: 0;
    margin-top: 0;
  }
}
</style> 