import { defineStore } from 'pinia'
import { mockAnalysisResult } from '@/mocks/mockAnalysisData'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentAnalysis: mockAnalysisResult
  }),

  actions: {
    setCurrentAnalysis(analysis) {
      this.currentAnalysis = analysis
    },

    clearCurrentAnalysis() {
      this.currentAnalysis = mockAnalysisResult
    }
  }
}) 