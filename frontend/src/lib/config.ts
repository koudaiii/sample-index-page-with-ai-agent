// API Configuration
const getApiBaseUrl = (): string => {
  // In production, API calls go through nginx proxy, so use relative paths
  if (import.meta.env.PROD) {
    return ''
  }
  
  // In development, use environment variable or default to localhost
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
}

export const API_BASE_URL = getApiBaseUrl()

export const API_ENDPOINTS = {
  BANNERS: `${API_BASE_URL}/api/banners`,
  CONTENT: `${API_BASE_URL}/api/content`,
  CONTENT_BY_CATEGORY: (category: string) => `${API_BASE_URL}/api/content/${category}`,
  HEALTH: `${API_BASE_URL}/health`,
} as const