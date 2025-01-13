<template>
  <v-fade-transition>
    <div v-if="!analysis" class="loading">
      <v-progress-circular 
        indeterminate 
        color="primary"
        size="64"
      ></v-progress-circular>
      <div class="loading-text">
        <h3>Analyzing Your Story</h3>
        <p>Please wait while we process your request...</p>
      </div>
    </div>
    <div v-else class="test">
      <div class="two-column-layout">
        <!-- Left Column -->
        <div class="primary-content-wrapper">
          <div class="primary-content">
            <div class="story-section">
              <h3>Improved User Story</h3>
              <div class="editable-content">
                <v-textarea
                  :model-value="analysis.improved_story?.text || ''"
                  @update:model-value="updateStoryText"
                  variant="outlined"
                  auto-grow
                  rows="3"
                />
              </div>

              <h3>Acceptance Criteria</h3>
              <div class="editable-content">
                <div v-for="(criteria, index) in analysis.improved_story?.acceptance_criteria || []" 
                     :key="index"
                     class="criteria-item">
                  <v-textarea
                    :model-value="criteria"
                    @update:model-value="value => updateCriteria(index, value)"
                    variant="outlined"
                    auto-grow
                    rows="1"
                  />
                  <v-btn 
                    icon="mdi-delete" 
                    size="small"
                    color="error" 
                    variant="text"
                    @click="removeCriteria(index)"
                  />
                </div>
                <v-btn 
                  prepend-icon="mdi-plus"
                  variant="text"
                  @click="addCriteria"
                >
                  Add Criteria
                </v-btn>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column -->
        <div class="analysis-panel">
          <div class="analysis">
            <h3>INVEST Analysis</h3>
            <div class="invest-grid">
              <div v-for="(item, index) in analysis.invest_analysis || []" 
                   :key="index" 
                   class="invest-item">
                <div class="invest-header">
                  <span class="invest-letter">{{ item?.letter }}</span>
                  <span class="invest-title">{{ item?.title }}</span>
                </div>
                <div class="invest-content">{{ item?.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </v-fade-transition>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useStoryStore } from '@/stores/storyStore'
import { getStoryStatus } from '@/api/storyApi'

const storyStore = useStoryStore()
const analysis = ref(null)
const pollInterval = ref(null)

const checkStatus = async () => {
  try {
    const storyId = storyStore.currentStoryId
    if (!storyId) return

    const response = await getStoryStatus(storyId)
    console.log('Status check:', response)

    if (response.status === 'completed') {
      analysis.value = response.result
      clearInterval(pollInterval.value)
    }
  } catch (error) {
    console.error('Error checking status:', error)
  }
}

onMounted(() => {
  // Start polling every 2 seconds
  pollInterval.value = setInterval(checkStatus, 2000)
})

onUnmounted(() => {
  // Clean up interval when component is destroyed
  if (pollInterval.value) {
    clearInterval(pollInterval.value)
  }
})

const updateStoryText = (value) => {
  if (analysis.value?.improved_story) {
    analysis.value.improved_story.text = value
  }
}

const updateCriteria = (index, value) => {
  if (analysis.value?.improved_story?.acceptance_criteria) {
    analysis.value.improved_story.acceptance_criteria[index] = value
  }
}

const addCriteria = () => {
  if (analysis.value?.improved_story) {
    analysis.value.improved_story.acceptance_criteria.push('')
  }
}

const removeCriteria = (index) => {
  if (analysis.value?.improved_story) {
    analysis.value.improved_story.acceptance_criteria.splice(index, 1)
    if (analysis.value.improved_story.acceptance_criteria.length === 0) {
      analysis.value.improved_story.acceptance_criteria.push('')
    }
  }
}
</script>

<style scoped>
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

.criteria-item {
  display: flex;
  align-items: start;
  gap: 8px;
  margin-bottom: 8px;
}

.editable-content {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  padding: 1rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  gap: 2rem;
  background: rgba(0, 0, 0, 0.02);
}

.loading-text {
  text-align: center;
}

.loading-text h3 {
  margin-bottom: 0.5rem;
  color: var(--v-primary-base);
}

.v-fade-transition-enter-active,
.v-fade-transition-leave-active {
  transition: opacity 0.5s ease;
}

.v-fade-transition-enter-from,
.v-fade-transition-leave-to {
  opacity: 0;
}
</style> 