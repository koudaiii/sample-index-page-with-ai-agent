import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { API_ENDPOINTS } from "@/lib/config"

interface BannerItem {
  id: string
  title: string
  subtitle: string
  imageUrl: string
  tag: string
  color: string
}

interface BannerProps {
  query?: string;
}

export function Banner({ query }: BannerProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [bannerItems, setBannerItems] = useState<BannerItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBanners = async () => {
      try {
        let url = API_ENDPOINTS.BANNERS;
        if (query) {
          const params = new URLSearchParams({ query });
          url = `${API_ENDPOINTS.BANNERS}?${params}`;
        }
        
        const response = await fetch(url)
        if (!response.ok) {
          throw new Error('Failed to fetch banners')
        }
        const data = await response.json()
        setBannerItems(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchBanners()
  }, [query])

  useEffect(() => {
    if (bannerItems.length === 0) return
    
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % bannerItems.length)
    }, 3000)

    return () => clearInterval(timer)
  }, [bannerItems.length])

  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + bannerItems.length) % bannerItems.length)
  }

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % bannerItems.length)
  }

  if (loading) {
    return (
      <div className="relative w-full h-64 md:h-80 lg:h-96 overflow-hidden rounded-lg">
        <Card className="relative h-full border-0 animate-pulse">
          <div className="absolute inset-0 bg-gray-300" />
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <div className="relative w-full h-64 md:h-80 lg:h-96 overflow-hidden rounded-lg">
        <Card className="relative h-full border-0">
          <div className="absolute inset-0 bg-red-100 flex items-center justify-center">
            <p className="text-red-600">Error loading banners: {error}</p>
          </div>
        </Card>
      </div>
    )
  }

  if (bannerItems.length === 0) {
    return null
  }

  const currentItem = bannerItems[currentIndex]

  return (
    <div className="relative w-full h-64 md:h-80 lg:h-96 overflow-hidden rounded-lg">
      <Card className="relative h-full border-0">
        <div
          className="absolute inset-0 bg-cover bg-center transition-all duration-500 ease-in-out"
          style={{ backgroundImage: `url(${currentItem.imageUrl})` }}
        >
          <div className="absolute inset-0 bg-black/40" />
          <div className="relative h-full flex flex-col justify-center px-6 md:px-12 text-white">
            <Badge className={`${currentItem.color} text-white w-fit mb-4`}>
              {currentItem.tag}
            </Badge>
            <h2 className="text-2xl md:text-4xl font-bold mb-2">
              {currentItem.title}
            </h2>
            <p className="text-lg md:text-xl mb-6 max-w-2xl">
              {currentItem.subtitle}
            </p>
            <Button className="w-fit bg-accent hover:bg-accent/90">
              詳しく見る
            </Button>
          </div>
        </div>

        <Button
          variant="outline"
          size="icon"
          className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur border-white/20 text-white hover:bg-white/20"
          onClick={goToPrevious}
        >
          <span className="text-lg font-bold">‹</span>
        </Button>

        <Button
          variant="outline"
          size="icon"
          className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur border-white/20 text-white hover:bg-white/20"
          onClick={goToNext}
        >
          <span className="text-lg font-bold">›</span>
        </Button>

        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
          {bannerItems.map((_, index) => (
            <button
              key={index}
              className={`h-2 w-8 rounded-full transition-all ${
                index === currentIndex ? "bg-white" : "bg-white/50"
              }`}
              onClick={() => setCurrentIndex(index)}
            />
          ))}
        </div>
      </Card>
    </div>
  )
}