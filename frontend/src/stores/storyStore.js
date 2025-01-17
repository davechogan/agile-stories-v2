import { defineStore } from 'pinia'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentStoryId: null,
    storyDetails: null,
    status: 'SUBMITTED',
    feedback: null
  }),

  actions: {
    setCurrentStoryId(id) {
      this.currentStoryId = id
    },

    setStoryDetails(details) {
      this.storyDetails = details
    },

    updateFromSubscription(data) {
      this.status = data.status
      this.feedback = data.feedback
    }
  }
}) 