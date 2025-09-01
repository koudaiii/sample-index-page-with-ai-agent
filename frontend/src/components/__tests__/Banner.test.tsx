import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Banner } from '../Banner'

// Mock the API config
vi.mock('@/lib/config', () => ({
  API_ENDPOINTS: {
    BANNERS: '/api/banners'
  }
}))

// Mock fetch
global.fetch = vi.fn()

describe('Banner', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders loading state', () => {
    // Mock pending fetch
    vi.mocked(fetch).mockImplementation(() => new Promise(() => {}))
    
    render(<Banner />)
    
    const loadingElement = document.querySelector('.animate-pulse')
    expect(loadingElement).toBeInTheDocument()
  })

  it('renders error state when fetch fails', async () => {
    vi.mocked(fetch).mockRejectedValue(new Error('Failed to fetch banners'))
    
    render(<Banner />)
    
    // Wait for error state
    await vi.waitFor(() => {
      expect(screen.queryByText(/Error loading banners/)).toBeInTheDocument()
    }, { timeout: 1000 })
  })

  it('renders nothing when no banners', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => []
    } as Response)
    
    const { container } = render(<Banner />)
    
    // Wait for empty state
    await vi.waitFor(() => {
      expect(container.firstChild).toBeNull()
    }, { timeout: 1000 })
  })
})