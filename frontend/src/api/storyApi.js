import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL
console.log('API URL:', API_BASE_URL)

export const submitStoryForAgileReview = async (storyData) => {
  try {
    const url = `${API_BASE_URL}/stories/analyze`
    console.log('Full API URL:', url)
    
    const response = await axios.post(url, storyData)
    return response.data
  } catch (error) {
    console.error('API Error:', error)
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