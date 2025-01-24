<template>
  <div class="tech-review">
    <!-- Debug panel -->
    <div v-if="isDev" style="background: #333; padding: 10px; margin: 10px;">
      <p>Debug Info:</p>
      <p>Loading: {{ loading }}</p>
      <p>Has Error: {{ !!error }}</p>
      <p>Error Message: {{ error }}</p>
      <p>Has Data: {{ !!storyData }}</p>
      <pre>{{ JSON.stringify(storyData, null, 2) }}</pre>
    </div>

    <div v-if="loading" class="loading-state">
      <v-progress-circular indeterminate color="primary" />
      <p>Loading technical review...</p>
    </div>

    <div v-else-if="error" class="error-state dark-panel">
      <p>{{ error }}</p>
      <v-btn to="/" color="primary" class="mt-4">Return to Story Input</v-btn>
    </div>

    <div v-else-if="storyData" class="two-column-layout">
      <!-- Left Column -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h3>Technical Review Modifications</h3>
          
          <section class="criteria-section">
            <h4>User Story</h4>
            <div class="dark-panel">
              {{ storyData?.content?.story_text }}
            </div>
          </section>

          <section class="criteria-section">
            <h4>Acceptance Criteria</h4>
            <div class="criteria-list">
              <div v-for="(criterion, index) in storyData?.content?.acceptance_criteria" 
                  :key="index"
                  class="criteria-item">
                <span class="bullet">•</span>
                {{ criterion }}
              </div>
            </div>
          </section>

          <section class="implementation-section">
            <h4>Selected Implementation Details</h4>
            <div v-if="!selectedTasks?.length" class="dark-panel">
              <em>No implementation details added yet. Select from the sections below.</em>
            </div>
            <div v-else class="task-list">
              <div v-for="task in selectedTasks" 
                  :key="task.id" 
                  class="task-item"
                  @click="toggleTask(task)">
                <v-icon :icon="task.icon" color="primary" class="mr-2" />
                {{ task.text }}
              </div>
            </div>
          </section>

          <section class="implementation-section">
            <h4>Frontend</h4>
            <div class="task-list">
              <div v-for="task in frontendTasks" 
                  :key="task.id" 
                  class="task-item selectable"
                  @click="toggleTask(task)">
                <v-icon icon="mdi-code-tags" color="primary" class="mr-2" />
                {{ task.text }}
              </div>
            </div>
          </section>

          <section class="implementation-section">
            <h4>Backend</h4>
            <div class="task-list">
              <div v-for="task in backendTasks" 
                  :key="task.id" 
                  class="task-item selectable"
                  @click="toggleTask(task)">
                <v-icon icon="mdi-server" color="primary" class="mr-2" />
                {{ task.text }}
              </div>
            </div>
          </section>

          <section class="implementation-section">
            <h4>Database</h4>
            <div class="task-list">
              <div v-for="task in databaseTasks" 
                  :key="task.id" 
                  class="task-item selectable"
                  @click="toggleTask(task)">
                <v-icon icon="mdi-database" color="primary" class="mr-2" />
                {{ task.text }}
              </div>
            </div>
          </section>
        </div>
        
        <div class="footer-buttons">
          <v-btn 
            color="success" 
            class="mr-4"
            @click="acceptTechReview"
          >
            ACCEPT TECH REVIEW
          </v-btn>
          <v-btn 
            color="primary"
            @click="submitForEstimation"
          >
            SEND FOR ESTIMATION
          </v-btn>
        </div>
      </div>

      <!-- Right Column -->
      <div class="analysis-panel">
        <h3 class="panel-title">Technical Analysis</h3>
        <div class="tech-analysis-grid">
          <div v-for="(analysis, key) in storyData?.analysis?.TechnicalAnalysis || {}"
               :key="key"
               class="tech-analysis-item dark-panel">
            <div class="analysis-header">
              <h4>{{ key }}</h4>
              <div class="score-badge" :class="getScoreClass(analysis.Score)">
                {{ analysis.Score }}/10
              </div>
            </div>
            <p class="analysis-content">{{ analysis.Description }}</p>
          </div>
        </div>

        <h3 class="panel-title mt-8">Risks & Considerations</h3>
        <div class="risks-grid">
          <div v-for="(risk, index) in storyData?.analysis?.RisksAndConsiderations || []"
               :key="index"
               class="risk-item dark-panel"
               :class="risk.Severity?.toLowerCase()">
            <div class="risk-header">
              <div class="risk-title">
                <v-icon color="warning" class="mr-2">mdi-alert</v-icon>
                {{ risk.Classification }}
              </div>
              <div class="risk-severity">{{ risk.Severity }}</div>
            </div>
            <div class="risk-description">{{ risk.Description }}</div>
            <div class="risk-mitigation">
              <v-icon color="success" size="small" class="mr-2">mdi-shield</v-icon>
              {{ risk.PotentialSolution }}
            </div>
          </div>
        </div>

        <h3 class="panel-title mt-8">Recommendations</h3>
        <div class="recommendations-list">
          <div v-for="(rec, index) in storyData?.analysis?.Recommendations || []"
               :key="index"
               class="recommendation-item dark-panel">
            <v-icon color="info" size="small" class="mr-2">mdi-lightbulb</v-icon>
            {{ rec }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const isDev = computed(() => import.meta.env.DEV)
const route = useRoute()
const router = useRouter()
const storyData = ref(null)
const error = ref(null)
const loading = ref(false)
const submitting = ref(false)
const editingStory = ref(false)
const editedStory = ref('')
const editingCriteria = ref(false)
const editedCriteria = ref('')
const selectedDetails = ref([])

const getScoreClass = (score) => {
  if (score <= 3) return 'score-high'
  if (score <= 7) return 'score-medium'
  return 'score-low'
}

const fetchTechReview = async () => {
  loading.value = true
  error.value = null
  
  try {
    const storyId = route.params.id
    if (!storyId) {
      throw new Error('No story ID provided')
    }

    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/stories/${storyId}?version=SENIOR_DEV`
    )
    
    storyData.value = response.data
    console.log('Tech review data:', storyData.value)
  } catch (err) {
    console.error('Error fetching tech review:', err)
    error.value = 'Failed to load technical review: ' + (err.message || 'Unknown error')
  } finally {
    loading.value = false
  }
}

const acceptTechReview = async () => {
  try {
    // TODO: Implement API call
    console.log('Accepting tech review...')
  } catch (error) {
    console.error('Error accepting tech review:', error)
  }
}

const submitForEstimation = async () => {
  try {
    // TODO: Implement API call
    console.log('Submitting for estimation...')
  } catch (error) {
    console.error('Error submitting for estimation:', error)
  }
}

const editTask = (section, index, task) => {
  console.log('Edit task:', { section, index, task })
  // TODO: Implement edit functionality
}

const startEditingStory = () => {
  editedStory.value = storyData.value?.content?.story || ''
  editingStory.value = true
}

const saveStory = () => {
  if (storyData.value?.content) {
    storyData.value.content.story = editedStory.value
  }
  editingStory.value = false
}

const cancelEditStory = () => {
  editingStory.value = false
}

const startEditingCriteria = () => {
  editedCriteria.value = storyData.value?.content?.acceptance_criteria?.join('\n') || ''
  editingCriteria.value = true
}

const saveCriteria = () => {
  if (storyData.value?.content) {
    storyData.value.content.acceptance_criteria = editedCriteria.value
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
  }
  editingCriteria.value = false
}

const cancelEditCriteria = () => {
  editingCriteria.value = false
}

const selectDetail = (section, task) => {
  selectedDetails.value.push({ section, task })
}

const deselectDetail = (detail) => {
  const index = selectedDetails.value.findIndex(d => d.task === detail.task && d.section === detail.section)
  if (index !== -1) {
    selectedDetails.value.splice(index, 1)
  }
}

// Update computed property to handle the new structure
const availableDetails = computed(() => {
  const details = { Frontend: [], Backend: [], Database: [] }
  Object.entries(storyData.value?.analysis?.ImplementationDetails || {}).forEach(([section, tasks]) => {
    details[section] = tasks.filter(task => 
      !selectedDetails.value.some(d => d.task === task && d.section === section)
    )
  })
  return details
})

// Watch for route changes
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      fetchTechReview()
    }
  }
)

onMounted(() => {
  if (route.params.id) {
    fetchTechReview()
  }
})
</script>

<style scoped>
.tech-review {
  padding: 2rem;
  color: #fff;
}

.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  padding: 1rem;
  max-width: 2000px;
  margin: 0 auto;
  min-height: 100vh;
}

/* Headers */
h3 {
  color: #64B5F6;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

h4 {
  color: #fff;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

/* Content panels */
.dark-panel {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
  padding: 1rem;
}

/* Task items */
.task-item {
  padding: 0.75rem 1rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
}

.primary-content-wrapper {
  position: relative;
  height: calc(100vh - 2rem);
  overflow-y: auto;
  padding-bottom: 7rem;
}

.analysis-panel {
  height: calc(100vh - 2rem);
  overflow-y: auto;
}

.footer-buttons {
  position: fixed;
  bottom: 1rem;
  left: 25%;
  transform: translateX(-50%);
  width: fit-content;
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 10;
}

.tech-analysis-grid,
.risks-grid,
.recommendations-list {
  display: grid;
  gap: 0.75rem;
}

.tech-analysis-item,
.risk-item,
.recommendation-item {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 0;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.analysis-content {
  margin: 0;
  line-height: 1.5;
}

.score-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.9rem;
}

.score-high {
  background: rgba(76, 175, 80, 0.2);
  color: #81C784;
}

.score-medium {
  background: rgba(255, 152, 0, 0.2);
  color: #FFB74D;
}

.score-low {
  background: rgba(244, 67, 54, 0.2);
  color: #E57373;
}

.risk-item {
  border-left: 4px solid;
  padding: 1.25rem 1.5rem;
}

.risk-item.critical { 
  border-left-color: #FF1744;
}
.risk-item.high { 
  border-left-color: #EF5350;
}
.risk-item.medium { 
  border-left-color: #FFA726;
}
.risk-item.low { 
  border-left-color: #66BB6A;
}
.risk-item.informational { 
  border-left-color: #64B5F6;
}

.risk-severity {
  font-size: 0.9rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  background: rgba(30, 41, 59, 0.8);
}

.risk-item.critical .risk-severity { 
  color: #FF1744;
}
.risk-item.high .risk-severity { 
  color: #EF5350;
}
.risk-item.medium .risk-severity { 
  color: #FFA726;
}
.risk-item.low .risk-severity { 
  color: #66BB6A;
}
.risk-item.informational .risk-severity { 
  color: #64B5F6;
}

.risk-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.risk-title {
  display: flex;
  align-items: center;
  font-weight: 500;
}

.risk-description {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.risk-mitigation {
  color: #81C784;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem 1.5rem;
  line-height: 1.5;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1rem;
}

.error-state {
  text-align: center;
  padding: 2rem;
  margin: 2rem;
}

.empty-state {
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

.implementation-item {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chevron-icons {
  display: flex;
  gap: 2px;
}

.selectable {
  cursor: pointer;
  transition: background-color 0.2s;
}

.selectable:hover {
  background: rgba(40, 51, 69, 0.8);
}

.edit-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  opacity: 0;
}

.editable-content:hover .edit-btn {
  opacity: 1;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.25rem;
  margin-top: 0.75rem;
}

.edit-textarea {
  width: 100%;
  margin-bottom: 1rem;
}

@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .primary-content-wrapper,
  .analysis-panel {
    height: auto;
    min-height: calc(100vh - 2rem);
  }

  .footer-buttons {
    left: 50%;
    padding: 0 1rem;
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 600px) {
  .footer-buttons {
    flex-direction: column;
    gap: 0.75rem;
  }
}

/* Section headers (Frontend, Backend, Database) */
h4 {
  color: #64B5F6;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

/* Task items in the implementation details */
.task-item {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  line-height: 1.5;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* First section header shouldn't have top margin */
h4:first-of-type {
  margin-top: 0;
}

/* Icons in task items */
.task-item .v-icon {
  margin-right: 0.75rem;
}

/* Hover state */
.task-item.selectable:hover {
  background: rgba(40, 51, 69, 0.8);
  cursor: pointer;
}

.primary-content {
  flex: 1;
}

.page-title {
  color: #64B5F6;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  font-weight: normal;
}

.form-group {
  margin-bottom: 2rem;
}

.input-label {
  color: #64B5F6;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  display: block;
}

.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.criteria-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
}

.bullet {
  color: #64B5F6;
  font-size: 1rem;
}

.criteria-section,
.implementation-section {
  margin-bottom: 2rem;
}
</style> 