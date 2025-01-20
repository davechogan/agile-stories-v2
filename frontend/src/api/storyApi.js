import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    // No need for extra CORS headers here since API Gateway handles it
  }
  // Remove withCredentials since we're using '*' in API Gateway
})

// Export individual functions
export const submitStoryForAgileReview = async (storyData) => {
  try {
    console.log('API URL:', API_URL)
    const fullUrl = `${API_URL}/stories/analyze`
    console.log('Full API URL:', fullUrl)
    
    const response = await api.post('/stories/analyze', storyData)
    return response.data
  } catch (error) {
    console.log('API Error:', error)
    throw error
  }
}

// Export other methods
export const storyApi = {
  api,
  submitStoryForAgileReview,

  async getStoryStatus(storyId) {
    try {
      const response = await api.get(`/stories/${storyId}/status`)
      return response.data  // Should return { status: "pending" | "completed", result?: {...} }
    } catch (error) {
      console.error('Error checking story status:', error)
      throw error
    }
  },

  async completeAnalysis(storyId, token, result) {
    return await this.api.post(`/stories/${storyId}/analysis/complete`, {
      token,
      result
    })
  },

  async completeTechnicalReview(storyId, token, result) {
    return await this.api.post(`/stories/${storyId}/tech-review/complete`, {
      token,
      result
    })
  },

  async completeTeamEstimate(storyId, token, payload) {
    return await this.api.post(`/stories/${storyId}/estimate/complete`, {
      token,
      ...payload,
      timestamp: new Date().toISOString()
    })
  },

  async getStoryEstimates(storyId) {
    const response = await this.api.get(`/stories/${storyId}/estimates`)
    return response.data
  },

  async getStory(storyId) {
    const response = await this.api.get(`/stories/${storyId}`)
    return response.data
  },

  async updateStory(storyId, data) {
    return await this.api.put(`/stories/${storyId}`, data)
  }
} 