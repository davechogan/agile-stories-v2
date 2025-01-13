import { defineStore } from 'pinia'

interface FormatFeedback {
  type: 'positive' | 'warning'
  message: string
}

interface StoryState {
  loading: boolean
  improvedStory: string
  acceptanceCriteria: string[]
  formatScore: number
  clarityScore: number
  formatFeedback: FormatFeedback[]
  clarityFeedback: FormatFeedback[]
}

export const useStoryStore = defineStore('story', {
  state: (): StoryState => {
    // Try to load state from localStorage
    const savedState = localStorage.getItem('storyState')
    if (savedState) {
      const state = JSON.parse(savedState)
      // Always reset loading state on load
      state.loading = false
      return state
    }
    
    return {
      loading: false,
      improvedStory: '',
      acceptanceCriteria: [],
      formatScore: 0,
      clarityScore: 0,
      formatFeedback: [],
      clarityFeedback: []
    }
  },

  actions: {
    async submitForImprovement(story: string, acceptanceCriteria: string, context: string) {
      this.loading = true
      try {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // Mock successful response
        const mockResponse = {
          improved_story: "As a user, I want to receive notifications about system updates, so that I can stay informed about new features and changes.",
          acceptance_criteria: [
            "User sees notification badge when new system update is available",
            "Clicking notification opens update details modal",
            "User can mark notifications as read",
            "Notifications show timestamp and priority level",
            "User can filter notifications by type and status"
          ],
          format_score: 8.5,
          clarity_score: 9.0,
          format_feedback: [
            { type: 'positive', message: "Clear user role identification" },
            { type: 'positive', message: "Well-defined action and benefit" },
            { type: 'warning', message: "Consider specifying user type more precisely" }
          ],
          clarity_feedback: [
            { type: 'positive', message: "Concise and focused objective" },
            { type: 'positive', message: "Clear value proposition" },
            { type: 'warning', message: "Could provide more context about system update types" }
          ]
        }

        // Update store with mock response
        this.improvedStory = mockResponse.improved_story
        this.acceptanceCriteria = mockResponse.acceptance_criteria
        this.formatScore = mockResponse.format_score
        this.clarityScore = mockResponse.clarity_score
        this.formatFeedback = mockResponse.format_feedback
        this.clarityFeedback = mockResponse.clarity_feedback

        // Save to localStorage
        localStorage.setItem('storyState', JSON.stringify(this.$state))

        return true
      } catch (error) {
        console.error('Error improving story:', error)
        return false
      } finally {
        this.loading = false
      }
    },

    clearState() {
      this.$reset()
      localStorage.removeItem('storyState')
    }
  }
}) 