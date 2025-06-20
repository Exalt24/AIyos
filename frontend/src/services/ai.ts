import { api } from './api'
import { 
  AIModel, 
  AIRequest, 
  AIUsageStats, 
  EmailToTaskForm, 
  SocialContentForm 
} from '@/types'
import { API_ENDPOINTS } from '@/lib/constants'

export const aiService = {
  getModels: async (): Promise<AIModel[]> => {
    const response = await api.get(API_ENDPOINTS.AI.MODELS)
    return response.data
  },

  getUsageStats: async (): Promise<AIUsageStats> => {
    const response = await api.get(API_ENDPOINTS.AI.USAGE_STATS)
    return response.data
  },

  getRequests: async (): Promise<AIRequest[]> => {
    const response = await api.get('/ai/requests/')
    return response.data.results
  },

  emailToTask: async (data: EmailToTaskForm) => {
    const response = await api.post(API_ENDPOINTS.AI.EMAIL_TO_TASK, data)
    return response.data
  },

  generateSocialContent: async (data: SocialContentForm) => {
    const response = await api.post(API_ENDPOINTS.AI.GENERATE_CONTENT, data)
    return response.data
  },

  getQuotaStatus: async () => {
    const response = await api.get('/ai/quota-status/')
    return response.data
  },

  getHealthCheck: async () => {
    const response = await api.get('/ai/health-check/')
    return response.data
  },
}