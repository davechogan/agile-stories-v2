<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <div class="story-section">
            <h3>Improved User Story</h3>
            <div class="editable-content">
              <v-textarea
                v-model="analysis.improved_story.text"
                variant="outlined"
                auto-grow
                rows="3"
              />
            </div>

            <h3>Acceptance Criteria</h3>
            <div class="editable-content">
              <div v-for="(criteria, index) in analysis.improved_story.acceptance_criteria" 
                   :key="index"
                   class="criteria-item">
                <v-textarea
                  v-model="analysis.improved_story.acceptance_criteria[index]"
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
            <div v-for="(item, index) in analysis.invest_analysis" 
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
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStoryStore } from '@/stores/storyStore'

const storyStore = useStoryStore()
const analysis = computed(() => storyStore.currentAnalysis)

const addCriteria = () => {
  if (analysis.value) {
    analysis.value.improved_story.acceptance_criteria.push('')
  }
}

const removeCriteria = (index: number) => {
  if (analysis.value) {
    analysis.value.improved_story.acceptance_criteria.splice(index, 1)
    if (analysis.value.improved_story.acceptance_criteria.length === 0) {
      analysis.value.improved_story.acceptance_criteria.push('')
    }
  }
}
</script>

<style>
/* Copy all styles exactly from TestFormatView.vue */
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

/* ... rest of styles from TestFormatView.vue ... */

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
</style> 