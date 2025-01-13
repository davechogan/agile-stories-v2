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
  const response = await api.post('/stories/analyze', {
    title: storyData.title,
    text: storyData.text,
    acceptance_criteria: storyData.acceptance_criteria.filter(c => c.trim() !== '')
  })
  return response.data
}

export const getStoryStatus = async (storyId) => {
  const response = await api.get(`/stories/${storyId}/status`)
  return response.data
} 