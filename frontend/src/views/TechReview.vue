<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2 class="page-title">Technical Review</h2>
          
          <!-- Story Overview -->
          <div class="story-form">
            <div class="dark-panel mb-8">
              <h3>{{ analysis?.ImprovedTitle }}</h3>
              <p class="mt-4">{{ analysis?.ImprovedStory }}</p>
            </div>

            <!-- Acceptance Criteria -->
            <h3 class="section-title">Acceptance Criteria</h3>
            <div class="dark-panel mb-8">
              <ul class="criteria-list">
                <li v-for="(criterion, index) in analysis?.ImprovedAcceptanceCriteria"
                    :key="index"
                    class="criterion-item">
                  {{ criterion }}
                </li>
              </ul>
            </div>

            <!-- Selected Implementation Details -->
            <div v-if="selectedTasks.length > 0" class="dark-panel mb-8">
              <h3 class="section-title">Selected Implementation Details</h3>
              <div class="selected-task-list">
                <div v-for="(task, index) in selectedTasks" 
                     :key="index"
                     class="selected-task-item">
                  <span class="task-category">{{ task.category }}:</span>
                  {{ task.description }}
                  <v-btn
                    icon="mdi-close"
                    size="small"
                    color="error"
                    variant="text"
                    @click="removeSelectedTask(index)"
                    class="remove-btn"
                  />
                </div>
              </div>
            </div>

            <!-- Implementation Details -->
            <h3 class="section-title">Implementation Details</h3>
            <div class="implementation-sections">
              <!-- Frontend -->
              <div class="detail-section">
                <h4 class="detail-title">
                  <v-icon color="primary" class="mr-2">mdi-code-tags</v-icon>
                  Frontend
                </h4>
                <div class="task-list">
                  <div v-for="(task, index) in unselectedTasks.Frontend"
                       :key="index"
                       class="task-item"
                       @click="toggleTask('Frontend', index, task)">
                    {{ task }}
                  </div>
                </div>
              </div>

              <!-- Backend -->
              <div class="detail-section">
                <h4 class="detail-title">
                  <v-icon color="success" class="mr-2">mdi-server</v-icon>
                  Backend
                </h4>
                <div class="task-list">
                  <div v-for="(task, index) in unselectedTasks.Backend"
                       :key="index"
                       class="task-item"
                       @click="toggleTask('Backend', index, task)">
                    {{ task }}
                  </div>
                </div>
              </div>

              <!-- Database -->
              <div class="detail-section">
                <h4 class="detail-title">
                  <v-icon color="warning" class="mr-2">mdi-database</v-icon>
                  Database
                </h4>
                <div class="task-list">
                  <div v-for="(task, index) in unselectedTasks.Database"
                       :key="index"
                       class="task-item"
                       @click="toggleTask('Database', index, task)">
                    {{ task }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="analysis-panel">
        <!-- Technical Analysis -->
        <h3 class="panel-title">Technical Analysis</h3>
        <div class="analysis-grid">
          <div v-for="(analysis, key) in analysis?.TechnicalAnalysis"
               :key="key"
               class="analysis-item">
            <div class="analysis-header">
              <span class="analysis-title">{{ key }}</span>
              <div class="score-badge" :class="getScoreClass(analysis.Score)">
                {{ analysis.Score }}/10
              </div>
            </div>
            <div class="analysis-content">{{ analysis.Description }}</div>
          </div>
        </div>

        <!-- Risks & Considerations -->
        <h3 class="panel-title mt-8">Risks & Considerations</h3>
        <div class="risks-grid">
          <div v-for="(risk, index) in analysis?.RisksAndConsiderations"
               :key="index"
               class="risk-item">
            <div class="risk-header">
              <v-icon color="warning" class="mr-2">mdi-alert</v-icon>
              {{ risk.Classification }}
              <span class="risk-severity">({{ risk.Severity }})</span>
            </div>
            <div class="risk-description">{{ risk.Description }}</div>
            <div class="risk-solution">
              <v-icon color="success" size="small" class="mr-2">mdi-shield</v-icon>
              {{ risk.PotentialSolution }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fixed Position Footer -->
    <div class="fixed-button-container">
      <v-btn
        color="primary"
        size="large"
        @click="submitForEstimation"
        :loading="loading"
      >
        Submit for Team Estimation
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'

const route = useRoute()
const store = useStoryStore()
const analysis = ref(null)
const loading = ref(true)
const selectedTasks = ref([])

const getScoreClass = (score) => {
  if (score >= 8) return 'score-high'
  if (score >= 5) return 'score-medium'
  return 'score-low'
}

const submitForEstimation = async () => {
  loading.value = true
  try {
    // TODO: Implement submission logic
    console.log('Submitting for estimation')
  } catch (error) {
    console.error('Error submitting for estimation:', error)
  } finally {
    loading.value = false
  }
}

// Computed property to get unselected tasks
const unselectedTasks = computed(() => {
  if (!analysis.value?.ImplementationDetails) return { Frontend: [], Backend: [], Database: [] }
  
  const selected = selectedTasks.value.reduce((acc, task) => {
    if (!acc[task.category]) acc[task.category] = new Set()
    acc[task.category].add(task.description)
    return acc
  }, {})

  return {
    Frontend: (analysis.value.ImplementationDetails.Frontend || [])
      .filter(task => !selected.Frontend?.has(task)),
    Backend: (analysis.value.ImplementationDetails.Backend || [])
      .filter(task => !selected.Backend?.has(task)),
    Database: (analysis.value.ImplementationDetails.Database || [])
      .filter(task => !selected.Database?.has(task))
  }
})

const toggleTask = (category, index, description) => {
  selectedTasks.value.push({ category, index, description })
}

const removeSelectedTask = (index) => {
  selectedTasks.value.splice(index, 1)
}

const pollForAnalysis = async () => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/stories/${route.params.id}?version=SENIOR_DEV`
    )
    
    if (response.ok) {
      const data = await response.json()
      analysis.value = data
      return true // Stop polling
    }
    return false // Continue polling
  } catch (error) {
    console.error('Error:', error)
    return false
  }
}

// Start polling when component mounts
onMounted(() => {
  const pollInterval = setInterval(async () => {
    const success = await pollForAnalysis()
    if (success) {
      clearInterval(pollInterval)
    }
  }, 2000) // Poll every 2 seconds
})
</script>

<style scoped>
/* Base Layout */
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: 100vh;
}

.primary-content-wrapper {
  width: 100%;
  min-width: 0;
}

.primary-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 4rem; /* Space for fixed button */
}

/* Section Styles */
.page-title {
  color: #64B5F6;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.section-title {
  color: #64B5F6;
  font-size: 1.25rem;
  margin: 2rem 0 1rem;
}

.dark-panel {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

/* Implementation Details */
.implementation-sections {
  display: grid;
  gap: 1.5rem;
}

.detail-section {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
}

.detail-title {
  display: flex;
  align-items: center;
  color: #64B5F6;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.task-list {
  display: grid;
  gap: 0.75rem;
}

.task-item {
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.task-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.selected-tasks {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
}

.selected-task-list {
  display: grid;
  gap: 0.75rem;
}

.selected-task-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.task-category {
  color: #64B5F6;
  font-weight: 500;
  margin-right: 0.5rem;
}

.remove-btn {
  margin-left: auto;
}

/* Analysis Panel */
.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  height: 100%;
}

.panel-title {
  color: #64B5F6;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.analysis-grid {
  display: grid;
  gap: 1rem;
}

.analysis-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1.25rem;
  border-radius: 8px;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.analysis-title {
  color: #64B5F6;
  font-weight: 500;
  text-transform: capitalize;
}

.score-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
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

/* Risks Section */
.risks-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.risk-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1.25rem;
  border-radius: 8px;
}

.risk-header {
  display: flex;
  align-items: center;
  color: #FFA726;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

.risk-severity {
  margin-left: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.8;
}

.risk-description {
  margin-bottom: 1rem;
  line-height: 1.5;
}

.risk-solution {
  color: #81C784;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Fixed Button Container */
.fixed-button-container {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: auto;
  display: flex;
  justify-content: center;
  background: linear-gradient(to top, rgba(18, 18, 18, 1) 50%, rgba(18, 18, 18, 0));
  padding: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }

  .analysis-panel {
    margin-top: 2rem;
  }

  .fixed-button-container {
    width: 100%;
    background: rgba(18, 18, 18, 0.9);
  }
}

/* Utility Classes */
.mb-8 {
  margin-bottom: 2rem;
}

.mt-8 {
  margin-top: 2rem;
}

.mr-2 {
  margin-right: 0.5rem;
}
</style> 