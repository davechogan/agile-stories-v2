<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2 class="page-title" style="color: yellow">TEST - Improved Story</h2>
          <div class="story-form">
            <div class="dark-panel mb-8">
              {{ analysis?.content?.improved_story?.text }}
            </div>

            <h2 class="page-title">Acceptance Criteria</h2>
            <div class="dark-panel">
              <ul class="criteria-list">
                <li v-for="(criterion, index) in analysis?.content?.improved_story?.acceptance_criteria"
                    :key="index"
                    class="criterion-item">
                  {{ criterion }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Analysis Panel -->
      <div class="analysis-panel">
        <h3 class="panel-title">INVEST Analysis</h3>
        <div class="invest-grid">
          <div v-for="(item, key) in analysis?.content?.invest_analysis"
               :key="key"
               class="invest-item">
            <div class="invest-header">
              <span class="invest-letter">{{ key }}</span>
              <span class="invest-title">{{ item.title }}</span>
            </div>
            <div class="invest-content">{{ item.content }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { mockAnalysisResult } from '@/mocks/mockAnalysisData'
import { useStoryStore } from '@/stores/storyStore'
import { useRouter } from 'vue-router'

const store = useStoryStore()
const router = useRouter()
const isLoading = ref(false)
const analysis = ref(mockAnalysisResult)

onMounted(() => {
  // Use mock data instead of redirecting
  store.analysis = mockAnalysisResult
})

// Comment out or remove the redirect logic
/*
watch(analysis, (newValue) => {
  if (!newValue) {
    router.push('/')
  }
})
*/

// Story editing
const editingStory = ref(false)
const editedStory = ref('')

const startEditingStory = () => {
  editedStory.value = mockAnalysisResult.improved_story.text
  editingStory.value = true
}

const saveStory = () => {
  mockAnalysisResult.improved_story.text = editedStory.value
  editingStory.value = false
}

const cancelEditStory = () => {
  editingStory.value = false
}

// Acceptance Criteria editing
const editingAC = ref(false)
const editedAC = ref('')

const startEditingAC = () => {
  editedAC.value = mockAnalysisResult.improved_story.acceptance_criteria.join('\n')
  editingAC.value = true
}

const saveAC = () => {
  mockAnalysisResult.improved_story.acceptance_criteria = editedAC.value
    .split('\n')
    .filter(line => line.trim()) // Remove empty lines
  editingAC.value = false
}

const cancelEditAC = () => {
  editingAC.value = false
}

// Parse INVEST analysis into structured data
const investAnalysis = [
  {
    letter: 'I',
    title: 'Independent',
    content: 'The user story is independent, as it does not seem to depend on any other user story for its implementation.'
  },
  {
    letter: 'N',
    title: 'Negotiable',
    content: 'The story is not very negotiable as it is not clear on what exactly the notification bell should do, or what exactly broadcasting a message entails.'
  },
  {
    letter: 'V',
    title: 'Valuable',
    content: 'The value to the user is not clearly stated. Why should the user care about this new notification bell?'
  },
  {
    letter: 'E',
    title: 'Estimable',
    content: 'The story is too vague to be reliably estimated. We don\'t know what "broadcasting a message" involves.'
  },
  {
    letter: 'S',
    title: 'Small',
    content: 'The story is not small, as it seems to involve several different features or functionalities.'
  },
  {
    letter: 'T',
    title: 'Testable',
    content: 'The acceptance criteria are too vague to be testable. What does it mean for everyone to "get it" and "read it"?'
  }
]

// Add this function to detect negative feedback
const isNegative = (content: string): boolean => {
  const negativeTerms = ['not', 'too vague', 'unclear', 'missing'];
  return negativeTerms.some(term => content.toLowerCase().includes(term));
}

const sendForTechReview = async () => {
  isLoading.value = true
  try {
    await store.completeAnalysis({
      improvedTitle: analysis.value.ImprovedTitle,
      improvedStory: analysis.value.ImprovedStory,
      improvedAcceptanceCriteria: analysis.value.ImprovedAcceptanceCriteria,
      investAnalysis: analysis.value.INVESTAnalysis,
      suggestions: analysis.value.Suggestions
    })
    router.push('/tech-review')
  } catch (error) {
    console.error('Error completing analysis:', error)
  }
  isLoading.value = false
}
</script>

<style scoped>
.test .two-column-layout {
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

.invest-content {
  color: rgba(255, 255, 255, 0.87);
  line-height: 1.6;
}

.criteria-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.criterion-item {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
  position: relative;
  font-size: 1rem;
  line-height: 1.6;
}

.criterion-item::before {
  content: "•";
  color: #64B5F6;
  position: absolute;
  left: 0;
}

@media (max-width: 1024px) {
  .test .two-column-layout {
    grid-template-columns: 1fr !important;
  }
}
</style> 