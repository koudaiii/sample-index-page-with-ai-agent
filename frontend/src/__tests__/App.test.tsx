import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

// Mock the components
vi.mock('@/components/Header', () => ({
  Header: () => <header data-testid="header">Header Component</header>
}))

vi.mock('@/components/Banner', () => ({
  Banner: () => <div data-testid="banner">Banner Component</div>
}))

vi.mock('@/components/ContentList', () => ({
  ContentList: ({ title }: { title: string }) => (
    <div data-testid={`content-list-${title}`}>ContentList: {title}</div>
  )
}))

describe('App', () => {
  it('renders the Header component', () => {
    render(<App />)
    
    expect(screen.getByTestId('header')).toBeInTheDocument()
  })

  it('renders the Banner component', () => {
    render(<App />)
    
    expect(screen.getByTestId('banner')).toBeInTheDocument()
  })

  it('renders three ContentList components with correct titles', () => {
    render(<App />)
    
    expect(screen.getByTestId('content-list-おすすめ商品')).toBeInTheDocument()
    expect(screen.getByTestId('content-list-新着アイテム')).toBeInTheDocument()
    expect(screen.getByTestId('content-list-セール中')).toBeInTheDocument()
    
    expect(screen.getByText('ContentList: おすすめ商品')).toBeInTheDocument()
    expect(screen.getByText('ContentList: 新着アイテム')).toBeInTheDocument()
    expect(screen.getByText('ContentList: セール中')).toBeInTheDocument()
  })

  it('has correct main container structure and styling', () => {
    const { container } = render(<App />)
    
    const appContainer = container.firstChild as Element
    expect(appContainer).toHaveClass('min-h-screen', 'bg-background', 'font-sans')
    
    const mainElement = container.querySelector('main')
    expect(mainElement).toBeInTheDocument()
    expect(mainElement).toHaveClass('container', 'mx-auto', 'px-4', 'py-8', 'space-y-12')
  })

  it('renders separators between content sections', () => {
    const { container } = render(<App />)
    
    // Should have separators between content sections
    const separators = container.querySelectorAll('[data-orientation="horizontal"]')
    expect(separators).toHaveLength(2) // Two separators between three content sections
  })

  it('renders components in correct order', () => {
    render(<App />)
    
    const header = screen.getByTestId('header')
    const banner = screen.getByTestId('banner')
    const recommendedContent = screen.getByTestId('content-list-おすすめ商品')
    const newContent = screen.getByTestId('content-list-新着アイテム')
    const saleContent = screen.getByTestId('content-list-セール中')
    
    // Check that elements appear in the correct DOM order
    const allElements = [header, banner, recommendedContent, newContent, saleContent]
    
    for (let i = 0; i < allElements.length - 1; i++) {
      expect(allElements[i].compareDocumentPosition(allElements[i + 1]))
        .toBe(Node.DOCUMENT_POSITION_FOLLOWING)
    }
  })

  it('has proper semantic structure with header and main elements', () => {
    render(<App />)
    
    expect(screen.getByRole('banner')).toBeInTheDocument() // Header should have role="banner"
    expect(screen.getByRole('main')).toBeInTheDocument() // Main should have role="main"
  })
})