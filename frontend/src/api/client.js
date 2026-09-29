import axios from 'axios'

const localHosts = ['localhost', '127.0.0.1']
const configuredBaseURL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000/api`
const parsedBaseURL = new URL(configuredBaseURL, window.location.origin)
if (localHosts.includes(window.location.hostname) && localHosts.includes(parsedBaseURL.hostname)) {
  parsedBaseURL.hostname = window.location.hostname
}
const baseURL = parsedBaseURL.toString().replace(/\/$/, '')
const api = axios.create({ baseURL, withCredentials: true, headers: { 'Content-Type': 'application/json' } })
let csrfToken = null

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift())
  return null
}

export async function initCsrf() {
  const response = await api.get('/auth/csrf/')
  csrfToken = response.data.csrfToken
}

api.interceptors.request.use((config) => {
  const method = (config.method || 'get').toLowerCase()
  if (!['get','head','options'].includes(method)) {
    const token = getCookie('csrftoken') || csrfToken
    if (token) config.headers['X-CSRFToken'] = token
  }
  return config
})

export function apiError(error) {
  return error?.response?.data?.detail || error?.response?.data || error?.message || 'Something went wrong.'
}
export default api
