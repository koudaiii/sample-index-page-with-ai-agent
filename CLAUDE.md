# Content Index Page - コンテンツインデックスページ

このリポジトリは、コンテンツプラットフォームのメインインデックス画面を提供するReact + TypeScriptアプリケーションです。GitHub Sparkテンプレートをベースに構築されています。

## プロジェクト概要

ユーザーが商品やおすすめ企画、新着コンテンツを効率的に発見・閲覧できるハブとして機能するコンテンツインデックスページです。

### 主な特徴
- **グローバルヘッダー**: サイトナビゲーション、ロゴ、検索機能
- **ローテーションバナー**: おすすめコンテンツを3秒間隔で自動表示
- **コンテンツリスト**: 商品、おすすめ品、新企画をグリッド表示

## 技術スタック

- **フレームワーク**: React 19 + TypeScript
- **ビルドツール**: Vite 6
- **スタイリング**: TailwindCSS 4
- **UIコンポーネント**: shadcn/ui + Radix UI
- **アニメーション**: Framer Motion
- **アイコン**: Lucide React, Heroicons, Phosphor Icons
- **開発ツール**: ESLint, TypeScript

## ディレクトリ構成

```
src/
├── components/          # Reactコンポーネント
│   ├── Banner.tsx      # ローテーションバナー
│   ├── ContentList.tsx # コンテンツグリッド
│   ├── Header.tsx      # グローバルヘッダー
│   └── ui/            # shadcn/ui コンポーネント
├── hooks/             # カスタムフック
├── lib/               # ユーティリティ関数
└── styles/           # CSSファイル
```

## 開発コマンド

### ローカル環境
```bash
# 開発サーバー起動
npm run dev

# ビルド
npm run build

# リント実行
npm run lint

# プレビュー
npm run preview

# ポート5000終了
npm run kill
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

## デザイン仕様

### カラーパレット
- **Primary**: Deep Navy (oklch(0.25 0.05 240))
- **Secondary**: Warm Gray (oklch(0.85 0.02 60))
- **Accent**: Coral Orange (oklch(0.7 0.15 40))
- **Background**: Light Gray (oklch(0.98 0.01 60))

### フォント
- **フォントファミリー**: Inter
- **階層**: H1(24px Bold) → H2(20px Semibold) → H3(16px Medium) → Body(14px Regular)

## 主要コンポーネント

### App.tsx:9
メインアプリケーションコンポーネント。ヘッダー、バナー、コンテンツリストを統合して表示。

### components/Header.tsx
グローバルヘッダーコンポーネント。サイトナビゲーションとロゴを提供。

### components/Banner.tsx
自動ローテーション機能付きバナーコンポーネント。おすすめコンテンツを3秒間隔で表示。

### components/ContentList.tsx
商品やコンテンツをグリッド形式で表示するリストコンポーネント。

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

アプリケーションはDockerコンテナで実行可能です。

### 構成
- **Dockerfile**: Node.js 20 Alpine imageベース
- **docker-compose.yml**: 開発環境用設定
- **.dockerignore**: 不要ファイルの除外設定

### 特徴
- Vite開発サーバーをポート5173で公開
- ホットリロード対応（ボリュームマウント）
- 依存関係はコンテナ内で管理

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

## ライセンス

MIT License - GitHub Spark Template Resources