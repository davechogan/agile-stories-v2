import { defineStore } from 'pinia'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentStoryId: null,
    storyDetails: null
  }),

  actions: {
    setCurrentStoryId(id) {
      this.currentStoryId = id
    },

    setStoryDetails(details) {
      this.storyDetails = details
    }
  }
}) 