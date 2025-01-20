<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2 class="page-title">Story Input</h2>
          <div class="story-form">
            <div class="form-group">
              <label class="input-label">Title</label>
              <v-text-field
                v-model="story.title"
                label="Enter a descriptive title"
                variant="outlined"
              />
            </div>

            <div class="form-group">
              <label class="input-label">User Story</label>
              <v-textarea
                v-model="story.text"
                label="As a [user type], I want [goal], so that [benefit]"
                variant="outlined"
                auto-grow
                rows="3"
              />
            </div>

            <div class="form-group">
              <label class="input-label">Acceptance Criteria</label>
              <div class="criteria-list">
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
              Submit Story
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Right Column: Help Panel -->
      <div class="analysis-panel">
        <h3 class="panel-title">Writing Tips</h3>
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'
import { submitStoryForAgileReview } from '../api/storyApi'
import { useAnalysisStore } from '@/stores/analysisStore'
import { v4 as uuidv4 } from 'uuid'

const router = useRouter()
const storyStore = useStoryStore()
const analysisStore = useAnalysisStore()
const loading = ref(false)
const error = ref(null)

// Generate token on component mount
onMounted(() => {
  if (!analysisStore.analysisToken) {
    analysisStore.setAnalysisToken(uuidv4())
  }
})

// Story data structure
const story = ref({
  title: '',
  text: '',
  acceptance_criteria: ['']
})

// Modified validation to only require title
const isValid = computed(() => {
  return story.value.title.trim() !== '' && story.value.text.trim() !== ''
})

const submitStory = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Verify token exists
    if (!analysisStore.analysisToken) {
      throw new Error('Missing analysis token')
    }

    const storyData = {
      tenant_id: "test-tenant-001",
      token: analysisStore.analysisToken,
      content: {
        title: story.value.title,
        description: "",
        story: story.value.text,
        acceptance_criteria: story.value.acceptance_criteria
          .filter(c => c.trim() !== '')
      }
    }

    console.log('Submitting story with token:', JSON.stringify(storyData, null, 2))
    
    const response = await submitStoryForAgileReview(storyData)
    console.log('Story submitted successfully:', response)
    
    if (response && response.story_id && response.token) {
      const storyData = {
        story_id: response.story_id,
        token: response.token
      }
      console.log('Setting store with:', storyData)
      
      await storyStore.setCurrentStory(storyData)
      console.log('Store updated. Current story:', storyStore.currentStory)
      
      await router.push('/agile')
    } else {
      throw new Error('Missing story_id or token in response')
    }
  } catch (err) {
    console.error('Error submitting story:', err)
    error.value = err.message || 'Failed to submit story. Please try again.'
  } finally {
    loading.value = false
  }
}

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

const addCriteria = () => {
  story.value.acceptance_criteria.push('')
}

const removeCriteria = (index) => {
  story.value.acceptance_criteria.splice(index, 1)
  if (story.value.acceptance_criteria.length === 0) {
    story.value.acceptance_criteria.push('')
  }
}

const guidelines = {
  story: {
    title: 'Story Writing Guidelines',
    items: [
      {
        icon: 'mdi-format-quote-open',
        header: 'User Story Format',
        content: [
          { prefix: 'As a', text: '[type of user]' },
          { prefix: 'I want to', text: '[perform some action]' },
          { prefix: 'So that', text: '[achieve some benefit]' }
        ]
      },
      {
        icon: 'mdi-lightbulb',
        header: 'Acceptance Criteria Tips',
        content: [
          { text: 'Use clear, specific language' },
          { text: 'One criterion per line' },
          { text: 'Include all success conditions' },
          { text: 'Consider edge cases' },
          { text: 'Make them testable' }
        ]
      }
    ]
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
}

.primary-content-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100%;  /* Take full height */
}

.primary-content {
  flex: 1;          /* Take remaining space */
  padding-bottom: 5rem;
}

.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgb(18, 18, 18);
  z-index: 100;
}

.footer-content {
  max-width: 1800px;  /* Match main content width */
  margin: 0 auto;
  padding: 1rem 2rem;  /* Match main content padding */
  display: flex;
  justify-content: flex-end;
}

.criteria-item {
  display: flex;
  align-items: start;
  gap: 8px;
  margin-bottom: 8px;
}

.editable-content {
  margin-bottom: 1.5rem;  /* More space between sections */
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

.section-title,
.panel-title {
  color: #64B5F6;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.story-section {
  margin-bottom: 1rem;
}

.story-section > * {
  margin-bottom: 1.5rem;  /* Reduced from 3rem */
}

.invest-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.analysis-panel {
  width: 100%;
  min-width: 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
}

.writing-tips-wrapper {
  background: #121212 !important;
  height: 100%;
  overflow-y: auto;
}

.writing-tips {
  padding: 20px;
}

.tip-card {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.guideline-card {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.page-title {
  color: #64B5F6;
  font-size: 1.5rem;
  margin-bottom: 1rem;  /* Reduced from 1.5rem */
  font-weight: 500;
}

.input-label {
  color: #fff;
  font-size: 1rem;
  margin-bottom: 0.25rem;  /* Reduced from 0.5rem */
  font-weight: 400;
}

.form-group {
  margin-bottom: 1rem;
}

.story-form {
  background: rgba(30, 30, 30, 0.5);
  border-radius: 8px;
  padding: 1.5rem;
}

/* Adjust acceptance criteria textarea size */
.criteria-item :deep(.v-field__input) {
  min-height: 48px !important;  /* Reduced height */
  padding: 8px 12px !important;
}
</style> 