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
        <!-- Team Estimate Panel - Shows on mobile -->
        <div v-if="hasEstimates" class="team-estimate-panel mobile-only">
          <h3>Team Estimate</h3>
          <div class="estimate-details">
            <div class="estimate-value">{{ averageEstimate }} {{ useStoryPoints ? 'points' : 'days' }}</div>
            <div class="estimate-confidence" :class="averageConfidence">
              {{ averageConfidence }} confidence
            </div>
          </div>
        </div>

        <h2 class="page-title">Technical Review Modifications</h2>
        
        <EditableSection
          v-model="storyData.content.title"
          title="Story Title"
          type="single-line"
          placeholder="Enter story title..."
        />
        
        <EditableSection
          v-model="storyData.content.story"
          title="User Story"
          type="text"
          placeholder="Describe the user story..."
        />
        
        <EditableSection
          v-model="storyData.content.acceptance_criteria"
          title="Acceptance Criteria"
          type="list"
          placeholder="Enter each criterion on a new line..."
        />

        <!-- Selected Implementation Details -->
        <h4 class="mt-4">Selected Implementation Details</h4>
        <div class="editable-content">
          <div v-if="selectedDetails.length === 0" class="no-details">
            No implementation details added yet. Select from the sections below.
          </div>
          <div v-else class="selected-details">
            <div v-for="(detail, index) in selectedDetails" 
                 :key="index"
                 class="selected-detail">
              <div class="detail-content">
                <v-icon size="small" :color="getDetailColor(detail.type)" class="mr-2">
                  {{ getDetailIcon(detail.type) }}
                </v-icon>
                {{ detail.text }}
              </div>
              <v-btn 
                size="x-small" 
                color="error" 
                variant="text"
                icon="mdi-close"
                @click="removeDetail(index)"
              ></v-btn>
            </div>
          </div>
        </div>

        <!-- Implementation Details Section -->
        <h2 class="mt-6">Implementation Details</h2>
        <div class="tech-section">
          <h4>Frontend</h4>
          <div class="task-list">
            <div v-for="(task, index) in availableDetails.Frontend" 
                 :key="'fe-'+index"
                 class="task-item"
                 @click="toggleDetail('Frontend', task)">
              <v-icon size="small" color="primary" class="mr-2">mdi-code-tags</v-icon>
              {{ task }}
            </div>
          </div>

          <h4>Backend</h4>
          <div class="task-list">
            <div v-for="(task, index) in availableDetails.Backend" 
                 :key="'be-'+index"
                 class="task-item"
                 @click="toggleDetail('Backend', task)">
              <v-icon size="small" color="success" class="mr-2">mdi-server</v-icon>
              {{ task }}
            </div>
          </div>

          <h4>Database</h4>
          <div class="task-list">
            <div v-for="(task, index) in availableDetails.Database" 
                 :key="'db-'+index"
                 class="task-item"
                 @click="toggleDetail('Database', task)">
              <v-icon size="small" color="warning" class="mr-2">mdi-database</v-icon>
              {{ task }}
            </div>
          </div>
        </div>

        <!-- Sticky footer -->
        <div class="sticky-footer">
          <div class="footer-content">
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
                @click="getTeamEstimate"
                :loading="estimating"
              >
                GET TEAM ESTIMATE
              </v-btn>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="analysis-panel">
        <!-- Team Estimate Panel - Shows on desktop -->
        <div v-if="hasEstimates" class="team-estimate-panel desktop-only">
          <h3>Team Estimate</h3>
          <div class="estimate-details">
            <div class="estimate-value">{{ averageEstimate }} {{ useStoryPoints ? 'points' : 'days' }}</div>
            <div class="estimate-confidence" :class="averageConfidence">
              {{ averageConfidence }} confidence
            </div>
          </div>
        </div>

        <h2 class="page-title">Technical Analysis</h2>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import EditableSection from '@/components/EditableSection.vue'
import { mockTechReviewResult } from '@/mocks/mockTechReviewData'
import { useSettingsStore } from '@/stores/settingsStore'
import { useEstimateStore } from '@/stores/estimateStore'

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
const estimating = ref(false)
const showTransition = ref(false)
const isExiting = ref(false)
const videoPlayer = ref(null)
const settingsStore = useSettingsStore()
const estimateStore = useEstimateStore()

interface ImplementationDetail {
  type: 'Frontend' | 'Backend' | 'Database'
  text: string
}

