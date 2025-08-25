import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ChevronLeft, ChevronRight } from "@phosphor-icons/react"

interface BannerItem {
  id: string
  title: string
  subtitle: string
  imageUrl: string
  tag: string
  color: string
}

const bannerItems: BannerItem[] = [
  {
    id: "1",
    title: "新春セール開催中",
    subtitle: "最大50%OFF！人気商品をお得にゲット",
    imageUrl: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=400&fit=crop",
    tag: "特別価格",
    color: "bg-red-500"
  },
  {
    id: "2", 
    title: "春の新作コレクション",
    subtitle: "トレンドアイテムが続々登場",
    imageUrl: "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800&h=400&fit=crop",
    tag: "新着",
    color: "bg-green-500"
  },
  {
    id: "3",
    title: "プレミアム会員限定",
    subtitle: "特別な商品とサービスをお楽しみください",
    imageUrl: "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=800&h=400&fit=crop",
    tag: "限定",
    color: "bg-purple-500"
  }
]

export function Banner() {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % bannerItems.length)
    }, 3000)

    return () => clearInterval(timer)
  }, [])

  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + bannerItems.length) % bannerItems.length)
  }

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % bannerItems.length)
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
          <ChevronLeft className="h-4 w-4" />
        </Button>

        <Button
          variant="outline"
          size="icon"
          className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/10 backdrop-blur border-white/20 text-white hover:bg-white/20"
          onClick={goToNext}
        >
          <ChevronRight className="h-4 w-4" />
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