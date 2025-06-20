import { api } from './api'
import { User, AuthTokens, LoginForm, RegisterForm } from '@/types'
import { API_ENDPOINTS } from '@/lib/constants'

export const authService = {
  login: async (credentials: LoginForm): Promise<{ user: User; tokens: AuthTokens }> => {
    const response = await api.post(API_ENDPOINTS.AUTH.LOGIN, credentials)
    return response.data
  },

  register: async (userData: RegisterForm): Promise<{ user: User; tokens: AuthTokens }> => {
    const response = await api.post(API_ENDPOINTS.AUTH.REGISTER, userData)
    return response.data
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get(API_ENDPOINTS.AUTH.PROFILE)
    return response.data
  },

  updateProfile: async (userData: Partial<User>): Promise<User> => {
    const response = await api.put(API_ENDPOINTS.AUTH.PROFILE, userData)
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<AuthTokens> => {
    const response = await api.post(API_ENDPOINTS.AUTH.REFRESH, {
      refresh: refreshToken,
    })
    return response.data
  },
}