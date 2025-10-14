import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { ContentList } from '../ContentList'

// Mock the API config
vi.mock('@/lib/config', () => ({
  API_ENDPOINTS: {
    CONTENT: '/api/content'
  }
}))

// Mock fetch
globalThis.fetch = vi.fn()

const mockContentData = [
  {
    id: 'item-1',
    title: 'ワイヤレスヘッドホン',
    price: 15800,
    originalPrice: 19800,
    rating: 4.2,
    imageUrl: '/images/headphones.jpg',
    category: 'electronics',
    isNew: true,
    isSale: true,
    isRecommended: false
  }
]

describe('ContentList', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders title correctly', () => {
    render(<ContentList title="テスト商品" items={[]} />)
    
    expect(screen.getByText('テスト商品')).toBeInTheDocument()
  })

  it('renders "すべて見る" button', () => {
    render(<ContentList title="テスト商品" items={[]} />)
    
    expect(screen.getByText('すべて見る')).toBeInTheDocument()
  })

  it('renders loading skeleton when loading', () => {
    // Mock pending fetch
    vi.mocked(fetch).mockImplementation(() => new Promise(() => {}))
    
    render(<ContentList title="テスト商品" />)
    
    const skeletonCards = document.querySelectorAll('.animate-pulse')
    expect(skeletonCards.length).toBeGreaterThan(0)
  })

  it('renders content items when provided as props', () => {
    render(<ContentList title="テスト商品" items={mockContentData} />)
    
    expect(screen.getByText('ワイヤレスヘッドホン')).toBeInTheDocument()
    expect(screen.getByText('electronics')).toBeInTheDocument()
  })

  it('renders error state when fetch fails', async () => {
    vi.mocked(fetch).mockRejectedValue(new Error('Failed to fetch content'))
    
    render(<ContentList title="テスト商品" />)
    
    await vi.waitFor(() => {
      expect(screen.queryByText(/Error loading content/)).toBeInTheDocument()
    }, { timeout: 1000 })
  })

  it('displays badges correctly', () => {
    render(<ContentList title="テスト商品" items={mockContentData} />)
    
    expect(screen.getByText('新着')).toBeInTheDocument()
    expect(screen.getByText('セール')).toBeInTheDocument()
  })
})