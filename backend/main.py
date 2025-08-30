from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

from models import BannerItem, ContentItem

# Load environment variables from .env file
load_dotenv()

# Check if Azure agent should be enabled via environment variable
AZURE_AGENT_AVAILABLE = os.getenv("AZURE_AGENT_AVAILABLE", "false").lower() == "true"

# Optional import for Azure agent - make it graceful
if AZURE_AGENT_AVAILABLE:
    try:
        from azure_agent_sample import get_recommendation
        print("Azure agent enabled and imported successfully")
    except ImportError as e:
        AZURE_AGENT_AVAILABLE = False
        print(f"Azure agent import failed: {e} - running without AI recommendations")
else:
    print("Azure agent disabled via environment variable")

# Load data on startup
banners_data: List[BannerItem] = []
content_data: List[ContentItem] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load data on startup
    global banners_data, content_data
    
    # Load banners
    banners_path = Path(__file__).parent / "data" / "banners.json"
    if banners_path.exists():
        with open(banners_path, "r", encoding="utf-8") as f:
            banners_json = json.load(f)
            banners_data = [BannerItem(**item) for item in banners_json]
    
    # Load content
    content_path = Path(__file__).parent / "data" / "content.json"
    if content_path.exists():
        with open(content_path, "r", encoding="utf-8") as f:
            content_json = json.load(f)
            content_data = [ContentItem(**item) for item in content_json]
    
    yield
    # Cleanup if needed

app = FastAPI(
    title="Content Index API",
    description="API for Content Index Page with Azure AI Foundry Agent Service integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Content Index API is running"}

@app.get("/api/banners", response_model=List[BannerItem])
async def get_banners():
    """Get all banner items with Azure AI recommendation"""
    # Only try to get AI recommendation if Azure agent is available
    if AZURE_AGENT_AVAILABLE:
        try:
            # Get recommendation from Azure AI agent
            recommendation = get_recommendation()
            
            # If we get a recommendation, create a banner from it
            if recommendation:
                rec_banner = BannerItem(
                    id=f"rec_{recommendation.get('id', 'ai_recommendation')}",
                    title=recommendation.get('title', 'AI おすすめ商品'),
                    subtitle=f"価格: ¥{recommendation.get('price', 0)} | 評価: {recommendation.get('rating', 0)}",
                    imageUrl=recommendation.get('imageUrl', '/placeholder-image.jpg'),
                    tag="AI推薦",
                    color="oklch(0.7 0.15 40)"  # Coral orange from design system
                )
                # Insert recommendation banner at the beginning
                return [rec_banner] + banners_data
        except Exception as e:
            # Log error but continue with regular banners
            print(f"Failed to get AI recommendation: {e}")
    
    return banners_data

@app.get("/api/content", response_model=List[ContentItem])
async def get_content():
    """Get all content items"""
    return content_data

@app.get("/api/content/{category}", response_model=List[ContentItem])
async def get_content_by_category(category: str):
    """Get content items by category"""
    filtered_content = [
        item for item in content_data 
        if item.category.lower() == category.lower()
    ]
    return filtered_content

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
