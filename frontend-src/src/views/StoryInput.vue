<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <div class="story-section">
            <h3>User Story</h3>
            <div class="editable-content">
              <v-textarea
                v-model="story.text"
                label="As a [user type], I want [goal], so that [benefit]"
                variant="outlined"
                auto-grow
                rows="3"
              />
            </div>

            <h3>Acceptance Criteria</h3>
            <div class="editable-content">
              <div v-for="(criteria, index) in story.acceptance_criteria" 
                   :key="index"
                   class="criteria-item">
                <v-textarea
                  v-model="story.acceptance_criteria[index]"
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

        <div class="sticky-footer">
          <div class="footer-content">
            <v-btn 
              color="primary" 
              :loading="loading"
              :disabled="!isValid"
              @click="submitStory"
              size="large"
            >
              Analyze Story
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Right Column: Help Panel -->
      <div class="analysis-panel">
        <div class="analysis">
          <h3>Writing Tips</h3>
          <div class="invest-grid">
            <div v-for="(tip, index) in writingTips" 
                 :key="index" 
                 class="invest-item">
              <div class="invest-header">
                <span class="invest-letter">{{ tip.letter }}</span>
                <span class="invest-title">{{ tip.title }}</span>
              </div>
              <div class="invest-content">{{ tip.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'
import { submitStoryForAgileReview } from '@/api/storyApi'

const router = useRouter()
const storyStore = useStoryStore()
const loading = ref(false)

const story = ref({
  text: '',
  acceptance_criteria: [''],
  context: '',
  version: 1
})

// ... rest of the script setup code remains the same ...
</script>

<style scoped>
/* ... styles remain the same ... */
</style> 