<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <!-- Add Story and AC sections -->
          <div class="story-section">
            <h3>Technical Review Modifications</h3>
            
            <!-- Story Section -->
            <h4 class="mt-4">User Story</h4>
            <div class="editable-content">
              <template v-if="!editingStory">
                <pre>{{ mockTechReviewResult.improved_story.text }}</pre>
                <v-btn 
                  size="small" 
                  color="primary" 
                  class="edit-btn"
                  icon="mdi-pencil"
                  @click="startEditingStory"
                ></v-btn>
              </template>
              <template v-else>
                <v-textarea
                  v-model="editedStory"
                  auto-grow
                  variant="outlined"
                  class="edit-textarea"
                ></v-textarea>
                <div class="edit-actions">
                  <v-btn 
                    size="small" 
                    color="success" 
                    @click="saveStory"
                    class="mr-2"
                  >Save</v-btn>
                  <v-btn 
                    size="small" 
                    color="error" 
                    @click="cancelEditStory"
                  >Cancel</v-btn>
                </div>
              </template>
            </div>
            
            <!-- AC Section -->
            <h4 class="mt-4">Acceptance Criteria</h4>
            <div class="editable-content">
              <template v-if="!editingAC">
                <ul>
                  <li v-for="(criterion, index) in mockTechReviewResult.improved_story.acceptance_criteria" 
                      :key="index">
                    {{ criterion }}
                  </li>
                </ul>
                <v-btn 
                  size="small" 
                  color="primary" 
                  class="edit-btn"
                  icon="mdi-pencil"
                  @click="startEditingAC"
                ></v-btn>
              </template>
              <template v-else>
                <v-textarea
                  v-model="editedAC"
                  auto-grow
                  variant="outlined"
                  placeholder="One acceptance criterion per line"
                  class="edit-textarea"
                ></v-textarea>
                <div class="edit-actions">
                  <v-btn 
                    size="small" 
                    color="success" 
                    @click="saveAC"
                    class="mr-2"
                  >Save</v-btn>
                  <v-btn 
                    size="small" 
                    color="error" 
                    @click="cancelEditAC"
                  >Cancel</v-btn>
                </div>
              </template>
            </div>

            <!-- After AC section and before Implementation Details -->
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
            <h3 class="mt-6">Implementation Details</h3>
            <div class="tech-section">
              <h4>Frontend</h4>
              <div class="task-list">
                <div v-for="(task, index) in availableDetails.frontend" 
                     :key="'fe-'+index"
                     class="task-item"
                     @click="toggleDetail('frontend', task)">
                  <v-icon size="small" color="primary" class="mr-2">mdi-code-tags</v-icon>
                  {{ task }}
                </div>
              </div>

              <h4>Backend</h4>
              <div class="task-list">
                <div v-for="(task, index) in availableDetails.backend" 
                     :key="'be-'+index"
                     class="task-item"
                     @click="toggleDetail('backend', task)">
                  <v-icon size="small" color="success" class="mr-2">mdi-server</v-icon>
                  {{ task }}
                </div>
              </div>

              <h4>Database</h4>
              <div class="task-list">
                <div v-for="(task, index) in availableDetails.database" 
                     :key="'db-'+index"
                     class="task-item"
                     @click="toggleDetail('database', task)">
                  <v-icon size="small" color="warning" class="mr-2">mdi-database</v-icon>
                  {{ task }}
                </div>
              </div>
            </div>

            <h3 class="mt-6">Tech Lead Estimate</h3>
            <div class="effort-grid">
              <div v-for="(effort, key) in mockTechReviewResult.estimated_effort" 
                   :key="key"
                   class="effort-item"
                   :class="{ 'effort-total': key === 'total' }">
                <div class="effort-label">{{ key }}</div>
                <div class="effort-value">{{ effort }}</div>
              </div>
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
                @click="submitForEstimation"
              >
                SEND FOR ESTIMATION
              </v-btn>
            </div>
            <div class="footer-hint" v-if="editingStory || editingAC">
              Save your changes to enable actions
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Analysis -->
      <div class="analysis-panel">
        <div class="technical-analysis">
          <h3>Technical Analysis</h3>
          <div class="analysis-grid">
            <div v-for="(analysis, key) in mockTechReviewResult.technical_analysis" 
                 :key="key"
                 class="analysis-item">
              <div class="analysis-header">
                <span class="analysis-title">{{ key }}</span>
                <div class="score-badge" :class="getScoreClass(analysis.score)">
                  {{ analysis.score }}/10
                </div>
              </div>
              <div class="analysis-content">{{ analysis.explanation }}</div>
            </div>
          </div>
        </div>

        <div class="risks mt-6">
          <h3>Risks & Considerations</h3>
          <div class="risks-grid">
            <div v-for="(risk, index) in mockTechReviewResult.risks_and_considerations" 
                 :key="index"
                 class="risk-item">
              <div class="risk-header">
                <v-icon color="warning" class="mr-2">mdi-alert</v-icon>
                {{ risk.category }}
              </div>
              <div class="risk-description">{{ risk.description }}</div>
              <div class="risk-mitigation">
                <v-icon color="success" size="small" class="mr-2">mdi-shield</v-icon>
                {{ risk.mitigation }}
              </div>
            </div>
          </div>
        </div>

        <div class="recommendations mt-6">
          <h3>Recommendations</h3>
          <div class="recommendations-list">
            <div v-for="(rec, index) in mockTechReviewResult.recommendations" 
                 :key="index"
                 class="recommendation-item">
              <v-icon color="info" size="small" class="mr-2">mdi-lightbulb</v-icon>
              {{ rec }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { mockTechReviewResult } from '@/mocks/mockTechReviewData'

const router = useRouter()
const loading = ref(false)

// Story editing
const editingStory = ref(false)
const editedStory = ref('')

const startEditingStory = () => {
  editedStory.value = mockTechReviewResult.improved_story.text
  editingStory.value = true
}

const saveStory = () => {
  mockTechReviewResult.improved_story.text = editedStory.value
  editingStory.value = false
}

const cancelEditStory = () => {
  editingStory.value = false
}

// Acceptance Criteria editing
const editingAC = ref(false)
const editedAC = ref('')

const startEditingAC = () => {
  editedAC.value = mockTechReviewResult.improved_story.acceptance_criteria.join('\n')
  editingAC.value = true
}

const saveAC = () => {
  mockTechReviewResult.improved_story.acceptance_criteria = editedAC.value
    .split('\n')
    .filter(line => line.trim())
  editingAC.value = false
}

const cancelEditAC = () => {
  editingAC.value = false
}

// Keep existing getScoreClass function
const getScoreClass = (score: number): string => {
  if (score >= 8) return 'score-high'
  if (score >= 5) return 'score-medium'
  return 'score-low'
}

interface ImplementationDetail {
  type: 'frontend' | 'backend' | 'database'
  text: string
}

// Store original details and selected details
const originalDetails = ref({
  frontend: [...mockTechReviewResult.implementation_details.frontend],
  backend: [...mockTechReviewResult.implementation_details.backend],
  database: [...mockTechReviewResult.implementation_details.database]
})

const availableDetails = ref({
  frontend: [...mockTechReviewResult.implementation_details.frontend],
  backend: [...mockTechReviewResult.implementation_details.backend],
  database: [...mockTechReviewResult.implementation_details.database]
})

const selectedDetails = ref<ImplementationDetail[]>([])

const toggleDetail = (type: 'frontend' | 'backend' | 'database', text: string) => {
  // Remove from available list and add to selected
  const typeList = availableDetails.value[type]
  const index = typeList.indexOf(text)
  if (index >= 0) {
    typeList.splice(index, 1)
    selectedDetails.value.push({ type, text })
  }
}

const removeDetail = (index: number) => {
  const detail = selectedDetails.value[index]
  // Add back to original section
  availableDetails.value[detail.type].push(detail.text)
  // Sort to maintain original order
  availableDetails.value[detail.type].sort((a, b) => {
    return originalDetails.value[detail.type].indexOf(a) - 
           originalDetails.value[detail.type].indexOf(b)
  })
  // Remove from selected
  selectedDetails.value.splice(index, 1)
}

const getDetailIcon = (type: string): string => {
  switch (type) {
    case 'frontend': return 'mdi-code-tags'
    case 'backend': return 'mdi-server'
    case 'database': return 'mdi-database'
    default: return 'mdi-code-tags'
  }
}

const getDetailColor = (type: string): string => {
  switch (type) {
    case 'frontend': return 'primary'
    case 'backend': return 'success'
    case 'database': return 'warning'
    default: return 'primary'
  }
}

const acceptTechReview = async () => {
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Just log for now since we don't have the accept endpoint
    console.log('Tech review accepted')
    // Don't navigate
  } catch (error) {
    console.error('Error accepting tech review:', error)
  } finally {
    loading.value = false
  }
}

