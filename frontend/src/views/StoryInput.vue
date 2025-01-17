<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <div class="story-section">
            <h3>Title</h3>
            <div class="editable-content">
              <v-text-field
                v-model="story.title"
                label="Enter a descriptive title"
                variant="outlined"
              />
            </div>

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
import { apolloClient } from '@/plugins/apollo'
import gql from 'graphql-tag'

const GET_STORY_STATUS = gql`
  query GetStoryStatus($storyId: ID!) {
    getStoryStatus(storyId: $storyId) {
      story_id
      version
    }
  }
`

const router = useRouter()
const storyStore = useStoryStore()
const loading = ref(false)

// Story data structure
const story = ref({
  title: '',
  text: '',
  description: '',
  acceptance_criteria: ['']
})

// Form validation
const isValid = computed(() => {
  return story.value.title.trim() !== '' &&
         story.value.text.trim() !== '' &&
         story.value.acceptance_criteria.some(c => c.trim() !== '')
})

// Submit handler
const submitStory = async () => {
  try {
    loading.value = true
    console.log('Starting story submission...')
    
    const storyData = {
      tenant_id: 'test-tenant-001',
      content: {
        title: story.value.title,
        description: story.value.description,
        story: story.value.text,
        acceptance_criteria: story.value.acceptance_criteria.filter(c => c.trim() !== '')
      }
    }

    console.log('Submitting to API Gateway:', storyData)
    const response = await submitStoryForAgileReview(storyData)
    console.log('API Response:', response)
    
    // Make sure storyStore is initialized
    if (storyStore && typeof storyStore.setCurrentStoryId === 'function') {
      storyStore.setCurrentStoryId(response.story_id)
      router.push('/agile')
    } else {
      console.error('Story store not properly initialized')
    }
  } catch (error) {
    console.error('Error submitting story:', error)
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

// After story submission success:
const handleSubmitSuccess = async (response) => {
  const storyId = response.story_id
  storyStore.setCurrentStoryId(storyId)
  
  // Start polling for AGILE_COACH version
  let pollAttempts = 0
  const MAX_POLL_ATTEMPTS = 10
  
  const pollInterval = setInterval(async () => {
    try {
      pollAttempts++
      console.log(`Polling attempt ${pollAttempts}/${MAX_POLL_ATTEMPTS} for story: ${storyId}`)
      
      const { data } = await apolloClient.query({
        query: GET_STORY_STATUS,
        variables: { storyId },
        fetchPolicy: 'network-only'
      })
      
      console.log('Poll response:', data?.getStoryStatus)
      
      if (data?.getStoryStatus?.version === 'AGILE_COACH') {
        console.log('✅ Found AGILE_COACH version - navigating to results')
        clearInterval(pollInterval)
        router.push('/agile')
      } else if (pollAttempts >= MAX_POLL_ATTEMPTS) {
        console.log('🛑 Max polling attempts reached')
        clearInterval(pollInterval)
      }
    } catch (error) {
      console.error('❌ Polling error:', error)
      if (pollAttempts >= MAX_POLL_ATTEMPTS) {
        clearInterval(pollInterval)
      }
    }
  }, 2000)
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
  width: 100%;
  min-width: 0;
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

.analysis-panel {
  width: 100%;
  min-width: 0;
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 1.5rem;
}
</style> 