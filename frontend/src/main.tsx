import { createRoot } from 'react-dom/client'
import { ErrorBoundary } from "react-error-boundary";
import "@github/spark/spark"

import App from './App.tsx'
import { ErrorFallback } from './ErrorFallback.tsx'

import "./main.css"
import "./styles/theme.css"
import "./index.css"

// URLパラメータからクエリを取得
const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get('query') || undefined;

createRoot(document.getElementById('root')!).render(
  <ErrorBoundary FallbackComponent={ErrorFallback}>
    <App query={query} />
   </ErrorBoundary>
)
