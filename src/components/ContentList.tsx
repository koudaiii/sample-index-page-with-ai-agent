import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Star, Heart, ShoppingCart } from "@phosphor-icons/react"

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

const contentItems: ContentItem[] = [
  {
    id: "1",
    title: "プレミアムワイヤレスヘッドホン",
    price: 15800,
    originalPrice: 19800,
    rating: 4.8,
    imageUrl: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
    category: "オーディオ",
    isSale: true,
    isRecommended: true
  },
  {
    id: "2",
    title: "スマートウォッチ Gen5",
    price: 28900,
    rating: 4.6,
    imageUrl: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
    category: "ウェアラブル",
    isNew: true
  },
  {
    id: "3",
    title: "ミニマリストバックパック",
    price: 8900,
    originalPrice: 12900,
    rating: 4.9,
    imageUrl: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
    category: "バッグ",
    isSale: true
  },
  {
    id: "4",
    title: "アロマディフューザー",
    price: 5400,
    rating: 4.7,
    imageUrl: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop",
    category: "ホーム",
    isRecommended: true
  },
  {
    id: "5",
    title: "エコフレンドリー水筒",
    price: 3200,
    rating: 4.5,
    imageUrl: "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop",
    category: "キッチン",
    isNew: true
  },
  {
    id: "6",
    title: "ワイヤレス充電パッド",
    price: 4800,
    originalPrice: 6800,
    rating: 4.4,
    imageUrl: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=400&fit=crop",
    category: "テック",
    isSale: true
  }
]

interface ContentListProps {
  title: string
  items?: ContentItem[]
}

export function ContentList({ title, items = contentItems }: ContentListProps) {
  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
        <Button variant="ghost" className="text-accent hover:text-accent/80">
          すべて見る
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((item) => (
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
                <Heart className="h-4 w-4" />
              </Button>
            </div>

            <CardContent className="p-4 space-y-3">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">{item.category}</p>
                <h3 className="font-medium leading-tight line-clamp-2">{item.title}</h3>
              </div>

              <div className="flex items-center gap-1">
                <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
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
                  <ShoppingCart className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}