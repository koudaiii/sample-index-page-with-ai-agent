# Sample Index page with AI Agent

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

1. [Azure AI Foundry](https://learn.microsoft.com/ja-jp/azure/ai-foundry/agents/environment-setup)

Add these environment variables to `backend/.env` 

- Create an agent from the project and obtain the following values:
   - `PROJECT_ENDPOINT`: 
   - `AZURE_AI_AGENT_ID`: 
- Upload `backend/data/content.js` to register knowledge

2. Create account for application

```bash
script/setup --project-name your-ai-project-name --resource-group your-resource-group-name
```

3. Setup .env

- frontend/.env
  - `VITE_API_BASE_URL=http://localhost:8000`
- backend/.env
  - `PROJECT_ENDPOINT`
  - `AZURE_AI_AGENT_ID`
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`

4. Run application

```bash
script/bootstrap
script/docker-build
script/docker-server
```

## License

MIT
