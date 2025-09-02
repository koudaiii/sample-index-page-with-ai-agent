import { Header } from "@/components/Header"
import { Banner } from "@/components/Banner"
import { ContentList } from "@/components/ContentList"
import { Separator } from "@/components/ui/separator"
import { useEffect, useState } from "react"

interface AppProps {
  query?: string;
}

function App({ query: propsQuery }: AppProps = {}) {
  const [query, setQuery] = useState<string | undefined>(propsQuery)
  const [useAi, setUseAi] = useState<boolean>(false)

  useEffect(() => {
    // URLクエリパラメータを読み取る
    const urlParams = new URLSearchParams(window.location.search)
    const queryParam = urlParams.get('query')
    const useAiParam = urlParams.get('use_ai')
    
    if (queryParam) {
      setQuery(queryParam)
    } else if (!propsQuery) {
      // デフォルトクエリを設定（propsでqueryが渡されていない場合のみ）
      setQuery("真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。")
    }
    
    if (useAiParam) {
      setUseAi(useAiParam.toLowerCase() === 'true')
    }
  }, [propsQuery])
  return (
    <div className="min-h-screen bg-background font-sans">
      <Header />
      
      <main className="container mx-auto px-4 py-8 space-y-12">
        <Banner query={query} useAi={useAi} />
        
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