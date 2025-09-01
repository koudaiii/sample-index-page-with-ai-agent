# Content Index Platform

コンテンツプラットフォームのメインインデックス画面。ユーザーが商品やおすすめ企画、新着コンテンツを効率的に発見し閲覧できるハブとして機能します。

## Features

### 実装済み機能
- **グローバルヘッダー**: サイトナビゲーション、ロゴ、検索機能
- **ローテーションバナー**: おすすめコンテンツを3秒間隔で自動ローテーション表示
- **コンテンツリスト**: 商品を「おすすめ商品」「新着アイテム」「セール中」のセクションに分けて表示
- **レスポンシブデザイン**: モバイル・デスクトップ対応
- **shadcn/ui**: モダンなUIコンポーネントライブラリを使用

### デザイン仕様
- **カラーパレット**: Deep Navy、Warm Gray、Coral Orangeの類似色系統
- **フォント**: Inter フォントファミリーで統一
- **コンポーネント**: Header、Carousel、Card、Button、Badge、Separatorを活用

## Architecture

- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python (データAPI用)
- **UI Library**: shadcn/ui + Radix UI
- **AI Integration**: Azure AI Foundry Agent Service
- **Deployment**: Docker + Azure App Service

## Usage

### 開発環境セットアップ

1. [Azure AI Foundry](https://learn.microsoft.com/ja-jp/azure/ai-foundry/agents/environment-setup)

- `PROJECT_ENDPOINT`: 
- `AZURE_AI_AGENT_ID`: 

2. Create account for application

```bash
script/setup --project-name your-ai-project-name --resource-group your-resource-group-name
```

3. Run application

```bash
cd frontend
script/server
```

```bash
cd backend
script/server
```

### データ構造

- **バナーデータ**: `backend/data/banners.json` - 3つのローテーションバナー情報
- **コンテンツデータ**: `backend/data/content.json` - 6つの商品アイテム（おすすめ、新着、セール情報を含む）

## License

MIT