// Store original details and selected details
const originalDetails = ref({
  Frontend: [...mockTechReviewResult.implementation_details.Frontend],
  Backend: [...mockTechReviewResult.implementation_details.Backend],
  Database: [...mockTechReviewResult.implementation_details.Database]
})

const availableDetails = ref({
  Frontend: [...mockTechReviewResult.implementation_details.Frontend],
  Backend: [...mockTechReviewResult.implementation_details.Backend],
  Database: [...mockTechReviewResult.implementation_details.Database]
})

const selectedDetails = ref<ImplementationDetail[]>([])

const toggleDetail = (type: 'Frontend' | 'Backend' | 'Database', text: string) => {
  const typeList = availableDetails.value[type]
  const index = typeList.indexOf(text)
  if (index >= 0) {
    typeList.splice(index, 1)
    selectedDetails.value.push({ type, text })
  }
}

const removeDetail = (index: number) => {
  const detail = selectedDetails.value[index]
  availableDetails.value[detail.type].push(detail.text)
  availableDetails.value[detail.type].sort((a, b) => {
    return originalDetails.value[detail.type].indexOf(a) - 
           originalDetails.value[detail.type].indexOf(b)
  })
  selectedDetails.value.splice(index, 1)
}

const getDetailIcon = (type: string): string => {
  switch (type) {
    case 'Frontend': return 'mdi-code-tags'
    case 'Backend': return 'mdi-server'
    case 'Database': return 'mdi-database'
    default: return 'mdi-code-tags'
  }
}

const getDetailColor = (type: string): string => {
  switch (type) {
    case 'Frontend': return 'primary'
    case 'Backend': return 'success'
    case 'Database': return 'warning'
    default: return 'primary'
  }
}

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
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Tech review accepted')
  } catch (error) {
    console.error('Error accepting tech review:', error)
  } finally {
    loading.value = false
  }
}

