import { defineStore } from 'pinia'
import type { MockAnalysisResult } from '@/types'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentAnalysis: null as MockAnalysisResult | null,
    error: null as string | null
  }),
  
  actions: {
    setCurrentAnalysis(analysis: MockAnalysisResult) {
      try {
        // Basic validation that's always required
        if (!analysis.improved_story) {
          throw new Error('Invalid analysis format: missing improved story')
        }
        
        // Only validate INVEST analysis if present
        if (analysis.invest_analysis && (!Array.isArray(analysis.invest_analysis) || analysis.invest_analysis.length === 0)) {
          throw new Error('Invalid INVEST analysis format')
        }

        // Clear any previous errors
        this.error = null
        // Set the analysis
        this.currentAnalysis = analysis
        
      } catch (error) {
        console.error('Store error:', error)
        this.error = error instanceof Error ? error.message : 'Unknown error setting analysis'
        throw error
      }
    },
    
    clearCurrentAnalysis() {
      this.currentAnalysis = null
      this.error = null
    }
  },

  getters: {
    hasError: (state) => state.error !== null,
    getError: (state) => state.error,
    hasAnalysis: (state) => state.currentAnalysis !== null
  }
}) 