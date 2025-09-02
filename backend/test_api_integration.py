import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json

from main import app

client = TestClient(app)

class TestAPIIntegration:
    
    def test_root_endpoint(self):
        """Test root endpoint returns expected message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Content Index API is running"}
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_get_banners_without_ai(self):
        """Test get banners without AI recommendation (default behavior)"""
        response = client.get("/api/banners")
        assert response.status_code == 200
        banners = response.json()
        assert isinstance(banners, list)
        # Should return regular banners without AI recommendation
        # Check that none of the banner IDs start with "rec_" (AI recommendation prefix)
        for banner in banners:
            assert not banner["id"].startswith("rec_")
    
    def test_get_banners_with_ai_false(self):
        """Test get banners with use_ai=false explicitly"""
        response = client.get("/api/banners?use_ai=false")
        assert response.status_code == 200
        banners = response.json()
        assert isinstance(banners, list)
        # Should return regular banners without AI recommendation
        for banner in banners:
            assert not banner["id"].startswith("rec_")
    
    @patch('main.get_recommendation')
    @patch('main.AZURE_AGENT_IMPORT_AVAILABLE', True)
    def test_get_banners_with_ai_true(self, mock_get_recommendation):
        """Test get banners with use_ai=true and successful AI recommendation"""
        # Mock AI recommendation response
        mock_recommendation = {
            "id": "bottle-001",
            "title": "保温水筒 500ml",
            "price": 2980,
            "rating": 4.5,
            "imageUrl": "/images/bottle.jpg",
            "category": "drinkware",
            "isRecommended": True
        }
        mock_get_recommendation.return_value = mock_recommendation
        
        response = client.get("/api/banners?use_ai=true")
        assert response.status_code == 200
        banners = response.json()
        assert isinstance(banners, list)
        assert len(banners) > 0
        
        # First banner should be the AI recommendation
        ai_banner = banners[0]
        assert ai_banner["id"] == "rec_bottle-001"
        assert ai_banner["title"] == "保温水筒 500ml"
        assert "価格: ¥2980" in ai_banner["subtitle"]
        assert "評価: 4.5" in ai_banner["subtitle"]
        assert ai_banner["tag"] == "AIモニター募集中"
        assert ai_banner["color"] == "oklch(0.7 0.15 40)"
        
        # Verify the AI agent was called
        mock_get_recommendation.assert_called_once_with(None)
    
    @patch('main.get_recommendation')
    @patch('main.AZURE_AGENT_IMPORT_AVAILABLE', True)
    def test_get_banners_with_ai_and_query(self, mock_get_recommendation):
        """Test get banners with use_ai=true and custom query"""
        mock_recommendation = {
            "id": "custom-001",
            "title": "カスタム商品",
            "price": 1500,
            "rating": 4.0,
            "imageUrl": "/images/custom.jpg",
            "category": "custom",
            "isRecommended": True
        }
        mock_get_recommendation.return_value = mock_recommendation
        
        response = client.get("/api/banners?use_ai=true&query=カスタム検索")
        assert response.status_code == 200
        banners = response.json()
        
        # First banner should be the AI recommendation
        ai_banner = banners[0]
        assert ai_banner["id"] == "rec_custom-001"
        assert ai_banner["title"] == "カスタム商品"
        
        # Verify the AI agent was called with the custom query
        mock_get_recommendation.assert_called_once_with("カスタム検索")
    
    @patch('main.get_recommendation')
    @patch('main.AZURE_AGENT_IMPORT_AVAILABLE', True)
    def test_get_banners_with_ai_error_fallback(self, mock_get_recommendation):
        """Test get banners with AI error falls back to regular banners"""
        # Mock AI recommendation to raise an exception
        mock_get_recommendation.side_effect = Exception("AI service error")
        
        response = client.get("/api/banners?use_ai=true")
        assert response.status_code == 200
        banners = response.json()
        assert isinstance(banners, list)
        
        # Should return regular banners without AI recommendation on error
        for banner in banners:
            assert not banner["id"].startswith("rec_")
        
        # Verify the AI agent was called
        mock_get_recommendation.assert_called_once_with(None)
    
    @patch('main.AZURE_AGENT_IMPORT_AVAILABLE', False)
    def test_get_banners_with_ai_unavailable(self):
        """Test get banners when AI agent is not available"""
        response = client.get("/api/banners?use_ai=true")
        assert response.status_code == 200
        banners = response.json()
        assert isinstance(banners, list)
        
        # Should return regular banners without AI recommendation
        for banner in banners:
            assert not banner["id"].startswith("rec_")
    
    @patch('main.get_recommendation')
    @patch('main.AZURE_AGENT_IMPORT_AVAILABLE', True)
    def test_get_banners_with_ai_empty_response(self, mock_get_recommendation):
        """Test get banners when AI returns empty/None response"""
        mock_get_recommendation.return_value = None
        
        response = client.get("/api/banners?use_ai=true")
        assert response.status_code == 200
        banners = response.json()
        assert isinstance(banners, list)
        
        # Should return regular banners when AI returns empty response
        for banner in banners:
            assert not banner["id"].startswith("rec_")
        
        mock_get_recommendation.assert_called_once_with(None)
    
    def test_get_content(self):
        """Test get all content items"""
        response = client.get("/api/content")
        assert response.status_code == 200
        content = response.json()
        assert isinstance(content, list)
    
    def test_get_content_by_category(self):
        """Test get content items by category"""
        # Test with a generic category name
        response = client.get("/api/content/general")
        assert response.status_code == 200
        content = response.json()
        assert isinstance(content, list)
        # If there are items, they should all be from the requested category
        for item in content:
            assert item["category"].lower() == "general"
