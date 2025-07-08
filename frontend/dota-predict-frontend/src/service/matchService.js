import axios from 'axios'

const MATCH_URL = import.meta.env.VITE_API_URL + 'match/'

export const getAllLiveMatches = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(MATCH_URL + 'getAllLive/',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    return response.data
  } catch (error) {
    console.error('Failed to fetch matches', error)
    throw error
  }
}

export const getAllMatchesHistory = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(MATCH_URL + 'getAllMatchesHistory/',
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    return response.data
  } catch (error) {
    console.error('Failed to fetch matches history', error)
    throw error
  }
}

export const getOneMatch = async matchId => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(MATCH_URL + 'getOne/' + matchId,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    return response.data
  } catch (error) {
    console.error('Failed to retrieve live matches', error)
    throw error
  }
}
