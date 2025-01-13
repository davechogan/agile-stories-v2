import { defineStore } from 'pinia'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentAnalysis: null
  }),

  actions: {
    setCurrentAnalysis(analysis) {
      console.log('Setting analysis:', analysis)
      this.currentAnalysis = analysis
    },

    clearCurrentAnalysis() {
      this.currentAnalysis = null
    }
  }
}) 