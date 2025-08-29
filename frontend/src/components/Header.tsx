import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useIsMobile } from "@/hooks/use-mobile"

export function Header() {
  const isMobile = useIsMobile()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-primary" />
            <span className="text-xl font-bold tracking-tight">ContentHub</span>
          </div>
          
          {!isMobile && (
            <nav className="flex items-center gap-6">
              <a href="#" className="text-sm font-medium hover:text-accent transition-colors">
                ホーム
              </a>
              <a href="#" className="text-sm font-medium hover:text-accent transition-colors">
                商品
              </a>
              <a href="#" className="text-sm font-medium hover:text-accent transition-colors">
                新着
              </a>
              <a href="#" className="text-sm font-medium hover:text-accent transition-colors">
                おすすめ
              </a>
            </nav>
          )}
        </div>

        <div className="flex items-center gap-4">
          {!isMobile && (
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">🔍</span>
              <Input
                placeholder="商品を検索..."
                className="w-64 pl-10"
                id="search-input"
              />
            </div>
          )}
          
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon">
              <span className="text-lg">♡</span>
            </Button>
            <Button variant="ghost" size="icon">
              <span className="text-lg">🛒</span>
            </Button>
            {isMobile && (
              <Button variant="ghost" size="icon">
                <span className="text-lg">☰</span>
              </Button>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}