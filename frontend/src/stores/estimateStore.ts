import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEstimateStore = defineStore('estimate', () => {
  // Use refs instead of state object
  const averageEstimate = ref<number | null>(null)
  const averageConfidence = ref<string | null>(null)

  // Load initial values from localStorage if they exist
  const savedData = localStorage.getItem('estimateData')
  if (savedData) {
    const parsed = JSON.parse(savedData)
    averageEstimate.value = parsed.averageEstimate
    averageConfidence.value = parsed.averageConfidence
  }

  function setEstimates(average: number, confidence: string) {
    console.log('Setting new estimates:', { average, confidence })
    averageEstimate.value = average
    averageConfidence.value = confidence
    
    // Save to localStorage
    localStorage.setItem('estimateData', JSON.stringify({
      averageEstimate: average,
      averageConfidence: confidence
    }))
  }

  function clearEstimates() {
    averageEstimate.value = null
    averageConfidence.value = null
    localStorage.removeItem('estimateData')
  }

  return {
    averageEstimate,
    averageConfidence,
    setEstimates,
    clearEstimates
  }
}) 