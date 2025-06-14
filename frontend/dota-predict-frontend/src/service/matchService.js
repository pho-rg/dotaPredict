import axios from 'axios'

const MATCH_URL = import.meta.env.VITE_API_URL + 'match/'

export const getAllLiveMatches = async () => {
  try {
    // TODO remove once kafka implemented
    await retrieveLiveMatches()

    const response = await axios.get(MATCH_URL + 'getAllLive/')
    return response.data
  } catch (error) {
    console.error('Failed to fetch matches', error)
    throw error
  }
}

export const getOneMatch = async (matchId) => {
  try {
    const response = await axios.get(MATCH_URL + 'getOne/' + matchId)
    return response.data
  } catch (error) {
    console.error('Failed to retrieve live matches', error)
    throw error
  }
}

// trigger POST API route to update table with live matches
// TODO remove once kafka implemented
export const retrieveLiveMatches = async () => {
  try {
    const response = await axios.post(MATCH_URL + 'saveLiveMatches/')
    return response.data
  } catch (error) {
    console.error('Failed to retrieve live matches', error)
    throw error
  }
}
