import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const submitStoryForAgileReview = async (storyData) => {
  const response = await api.post('/stories/analyze', storyData)
  return response.data
}

export const getStoryStatus = async (storyId) => {
  const response = await api.get(`/stories/${storyId}/status`)
  return response.data
} 