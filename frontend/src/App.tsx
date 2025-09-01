import { Header } from "@/components/Header"
import { Banner } from "@/components/Banner"
import { ContentList } from "@/components/ContentList"
import { Separator } from "@/components/ui/separator"

interface AppProps {
  query?: string;
}

function App({ query = "真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。" }: AppProps = {}) {
  return (
    <div className="min-h-screen bg-background font-sans">
      <Header />
      
      <main className="container mx-auto px-4 py-8 space-y-12">
        <Banner query={query} />
        
        <ContentList title="おすすめ商品" />
        
        <Separator />
        
        <ContentList title="新着アイテム" />
        
        <Separator />
        
        <ContentList title="セール中" />
      </main>
    </div>
  )
}

export default App