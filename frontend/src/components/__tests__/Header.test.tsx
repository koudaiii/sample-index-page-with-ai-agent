import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Header } from '../Header'
import * as useMobileHook from '@/hooks/use-mobile'

// Mock the use-mobile hook
vi.mock('@/hooks/use-mobile')
const mockUseIsMobile = vi.mocked(useMobileHook.useIsMobile)

describe('Header', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.resetAllMocks()
  })

  it('renders the logo and site name', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    expect(screen.getByText('ContentHub')).toBeInTheDocument()
  })

  it('renders navigation links on desktop', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    expect(screen.getByText('ホーム')).toBeInTheDocument()
    expect(screen.getByText('商品')).toBeInTheDocument()
    expect(screen.getByText('新着')).toBeInTheDocument()
    expect(screen.getByText('おすすめ')).toBeInTheDocument()
  })

  it('hides navigation links on mobile', () => {
    mockUseIsMobile.mockReturnValue(true)
    
    render(<Header />)
    
    expect(screen.queryByText('ホーム')).not.toBeInTheDocument()
    expect(screen.queryByText('商品')).not.toBeInTheDocument()
    expect(screen.queryByText('新着')).not.toBeInTheDocument()
    expect(screen.queryByText('おすすめ')).not.toBeInTheDocument()
  })

  it('renders search input on desktop', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    const searchInput = screen.getByPlaceholderText('商品を検索...')
    expect(searchInput).toBeInTheDocument()
    expect(searchInput).toHaveAttribute('id', 'search-input')
  })

  it('hides search input on mobile', () => {
    mockUseIsMobile.mockReturnValue(true)
    
    render(<Header />)
    
    expect(screen.queryByPlaceholderText('商品を検索...')).not.toBeInTheDocument()
  })

  it('renders action buttons', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    const favoriteButtons = screen.getAllByText('♡')
    const cartButtons = screen.getAllByText('🛒')
    
    expect(favoriteButtons.length).toBeGreaterThan(0)
    expect(cartButtons.length).toBeGreaterThan(0)
  })

  it('shows hamburger menu button on mobile', () => {
    mockUseIsMobile.mockReturnValue(true)
    
    render(<Header />)
    
    expect(screen.getByText('☰')).toBeInTheDocument()
  })

  it('hides hamburger menu button on desktop', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    expect(screen.queryByText('☰')).not.toBeInTheDocument()
  })

  it('has correct header styling classes', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    const headerElement = screen.getByRole('banner')
    expect(headerElement).toHaveClass('sticky', 'top-0', 'z-50', 'w-full', 'border-b')
  })

  it('navigation links have correct hover classes', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    const homeLink = screen.getByText('ホーム')
    expect(homeLink).toHaveClass('hover:text-accent', 'transition-colors')
  })

  it('search input has correct placeholder and styling', () => {
    mockUseIsMobile.mockReturnValue(false)
    
    render(<Header />)
    
    const searchInput = screen.getByPlaceholderText('商品を検索...')
    expect(searchInput).toHaveClass('w-64', 'pl-10')
  })
})