const submitForEstimation = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    router.push('/estimate')
  } catch (error) {
    console.error('Error submitting for estimation:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style>
/* Base layout styles (similar to TestFormatView) */
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

/* Implementation Details Styles */
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

/* Effort Grid */
.effort-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid #4CAF50;
}

.effort-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.effort-total {
  background: rgba(33, 150, 243, 0.2);
  font-weight: bold;
}

.effort-label {
  color: #64B5F6;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.effort-value {
  font-size: 1.2rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.87);
}

/* Analysis Panel Styles */
.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.analysis-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
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
  font-size: 1.1rem;
  text-transform: capitalize;
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

/* Risks Styles */
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
  color: #FFA726;
  font-weight: 500;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
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

/* Recommendations Styles */
.recommendations-list {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
}

.recommendation-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
}

/* Sticky Footer */
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
  
  .sticky-footer {
    position: fixed;
    width: 100%;
    left: 0;
    right: 0;
    margin-top: 0;
  }
  
  .analysis-panel {
    margin-top: 2rem;
  }
}

/* Add these new styles */
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

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.edit-textarea {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.footer-hint {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
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

.selected-detail:hover {
  background: rgba(33, 150, 243, 0.15);
}

.detail-content {
  display: flex;
  align-items: center;
}

.no-details {
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

.task-item {
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.task-item:hover {
  background: rgba(33, 150, 243, 0.2);
}

.task-item.selected {
  background: rgba(33, 150, 243, 0.3);
}

/* Checkbox styling */
:deep(.v-checkbox) {
  margin: 0;
  padding: 0;
}

:deep(.v-checkbox .v-selection-control) {
  margin: 0;
  padding: 0;
}

.footer-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* Add animation classes */
.task-list-enter-active,
.task-list-leave-active {
  transition: all 0.3s ease;
}

.task-list-enter-from,
.task-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 