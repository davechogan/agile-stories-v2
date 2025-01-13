import axios from 'axios'

// Allow for multiple development URLs
const DEV_URLS = [
  'http://localhost:3000',
  'http://127.0.0.1:3000'
]

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || DEV_URLS[0]

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor to handle CORS
api.interceptors.request.use(config => {
  // Add CORS headers for development
  if (DEV_URLS.some(url => config.baseURL.startsWith(url))) {
    config.headers['Access-Control-Allow-Origin'] = '*'
    config.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    config.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'
  }
  return config
})

export const submitStoryForAgileReview = async (storyData) => {
  try {
    console.log('Submitting story to API:', storyData)  // Log outgoing request
    
    const payload = {
      story: {
        title: storyData.title,
        description: storyData.text,
        acceptanceCriteria: storyData.acceptance_criteria.filter(c => c.trim() !== '')
      }
    }

    console.log('Formatted payload:', payload)  // Log formatted payload
    const response = await api.post('/stories/analyze', payload)
    console.log('API response:', response.data)  // Log API response
    return response.data  // Should return { storyId: "some-uuid" }
  } catch (error) {
    console.error('Error submitting story:', error)
    throw error
  }
}

export const getStoryStatus = async (storyId) => {
  try {
    const response = await api.get(`/stories/${storyId}/status`)
    return response.data  // Should return { status: "pending" | "completed", result?: {...} }
  } catch (error) {
    console.error('Error checking story status:', error)
    throw error
  }
} 