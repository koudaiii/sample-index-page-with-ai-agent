import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { API_ENDPOINTS } from "@/lib/config"

interface ContentItem {
  id: string
  title: string
  price: number
  originalPrice?: number
  rating: number
  imageUrl: string
  category: string
  isNew?: boolean
  isSale?: boolean
  isRecommended?: boolean
}

interface ContentListProps {
  title: string
  items?: ContentItem[]
}

export function ContentList({ title, items }: ContentListProps) {
  const [contentItems, setContentItems] = useState<ContentItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (items) {
      setContentItems(items)
      setLoading(false)
      return
    }

    const fetchContent = async () => {
      try {
        const response = await fetch(API_ENDPOINTS.CONTENT)
        if (!response.ok) {
          throw new Error('Failed to fetch content')
        }
        const data = await response.json()
        setContentItems(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [items])

  if (loading) {
    return (
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
          <Button variant="ghost" className="text-accent hover:text-accent/80">
            すべて見る
          </Button>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, index) => (
            <Card key={index} className="overflow-hidden animate-pulse">
              <div className="aspect-square bg-gray-300" />
              <CardContent className="p-4 space-y-3">
                <div className="h-4 bg-gray-300 rounded w-3/4" />
                <div className="h-4 bg-gray-300 rounded w-1/2" />
                <div className="h-4 bg-gray-300 rounded w-1/4" />
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
        </div>
        <div className="text-center text-red-600">
          Error loading content: {error}
        </div>
      </section>
    )
  }

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
        <Button variant="ghost" className="text-accent hover:text-accent/80">
          すべて見る
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {contentItems.map((item) => (
          <Card key={item.id} className="group overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer">
            <div className="relative aspect-square overflow-hidden">
              <img
                src={item.imageUrl}
                alt={item.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute top-3 left-3 flex gap-2">
                {item.isNew && (
                  <Badge className="bg-green-500 hover:bg-green-500">新着</Badge>
                )}
                {item.isSale && (
                  <Badge className="bg-red-500 hover:bg-red-500">セール</Badge>
                )}
                {item.isRecommended && (
                  <Badge className="bg-accent hover:bg-accent">おすすめ</Badge>
                )}
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="absolute top-3 right-3 bg-white/10 backdrop-blur hover:bg-white/20 text-white opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <span className="text-base">♡</span>
              </Button>
            </div>

            <CardContent className="p-4 space-y-3">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">{item.category}</p>
                <h3 className="font-medium leading-tight line-clamp-2">{item.title}</h3>
              </div>

              <div className="flex items-center gap-1">
                <span className="text-yellow-400 text-sm">★</span>
                <span className="text-sm font-medium">{item.rating}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-semibold">¥{item.price.toLocaleString()}</span>
                    {item.originalPrice && (
                      <span className="text-sm text-muted-foreground line-through">
                        ¥{item.originalPrice.toLocaleString()}
                      </span>
                    )}
                  </div>
                </div>

                <Button size="icon" variant="outline" className="shrink-0">
                  <span className="text-base">🛒</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}