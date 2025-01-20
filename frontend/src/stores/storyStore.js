import { defineStore } from 'pinia'
import { storyApi } from '../api/storyApi'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentStory: null,
    storyEstimates: [], // Array of all estimates for current story
    currentEstimate: null,
    analysisToken: null,
    techReviewToken: null,
    estimateToken: null,
    
    // Tech Review state
    technicalComplexity: null,
    architectureImpact: null,
    securityConsiderations: null,
    technicalNotes: '',
    
    // Estimate state
    storyPoints: null,
    confidenceLevel: null,
    estimationNotes: '',
    teamConsensus: null,
    
    loading: false,
    error: null,
    estimateHistory: {
      versions: [],
      currentVersion: null,
      isLatestAccepted: false
    },
    revisionHistory: {
      versions: [],
      currentVersion: null
    }
  }),

  getters: {
    hasEstimate: (state) => state.storyEstimates.length > 0,
    latestEstimate: (state) => state.storyEstimates[state.storyEstimates.length - 1],
    estimateVersions: (state) => state.storyEstimates,
    hasAcceptedEstimate: (state) => state.estimateHistory.isLatestAccepted,
    currentEstimateVersion: (state) => state.estimateHistory.currentVersion,
    
    // For displaying history
    formattedEstimateHistory: (state) => {
      return state.estimateHistory.versions.map(v => ({
        ...v,
        formattedDate: new Date(v.timestamp).toLocaleString()
      }))
    }
  },

  actions: {
    setCurrentStory(story) {
      this.currentStory = story
    },

    clearCurrentStory() {
      this.currentStory = null
    },

    async completeTechReview(payload) {
      this.loading = true
      try {
        const response = await storyApi.completeTechReview(
          this.currentStory.id,
          this.techReviewToken,
          {
            ...payload,
            version: this.storyEstimates.length + 1 // Increment version
          }
        )
        this.techReviewToken = null
        
        // If final, update story status
        if (payload.status === 'FINAL') {
          this.currentStory.status = 'COMPLETED'
        }
        
        await this.fetchStory(this.currentStory.id)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async completeTeamEstimate(payload) {
      this.loading = true
      try {
        const response = await storyApi.completeTeamEstimate(
          this.currentStory.id,
          this.estimateToken,
          {
            ...payload,
            version: this.storyEstimates.length + 1,
            timestamp: new Date().toISOString()
          }
        )
        
        // Add new estimate to history
        this.storyEstimates.push({
          ...payload,
          version: this.storyEstimates.length + 1,
          timestamp: new Date().toISOString()
        })
        
        this.estimateToken = null
        
        // If accepted, update story status
        if (payload.status === 'FINAL') {
          this.currentStory.status = 'COMPLETED'
        }
        
        await this.fetchStory(this.currentStory.id)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchStoryEstimates(storyId) {
      this.loading = true
      try {
        const estimates = await storyApi.getStoryEstimates(storyId)
        this.storyEstimates = estimates
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    // Called when loading a story
    async fetchStory(storyId) {
      this.loading = true
      try {
        const [story, estimates] = await Promise.all([
          storyApi.getStory(storyId),
          storyApi.getStoryEstimates(storyId)
        ])
        this.currentStory = story
        this.storyEstimates = estimates
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async loadEstimateHistory(storyId) {
      this.loading = true
      try {
        const history = await storyApi.getStoryEstimates(storyId)
        this.estimateHistory = {
          versions: history,
          currentVersion: history.length,
          isLatestAccepted: history[history.length - 1]?.status === 'FINAL'
        }
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async addNewEstimateVersion(payload) {
      const newVersion = {
        ...payload,
        version: this.estimateHistory.versions.length + 1,
        timestamp: new Date().toISOString()
      }
      
      this.estimateHistory.versions.push(newVersion)
      this.estimateHistory.currentVersion = newVersion.version
      this.estimateHistory.isLatestAccepted = payload.status === 'FINAL'
    }
  }
}) 