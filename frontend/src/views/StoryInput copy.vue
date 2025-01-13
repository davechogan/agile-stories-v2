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

const writingTips = [
  {
    letter: 'U',
    title: 'User',
    content: 'Clearly identify who the user is (e.g., customer, admin, guest)'
  },
  {
    letter: 'G',
    title: 'Goal',
    content: 'State what the user wants to accomplish'
  },
  {
    letter: 'B',
    title: 'Benefit',
    content: 'Explain why this is valuable to the user'
  },
  {
    letter: 'A',
    title: 'Acceptance',
    content: 'Write clear, testable acceptance criteria'
  }
]

const isValid = computed(() => {
  return story.value.text.trim() !== '' && 
         story.value.acceptance_criteria.some(c => c.trim() !== '')
})

const addCriteria = () => {
  story.value.acceptance_criteria.push('')
}

const removeCriteria = (index) => {
  story.value.acceptance_criteria.splice(index, 1)
  if (story.value.acceptance_criteria.length === 0) {
    story.value.acceptance_criteria.push('')
  }
}

const submitStory = async () => {
  if (!isValid.value) return
  
  loading.value = true
  try {
    const result = await submitStoryForAgileReview(story.value)
    storyStore.setCurrentAnalysis(result)
    router.push('/agile')
  } catch (error) {
    console.error('Error submitting story:', error)
  } finally {
    loading.value = false
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

.primary-content-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.primary-content {
  flex-grow: 1;
  margin-bottom: 2rem;
}

.sticky-footer {
  position: sticky;
  bottom: 0;
  background: rgb(18, 18, 18);
  padding: 1rem 0;
  width: 100%;
  z-index: 1;
}

.footer-content {
  display: flex;
  justify-content: flex-end;
  padding: 0 1rem;
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

h3 {
  color: #64B5F6;
  margin-bottom: 1rem;
}

.invest-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.invest-item {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 1.5rem;
  border-left: 4px solid #FFA726;
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
</style> 