import axios from 'axios'

const PREDICTION_URL = import.meta.env.VITE_API_URL + 'prediction/'

export const getAvailableModels = async () => {
  try {
    const response = await axios.get(PREDICTION_URL + 'getAvailableModels/')
    return response.data
  } catch (error) {
    console.error('Failed to fetch models', error)
    throw error
  }
}

export const predictMatch = async body => {
  try {
    const response = await axios.post(PREDICTION_URL + 'predictMatch/', body)
    return response.data
  } catch (error) {
    console.error('Failed to retrieve prediction', error)
    throw error
  }
}
