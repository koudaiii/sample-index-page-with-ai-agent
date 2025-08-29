from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
from typing import List, Optional

from models import BannerItem, ContentItem

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
    """Get all banner items"""
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
