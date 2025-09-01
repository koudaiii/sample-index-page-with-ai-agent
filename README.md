# Content Index Platform

コンテンツプラットフォームのメインインデックス画面。ユーザーが商品やおすすめ企画、新着コンテンツを効率的に発見し閲覧できるハブとして機能します。

## 🏗️ Architecture

- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS
- **Backend**: Python + FastAPI + Azure AI Foundry Agent Service
- **Testing**: Vitest (Frontend) + pytest (Backend)
- **CI/CD**: GitHub Actions

## 📁 Project Structure

```
.
├── frontend/          # React frontend application
├── backend/           # Python backend API
├── script/            # Build and deployment scripts
├── .github/           # GitHub Actions workflows
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.12+
- **uv** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd index
   ```

2. **Backend Setup**
   ```bash
   cd backend/
   uv sync --dev
   ```

3. **Frontend Setup**
   ```bash
   cd frontend/
   npm install --legacy-peer-deps
   ```

## 🧪 Testing

### Run All Tests (CI Script)
```bash
./script/ci-test
```

### Backend Tests
```bash
cd backend/
uv run python -m pytest
```

### Frontend Tests
```bash
cd frontend/
npm run test:run
```

### Watch Mode (Development)
```bash
# Frontend
npm run test

# Backend
uv run python -m pytest --watch
```

## 🛠️ Development

### Frontend Development
```bash
cd frontend/
npm run dev
```

### Backend Development
```bash
cd backend/
uv run uvicorn main:app --reload
```

### Linting
```bash
cd frontend/
npm run lint
```

## 🏗️ Build

### Frontend Build
```bash
cd frontend/
npm run build
```

### Production Preview
```bash
npm run preview
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

- **Push to main/develop**: Runs full test suite with multiple Node.js versions
- **Pull Requests**: Runs quick tests, code quality checks, and security audits
- **Integration Tests**: Uses the `script/ci-test` script for comprehensive testing

### CI Workflow Features

- ✅ Matrix testing (Node.js 18, 20 × Python 3.12)
- ✅ Dependency caching for faster builds
- ✅ Test result artifacts
- ✅ Code coverage reporting
- ✅ Security vulnerability scanning
- ✅ TypeScript type checking
- ✅ ESLint code quality checks

## 🧩 Features

### 実装済み機能
- **グローバルヘッダー**: サイトナビゲーション、ロゴ、検索機能
- **ローテーションバナー**: おすすめコンテンツを3秒間隔で自動ローテーション表示
- **コンテンツリスト**: 商品を「おすすめ商品」「新着アイテム」「セール中」のセクションに分けて表示
- **レスポンシブデザイン**: モバイル・デスクトップ対応
- **Unit Tests**: フロントエンド・バックエンド両方の包括的テスト
- **CI/CD**: GitHub Actions による自動テスト実行

### デザイン仕様
- **カラーパレット**: Deep Navy、Warm Gray、Coral Orangeの類似色系統
- **フォント**: Inter フォントファミリーで統一
- **コンポーネント**: Header、Carousel、Card、Button、Badge、Separatorを活用

### Testing Coverage
- **Unit Tests**: Component and function level testing
- **Integration Tests**: End-to-end workflow testing
- **Error Handling**: Comprehensive fallback scenario testing
- **Responsive Design**: Mobile and desktop compatibility testing

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
