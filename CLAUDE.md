# Content Index Page - コンテンツインデックスページ

このリポジトリは、コンテンツプラットフォームのメインインデックス画面を提供するReact + TypeScriptアプリケーションです。GitHub Sparkテンプレートをベースに構築されています。

## プロジェクト概要

ユーザーが商品やおすすめ企画、新着コンテンツを効率的に発見・閲覧できるハブとして機能するコンテンツインデックスページです。

### 主な特徴
- **グローバルヘッダー**: サイトナビゲーション、ロゴ、検索機能
- **ローテーションバナー**: おすすめコンテンツを3秒間隔で自動表示
- **コンテンツリスト**: 商品、おすすめ品、新企画をグリッド表示

## 技術スタック

### フロントエンド
- **フレームワーク**: React 19 + TypeScript
- **ビルドツール**: Vite 6
- **スタイリング**: TailwindCSS 4
- **UIコンポーネント**: shadcn/ui + Radix UI
- **アニメーション**: Framer Motion
- **アイコン**: Lucide React, Heroicons, Phosphor Icons
- **開発ツール**: ESLint, TypeScript

### バックエンド
- **フレームワーク**: FastAPI + Python 3.12
- **ASGI サーバー**: Uvicorn
- **データ**: JSON ファイル (モックデータ)
- **Azure連携**: Azure AI Foundry Agent Service 対応準備済み
- **CORS**: フロントエンド通信対応

## ディレクトリ構成

```
frontend/              # フロントエンドソース
├── src/               # Reactアプリケーション
│   ├── components/    # Reactコンポーネント
│   │   ├── Banner.tsx # ローテーションバナー (API連携済み)
│   │   ├── ContentList.tsx # コンテンツグリッド (API連携済み)  
│   │   ├── Header.tsx # グローバルヘッダー
│   │   └── ui/        # shadcn/ui コンポーネント
│   ├── hooks/         # カスタムフック
│   ├── lib/           # ユーティリティ関数
│   └── styles/        # CSSファイル
├── nginx/          # nginx
│   ├── nginx.conf       # メイン設定
│   └── default.conf     # サーバー設定とプロキシ
├── package.json       # npm 依存関係
├── vite.config.ts     # Vite 設定
├── tsconfig.json      # TypeScript 設定
└── tailwind.config.js # TailwindCSS 設定

backend/               # バックエンドソース
├── main.py           # FastAPI アプリケーション
├── models.py         # Pydantic データモデル
├── azure_agent.py    # Azure AI Foundry Agent Service 連携
├── requirements.txt  # Python 依存関係
├── Dockerfile       # 開発用 Docker 設定
├── Dockerfile.prod  # 本番用 Docker 設定
├── .env.example     # 環境変数テンプレート
└── data/            # モックデータ
    ├── banners.json # バナーデータ
    └── content.json # コンテンツデータ


script/               # 実行スクリプト
├── bootstrap         # フロントエンド環境セットアップ
├── server           # フロントエンド開発サーバー起動
├── backend-server   # バックエンドサーバー起動
├── docker-bootstrap # 開発Docker環境構築
├── docker-server    # 開発Dockerサーバー起動
├── docker-shutdown  # 全Dockerサーバー停止
├── compose-bootstrap # 本番Docker環境構築
├── compose-server   # 本番サーバー起動 (Nginx + API)
└── compose-shutdown # 全Docker環境停止

# Docker設定ファイル
├── Dockerfile       # フロントエンド用マルチステージ (dev/prod対応)
├── docker-compose.yml # 統合環境設定
└── .env.example     # 環境変数テンプレート
```

## 開発コマンド

### ローカル環境

#### フロントエンド
```bash
# 環境セットアップ
script/bootstrap

# フロントエンド開発サーバー起動
script/server

# 個別コマンド (frontend ディレクトリで実行)
cd frontend
npm run dev    # 開発サーバー起動
npm run build  # ビルド
npm run lint   # リント実行
npm run kill   # ポート5000終了
```

#### バックエンド
```bash
# バックエンドサーバー起動
script/backend-server

# 手動起動 (backend ディレクトリで実行)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker環境

#### Docker Compose使用
```bash
# Docker Composeで起動
docker-compose up

# バックグラウンドで起動
docker-compose up -d

# 停止
docker-compose down

# イメージを再ビルドして起動
docker-compose up --build
```

#### Docker単体使用
```bash
# イメージをビルド
docker build -t content-index-page .

# コンテナ起動
docker run -p 5173:5173 -v $(pwd):/app -v /app/node_modules content-index-page

# バックグラウンドで起動
docker run -d -p 5173:5173 -v $(pwd):/app -v /app/node_modules --name content-index content-index-page

# コンテナ停止・削除
docker stop content-index
docker rm content-index
```

#### スクリプト使用（推奨）

**開発環境**
```bash
# フロントエンド環境セットアップ
script/bootstrap

# フロントエンドサーバー起動
script/server

# バックエンドサーバー起動 
script/backend-server

# Docker環境セットアップ (frontend + backend)
script/docker-bootstrap

# Dockerサーバー起動 (開発環境)
script/docker-server

# Dockerサーバー停止
script/docker-shutdown
```

**Docker Compose環境**
```bash
# Docker Compose環境セットアップ
script/compose-bootstrap

# Docker Composeサーバー起動 (Nginx + Backend)
script/compose-server

