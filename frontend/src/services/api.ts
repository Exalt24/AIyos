import axios, { AxiosResponse } from 'axios'
import { useAuthStore } from '@/store/auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().tokens?.access
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = useAuthStore.getState().tokens?.refresh
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          })

          const newTokens = response.data
          useAuthStore.getState().setTokens(newTokens)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${newTokens.access}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        useAuthStore.getState().logout()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

// Generic API functions
export const apiGet = <T>(url: string): Promise<AxiosResponse<T>> => api.get(url)
export const apiPost = <T>(url: string, data?: any): Promise<AxiosResponse<T>> => api.post(url, data)
export const apiPut = <T>(url: string, data?: any): Promise<AxiosResponse<T>> => api.put(url, data)
export const apiDelete = <T>(url: string): Promise<AxiosResponse<T>> => api.delete(url)

export default api