<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2 class="page-title">Improved Title</h2>
          <div class="story-form">
            <div class="dark-panel mb-8">
              <textarea
                v-model="analysis?.analysis?.content?.title"
                class="edit-field"
                rows="1"
              ></textarea>
            </div>

            <h2 class="page-title">Improved Story</h2>
            <div class="dark-panel mb-8">
              <textarea
                v-model="analysis?.analysis?.content?.story"
                class="edit-field"
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <h2 class="page-title">Acceptance Criteria</h2>
              <div class="criteria-list">
                <div v-if="analysis?.analysis?.content?.acceptance_criteria"
                     v-for="(criterion, index) in analysis.analysis.content.acceptance_criteria" 
                     :key="index"
                     class="criteria-item">
                  <v-textarea
                    :value="criterion"
                    @input="updateCriterion(index, $event)"
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
                  :disabled="!analysis?.analysis?.content?.acceptance_criteria"
                >
                  Add Criteria
                </v-btn>
              </div>
            </div>
          </div>

          <!-- Single button for tech review -->
          <div class="action-buttons">
            <v-btn
              color="primary"
              size="large"
              @click="requestTechnicalReview"
              :loading="reviewing"
              :disabled="!canRequestReview || !analysis?.analysis?.content"
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
            <li v-for="(suggestion, index) in analysis?.analysis?.analysis?.Suggestions || []"
                :key="index"
                class="suggestion-item">
              {{ suggestion }}
            </li>
          </ul>
        </div>

        <h3 class="panel-title">INVEST Analysis</h3>
        <div class="invest-grid">
          <div v-for="(item, index) in analysis?.analysis?.analysis?.INVESTAnalysis || []"
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

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useStoryStore()
const analysis = ref(null)
const loading = ref(true)
const error = ref(null)
const reviewing = ref(false)
const canRequestReview = computed(() => true)

const addCriterion = () => {
  analysis.value.analysis.content.acceptance_criteria.push('')
}

const removeCriterion = (index) => {
  analysis.value.analysis.content.acceptance_criteria.splice(index, 1)
}

const updateCriterion = (index, value) => {
  if (analysis.value?.analysis?.content?.acceptance_criteria) {
    analysis.value.analysis.content.acceptance_criteria[index] = value
  }
}

const requestTechnicalReview = async () => {
  reviewing.value = true
  try {
    const storyId = route.params.id
    console.log('Requesting technical review for story:', storyId)
    
    const requestData = {
      story_id: storyId,
      tenant_id: "test-tenant-001",
      analysis: {
        content: {
          title: analysis.value.analysis.content.title,
          story: analysis.value.analysis.content.story,
          acceptance_criteria: analysis.value.analysis.content.acceptance_criteria
        }
      }
    }
    
    console.log('Sending technical review request:', requestData)
    
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/stories/tech-review`,
      requestData
    )
    
    console.log('Technical review response:', response)
    
    if (response.data && response.data.story_id) {
      await router.push(`/tech/${storyId}`)
    }
  } catch (err) {
    console.error('Error requesting technical review:', err)
    if (err.response) {
      console.log('Error response:', err.response.data)
    }
  } finally {
    reviewing.value = false
  }
}

onMounted(() => {
  // We'll need to add fetchAnalysis back later
})
</script>

<style scoped>
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

.debug {
  background: #333;
  padding: 1rem;
  margin: 1rem 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-size: 0.8rem;
}
</style> 