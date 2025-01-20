import { defineStore } from 'pinia'

export const useAnalysisStore = defineStore('analysis', {
  state: () => ({
    analysisToken: null,
    analysisStatus: null,
    analysisResults: null
  }),

  actions: {
    setAnalysisToken(token) {
      this.analysisToken = token
    },

    setAnalysisStatus(status) {
      this.analysisStatus = status
    },

    setAnalysisResults(results) {
      this.analysisResults = results
    },

    clearAnalysis() {
      this.analysisToken = null
      this.analysisStatus = null
      this.analysisResults = null
    }
  },

  getters: {
    hasToken: (state) => Boolean(state.analysisToken),
    isAnalysisComplete: (state) => state.analysisStatus === 'COMPLETE'
  }
}) 