const getTeamEstimate = async () => {
  estimating.value = true
  
  try {
    const storyId = route.params.id
    
    // Single POST to trigger estimation process
    const estimatePayload = {
      story_id: storyId,
      tenant_id: "test-tenant-001",
      content: {
        title: storyData.value.content.title,
        story: storyData.value.content.story,
        acceptance_criteria: storyData.value.content.acceptance_criteria,
        implementation_details: selectedDetails.value.map(detail => ({
          type: detail.type,
          text: detail.text
        }))
      },
      roles: settingsStore.selectedRoles
    }
    
    console.log('Sending estimate request:', estimatePayload)
    
    // Show transition immediately
    showTransition.value = true
    isExiting.value = false
    
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/stories/estimate`,
      estimatePayload
    )
    
    console.log('Estimate response:', response.data)
    
    // Start fading out after response
    isExiting.value = true
    
    // Wait for fade out animation before hiding video and navigating
    setTimeout(async () => {
      showTransition.value = false
      await router.push(`/estimates/${storyId}`)
    }, 1000)
    
  } catch (err) {
    console.error('Error in estimate process:', err)
    showTransition.value = false
    isExiting.value = false
    error.value = 'Failed to process estimate request'
  } finally {
    estimating.value = false
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
  console.log('Tech Review mounted, store values:', {
    average: estimateStore.averageEstimate,
    confidence: estimateStore.averageConfidence,
    hasEstimates: estimateStore.averageEstimate !== null && 
                  estimateStore.averageConfidence !== null
  })
})

const hasEstimates = computed(() => 
  estimateStore.averageEstimate !== null && 
  estimateStore.averageConfidence !== null
)

const averageEstimate = computed(() => estimateStore.averageEstimate ?? '-')
const averageConfidence = computed(() => estimateStore.averageConfidence ?? '-')

const useStoryPoints = computed(() => settingsStore.estimateType === 'story_points')

// Add debug info to verify store value
console.log('Tech Review - Store estimate type:', settingsStore.estimateType)
</script>

<style scoped>
/* Container (outermost) - stays black */
.tech-review {
  background: rgb(18, 18, 18);
}

/* Panel/Column (middle) - dark gray to match left side */
.analysis-panel {
  background: rgb(18, 18, 18);
  padding: 1rem;
  border-radius: 8px;
}

/* Cards (innermost) - return to original blue */
.tech-analysis-item,
.risk-item,
.recommendation-item,
.team-estimate-panel {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.tech-review {
  padding: 1rem;
}

.page-title {
  color: #64B5F6;
  font-size: 1.5rem;
  font-weight: normal;
  margin-bottom: 2rem;
}

.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

.team-estimate-panel,
.analysis-panel,
.tech-analysis-item,
.risk-item,
.recommendation-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.primary-content-wrapper {
  position: relative;
  height: calc(100vh - 2rem);
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: 7rem;
  isolation: isolate; /* Create stacking context */
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
  max-width: 100%;
}

.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(18, 18, 18, 0.9);
  padding: 1rem;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.footer-content {
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.footer-buttons {
  display: flex;
  gap: 1rem;
  width: 100%;
  justify-content: center;
}

.section-title {
  font-size: 1.25rem;
}

.section-header {
  color: #fff;
  font-size: 1rem;
  margin-bottom: 0.75rem;
  font-weight: normal;
}

.task-item,
.criteria-item,
pre {
  font-size: 0.875rem;
  line-height: 1.5;
}

.dark-panel {
  background: rgba(33, 150, 243, 0.1) !important;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
}

section {
  margin-bottom: 1rem;
}

.task-list {
  gap: 0.5rem;
}

.task-item {
  padding: 0.5rem 0.75rem;
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
  padding: 1rem;
  margin-bottom: 1rem;
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

@media (max-width: 960px) {
  .two-column-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1rem;
  }

  .team-estimate-panel,
  .analysis-panel,
  .tech-analysis-item,
  .risk-item,
  .recommendation-item {
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
    overflow-wrap: break-word;
    word-wrap: break-word;
    hyphens: auto;
  }

  /* Ensure content doesn't overflow */
  .primary-content-wrapper,
  .analysis-panel {
    width: 100%;
    padding: 1rem;
    overflow-x: hidden;
  }

  /* Adjust text sizes for mobile */
  h2, h3 {
    font-size: 1.25rem;
  }

  .estimate-value {
    font-size: 1.1rem;
  }

  .estimate-confidence {
    font-size: 0.85rem;
  }

  /* Add some breathing room between sections */
  .section {
    margin-bottom: 1.5rem;
  }

  .sticky-footer {
    padding: 0.75rem;
  }

  .footer-buttons {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0 1rem;
  }

  .v-btn {
    width: 100%;
    margin: 0 !important;
  }

  /* Add padding to content to prevent overlap with fixed buttons */
  .primary-content-wrapper {
    padding-bottom: calc(7rem + env(safe-area-inset-bottom));
  }
}

/* Prevent horizontal scrolling on all screen sizes */
body {
  overflow-x: hidden;
}

/* Section headers (Frontend, Backend, Database) */
h4 {
  color: #fff;
  font-size: 1.1rem;
  margin: 1.5rem 0 1rem;
  font-weight: normal;
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
  display: grid;
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

/* Restore original styles */
.tech-section {
  margin-top: 1rem;
}

.tech-section h4 {
  color: #64B5F6;
  margin: 1.5rem 0 1rem;
  font-size: 1.1rem;
}

.task-list {
  display: grid;
  gap: 0.75rem;
}

.task-item {
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  background: rgba(33, 150, 243, 0.1);
}

.task-item:hover {
  background: rgba(33, 150, 243, 0.2);
  transform: translateY(-1px);
}

.selected-details {
  display: grid;
  gap: 0.5rem;
}

.selected-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(33, 150, 243, 0.1);
  border-radius: 6px;
  transition: all 0.2s ease;
}

.detail-content {
  display: flex;
  align-items: center;
}

.no-details {
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

.editable-content {
  position: relative;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  transition: all 0.3s ease;
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

.team-estimate-panel {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(33, 150, 243, 0.3);  /* Subtle blue border */
  box-shadow: 0 0 15px rgba(33, 150, 243, 0.1);  /* Soft blue glow */
}

.estimate-details {
  margin-top: 0.5rem;
}

.estimate-value {
  font-size: 1.2rem;
  color: #64B5F6;
  font-weight: 500;
}

.estimate-confidence {
  font-size: 0.9rem;
  margin-top: 0.2rem;
}

.estimate-confidence.high {
  color: #4CAF50;
}

.estimate-confidence.medium {
  color: #FFC107;
}

.estimate-confidence.low {
  color: #F44336;
}

@media (min-width: 961px) {
  .mobile-only {
    display: none;
  }
}

/* iOS safe area support */
@supports (padding: max(0px)) {
  .sticky-footer {
    padding-bottom: max(1rem, env(safe-area-inset-bottom));
  }
}

.right-column {
  flex: 1;
  padding: 1rem;
}

/* If needed, override any Vuetify default backgrounds */
:deep(.dark-panel) {
  background: rgba(33, 150, 243, 0.1) !important;
}
</style> 