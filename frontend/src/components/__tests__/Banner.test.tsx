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

  it('calls API with query parameter when provided', async () => {
    const mockBanners = [
      {
        id: '1',
        title: 'Test Banner',
        subtitle: 'Test Subtitle',
        imageUrl: '/test.jpg',
        tag: 'Test',
        color: 'blue'
      }
    ]

    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockBanners
    } as Response)

    render(<Banner query="test query" />)

    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/banners?query=test+query')
    }, { timeout: 1000 })
  })

  it('calls API with use_ai parameter when provided', async () => {
    const mockBanners = [
      {
        id: 'rec_1',
        title: 'AI Recommended Banner',
        subtitle: 'AI Generated',
        imageUrl: '/ai.jpg',
        tag: 'AI推薦',
        color: 'orange'
      }
    ]

    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockBanners
    } as Response)

    render(<Banner useAi={true} />)

    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/banners?use_ai=true')
    }, { timeout: 1000 })
  })

  it('calls API with both query and use_ai parameters', async () => {
    const mockBanners = [
      {
        id: 'rec_2',
        title: 'Custom AI Banner',
        subtitle: 'Custom Query Result',
        imageUrl: '/custom.jpg',
        tag: 'AI推薦',
        color: 'green'
      }
    ]

    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockBanners
    } as Response)

    render(<Banner query="custom search" useAi={true} />)

    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/banners?query=custom+search&use_ai=true')
    }, { timeout: 1000 })
  })

  it('calls API without parameters when none provided', async () => {
    const mockBanners = [
      {
        id: '3',
        title: 'Regular Banner',
        subtitle: 'Regular Content',
        imageUrl: '/regular.jpg',
        tag: 'Regular',
        color: 'blue'
      }
    ]

    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockBanners
    } as Response)

    render(<Banner />)

    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/banners')
    }, { timeout: 1000 })
  })
})