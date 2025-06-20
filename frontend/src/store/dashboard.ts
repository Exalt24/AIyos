import { create } from 'zustand'
import { DashboardStats, AIUsageStats } from '@/types'

interface DashboardState {
  stats: DashboardStats | null
  aiStats: AIUsageStats | null
  isLoading: boolean
  error: string | null
  
  // Actions
  setStats: (stats: DashboardStats) => void
  setAiStats: (stats: AIUsageStats) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  clearError: () => void
}

export const useDashboardStore = create<DashboardState>((set) => ({
  stats: null,
  aiStats: null,
  isLoading: false,
  error: null,
  
  setStats: (stats) => set({ stats }),
  setAiStats: (aiStats) => set({ aiStats }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}))