import type { Story, AnalysisResult, MockAnalysisResult } from '@/types'
import api from './api'

export async function submitStoryForAgileReview(story: Story): Promise<MockAnalysisResult> {
  try {
    const response = await api.post<AnalysisResult>('/api/analyze', story)
    return transformAnalysis(response.data)
  } catch (error) {
    console.error('Error submitting story:', error)
    throw error
  }
}

const transformAnalysis = (rawAnalysis: AnalysisResult): MockAnalysisResult => {
  const investAnalysis = [
    { letter: 'I', title: 'Independent', content: 'Can this story be delivered independently?' },
    { letter: 'N', title: 'Negotiable', content: 'Is there room for negotiation?' },
    { letter: 'V', title: 'Valuable', content: 'Does this deliver value to stakeholders?' },
    { letter: 'E', title: 'Estimable', content: 'Can we estimate the size of the work?' },
    { letter: 'S', title: 'Small', content: 'Is this story small enough?' },
    { letter: 'T', title: 'Testable', content: 'Can we test this functionality?' }
  ]

  const suggestions = {}

  return {
    improved_story: {
      text: rawAnalysis.improved_story?.text || '',
      acceptance_criteria: rawAnalysis.improved_story?.acceptance_criteria || []
    },
    invest_analysis: investAnalysis,
    suggestions: Object.keys(suggestions).length ? suggestions : rawAnalysis.suggestions || {}
  }
} 