# 全環境停止
script/compose-shutdown
```

## デザイン仕様

### カラーパレット
- **Primary**: Deep Navy (oklch(0.25 0.05 240))
- **Secondary**: Warm Gray (oklch(0.85 0.02 60))
- **Accent**: Coral Orange (oklch(0.7 0.15 40))
- **Background**: Light Gray (oklch(0.98 0.01 60))

### フォント
- **フォントファミリー**: Inter
- **階層**: H1(24px Bold) → H2(20px Semibold) → H3(16px Medium) → Body(14px Regular)

## API エンドポイント

### バックエンドAPI (http://localhost:8000)
- `GET /api/banners` - バナー情報取得
- `GET /api/content` - 全コンテンツ取得
- `GET /api/content/{category}` - カテゴリ別コンテンツ取得
- `GET /health` - ヘルスチェック
- `GET /docs` - API ドキュメント (Swagger UI)

### データ形式
```typescript
// Banner
interface BannerItem {
  id: string
  title: string
  subtitle: string
  imageUrl: string
  tag: string
  color: string
}

// Content
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
```

## 主要コンポーネント

### frontend/src/App.tsx
メインアプリケーションコンポーネント。ヘッダー、バナー、コンテンツリストを統合して表示。

### frontend/src/components/Header.tsx
グローバルヘッダーコンポーネント。サイトナビゲーションとロゴを提供。

### frontend/src/components/Banner.tsx
API連携済みバナーコンポーネント。バックエンドからデータを取得し、3秒間隔で自動ローテーション。ローディング状態とエラーハンドリング対応。

### frontend/src/components/ContentList.tsx
API連携済みコンテンツリストコンポーネント。バックエンドからデータを取得し、グリッド形式で表示。ローディング状態とエラーハンドリング対応。

## Azure AI Foundry Agent Service 連携

### 準備済み機能
- `backend/azure_agent.py` - Azure AI 連携モジュール
- 環境変数設定 (`.env.example`)
- パーソナライゼーション機能の基盤
- 動的コンテンツ生成の準備

### 将来の拡張予定
- ユーザー行動分析
- パーソナライズドレコメンデーション  
- 動的バナー生成
- コンテンツ最適化

## 開発ガイドライン

### コード規約
- TypeScriptの型安全性を活用
- shadcn/uiコンポーネントの使用を推奨
- TailwindCSSのユーティリティクラスでスタイリング
- ESLintルールに従ったコード品質維持

### レスポンシブ対応
- モバイルファースト設計
- ブレークポイント: sm(640px), md(768px), lg(1024px)
- グリッドは1列→2列→3列の段階的表示

### パフォーマンス
- 画像遅延読み込み対応
- バンドルサイズ最適化
- コンポーネントの適切なメモ化

## Docker対応

### 統合Docker構成
- **Dockerfile**: マルチステージビルド (development/builder/production)
- **backend/Dockerfile**: マルチステージビルド (development/production)
- **docker-compose.yml**: Docker Compose統合設定

### Docker Compose環境
- **frontend**: Nginx + Static files (port:80)
- **backend**: 運用モード (internal:8000, 4 workers)
- **特徴**: 最適化、セキュリティ、ヘルスチェック

### アーキテクチャ

#### ローカル開発環境
```
Frontend-dev (localhost:5173) ←直接→ Backend (localhost:8000)
```

#### Docker Compose環境  
```
Frontend: Nginx (localhost:80) → Static Files
                               → /api/* → Backend (internal:8000)
```

### Docker Compose起動
```bash
# Docker Compose環境
docker-compose up

# バックグラウンドで起動
docker-compose up -d
```

### スクリプト詳細

#### ローカル開発環境用
- **script/bootstrap**: フロントエンド環境確認と依存関係インストール
- **script/server**: フロントエンド開発サーバー起動（http://localhost:5173）
- **script/backend-server**: バックエンドサーバー起動（http://localhost:8000）

#### Docker開発環境用
- **script/docker-bootstrap**: 開発Docker環境構築 (`--profile dev`)
- **script/docker-server**: 開発環境コンテナ起動 (Frontend:5173, Backend:8000)
- **script/docker-shutdown**: 全てのDockerコンテナ停止

#### Docker Compose環境用  
- **script/compose-bootstrap**: Docker Compose環境構築
- **script/compose-server**: Docker Compose環境起動 (Nginx:80 + Backend:internal)
- **script/compose-shutdown**: 全Docker環境停止

## トラブルシューティング

### 開発サーバーが起動しない
```bash
npm run kill  # ポート5000を解放
npm run dev   # 再起動
```

### Dockerでの問題
```bash
# コンテナとイメージをクリア
docker-compose down
docker system prune -f

# 再ビルド
docker-compose up --build
```

### ビルドエラー
```bash
npm run lint  # ESLintでエラー確認
npm run build # TypeScriptエラー確認
```

## Azure App Service デプロイメント

### 準備
1. **Docker Hub等へのイメージプッシュ**
```bash
# Docker Composeイメージビルド
script/compose-bootstrap

# イメージタグ付け (compose project名に注意)
docker tag content-index-page-frontend-prod your-registry/content-index-frontend:latest
docker tag content-index-page-backend your-registry/content-index-backend:latest

# レジストリへプッシュ
docker push your-registry/content-index-frontend:latest
docker push your-registry/content-index-backend:latest
```

2. **Azure App Service設定**
- Container設定で`your-registry/content-index-frontend:latest`を指定
- ポート80でリスニング設定
- 環境変数`AZURE_AI_FOUNDRY_*`を設定

3. **バックエンドサービス**
- 別のApp ServiceまたはContainer Instancesでバックエンド実行
- フロントエンドからアクセス可能なURLを設定

### 環境変数
```bash
# フロントエンド (Docker Composeでは不要 - Nginxプロキシを使用)
NODE_ENV=production

# バックエンド
DEBUG=false
AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.azure.com
AZURE_AI_FOUNDRY_API_KEY=your-api-key
```

## ライセンス

MIT License - GitHub Spark Template Resources
