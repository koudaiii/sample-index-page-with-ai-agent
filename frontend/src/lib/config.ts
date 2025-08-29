// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const API_ENDPOINTS = {
  BANNERS: `${API_BASE_URL}/api/banners`,
  CONTENT: `${API_BASE_URL}/api/content`,
  CONTENT_BY_CATEGORY: (category: string) => `${API_BASE_URL}/api/content/${category}`,
  HEALTH: `${API_BASE_URL}/health`,
} as const