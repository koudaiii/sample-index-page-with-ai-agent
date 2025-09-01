import unittest
import pytest
from pydantic import ValidationError
from models import BannerItem, ContentItem


class TestBannerItem(unittest.TestCase):
    
    def test_valid_banner_item_creation(self):
        """Test creating a valid BannerItem"""
        banner_data = {
            "id": "banner-001",
            "title": "夏のセール開始！",
            "subtitle": "最大50%OFF",
            "imageUrl": "/images/summer-sale.jpg",
            "tag": "セール",
            "color": "red"
        }
        
        banner = BannerItem(**banner_data)
        
        self.assertEqual(banner.id, "banner-001")
        self.assertEqual(banner.title, "夏のセール開始！")
        self.assertEqual(banner.subtitle, "最大50%OFF")
        self.assertEqual(banner.imageUrl, "/images/summer-sale.jpg")
        self.assertEqual(banner.tag, "セール")
        self.assertEqual(banner.color, "red")
    
    def test_banner_item_missing_required_fields(self):
        """Test BannerItem validation with missing required fields"""
        incomplete_data = {
            "id": "banner-001",
            "title": "セール"
            # Missing subtitle, imageUrl, tag, color
        }
        
        with self.assertRaises(ValidationError):
            BannerItem(**incomplete_data)
    
    def test_banner_item_empty_strings(self):
        """Test BannerItem with empty string values"""
        banner_data = {
            "id": "",
            "title": "",
            "subtitle": "",
            "imageUrl": "",
            "tag": "",
            "color": ""
        }
        
        # Should still create the object even with empty strings
        banner = BannerItem(**banner_data)
        self.assertEqual(banner.id, "")
        self.assertEqual(banner.title, "")
    
    def test_banner_item_json_serialization(self):
        """Test BannerItem JSON serialization"""
        banner_data = {
            "id": "banner-001",
            "title": "新商品入荷",
            "subtitle": "今すぐチェック",
            "imageUrl": "/images/new-items.jpg",
            "tag": "新着",
            "color": "blue"
        }
        
        banner = BannerItem(**banner_data)
        json_output = banner.model_dump()
        
        self.assertEqual(json_output, banner_data)


class TestContentItem(unittest.TestCase):
    
    def test_valid_content_item_creation(self):
        """Test creating a valid ContentItem"""
        content_data = {
            "id": "item-001",
            "title": "ワイヤレスヘッドホン",
            "price": 15800,
            "originalPrice": 19800,
            "rating": 4.2,
            "imageUrl": "/images/headphones.jpg",
            "category": "electronics",
            "isNew": True,
            "isSale": True,
            "isRecommended": False
        }
        
        item = ContentItem(**content_data)
        
        self.assertEqual(item.id, "item-001")
        self.assertEqual(item.title, "ワイヤレスヘッドホン")
        self.assertEqual(item.price, 15800)
        self.assertEqual(item.originalPrice, 19800)
        self.assertEqual(item.rating, 4.2)
        self.assertEqual(item.imageUrl, "/images/headphones.jpg")
        self.assertEqual(item.category, "electronics")
        self.assertTrue(item.isNew)
        self.assertTrue(item.isSale)
        self.assertFalse(item.isRecommended)
    
    def test_content_item_with_minimal_required_fields(self):
        """Test ContentItem with only required fields"""
        minimal_data = {
            "id": "item-002",
            "title": "シンプル商品",
            "price": 1000,
            "rating": 3.5,
            "imageUrl": "/images/simple.jpg",
            "category": "general"
        }
        
        item = ContentItem(**minimal_data)
        
        self.assertEqual(item.id, "item-002")
        self.assertEqual(item.title, "シンプル商品")
        self.assertEqual(item.price, 1000)
        self.assertIsNone(item.originalPrice)
        self.assertEqual(item.rating, 3.5)
        self.assertFalse(item.isNew)  # Default value
        self.assertFalse(item.isSale)  # Default value
        self.assertFalse(item.isRecommended)  # Default value
    
    def test_content_item_optional_fields_defaults(self):
        """Test ContentItem optional fields have correct defaults"""
        content_data = {
            "id": "item-003",
            "title": "テスト商品",
            "price": 5000,
            "rating": 4.0,
            "imageUrl": "/images/test.jpg",
            "category": "test"
        }
        
        item = ContentItem(**content_data)
        
        # Check default values for optional fields
        self.assertIsNone(item.originalPrice)
        self.assertFalse(item.isNew)
        self.assertFalse(item.isSale)
        self.assertFalse(item.isRecommended)
    
    def test_content_item_negative_price_validation(self):
        """Test ContentItem handles negative prices (Pydantic allows this by default)"""
        content_data = {
            "id": "item-004",
            "title": "負の価格商品",
            "price": -1000,
            "rating": 3.0,
            "imageUrl": "/images/negative.jpg",
            "category": "test"
        }
        
        # Pydantic doesn't validate negative prices by default
        item = ContentItem(**content_data)
        self.assertEqual(item.price, -1000)
    
    def test_content_item_rating_bounds(self):
        """Test ContentItem rating with various values"""
        # Test with valid rating
        content_data = {
            "id": "item-005",
            "title": "高評価商品",
            "price": 2000,
            "rating": 5.0,
            "imageUrl": "/images/high-rating.jpg",
            "category": "premium"
        }
        
        item = ContentItem(**content_data)
        self.assertEqual(item.rating, 5.0)
        
        # Test with zero rating
        content_data["rating"] = 0.0
        item = ContentItem(**content_data)
        self.assertEqual(item.rating, 0.0)
    
    def test_content_item_missing_required_fields(self):
        """Test ContentItem validation with missing required fields"""
        incomplete_data = {
            "id": "item-006",
            "title": "不完全商品"
            # Missing price, rating, imageUrl, category
        }
        
        with self.assertRaises(ValidationError):
            ContentItem(**incomplete_data)
    
    def test_content_item_wrong_type_fields(self):
        """Test ContentItem validation with wrong field types"""
        wrong_type_data = {
            "id": "item-007",
            "title": "型違い商品",
            "price": "not-a-number",  # Should be int
            "rating": 4.0,
            "imageUrl": "/images/wrong-type.jpg",
            "category": "test"
        }
        
        with self.assertRaises(ValidationError):
            ContentItem(**wrong_type_data)
    
    def test_content_item_json_serialization(self):
        """Test ContentItem JSON serialization"""
        content_data = {
            "id": "item-008",
            "title": "JSON商品",
            "price": 3000,
            "originalPrice": 3500,
            "rating": 4.5,
            "imageUrl": "/images/json-item.jpg",
            "category": "serialization",
            "isNew": True,
            "isSale": False,
            "isRecommended": True
        }
        
        item = ContentItem(**content_data)
        json_output = item.model_dump()
        
        self.assertEqual(json_output, content_data)
    
    def test_content_item_json_serialization_with_defaults(self):
        """Test ContentItem JSON serialization includes default values"""
        minimal_data = {
            "id": "item-009",
            "title": "デフォルト商品",
            "price": 1500,
            "rating": 3.8,
            "imageUrl": "/images/default.jpg",
            "category": "default"
        }
        
        item = ContentItem(**minimal_data)
        json_output = item.model_dump()
        
        # Check that default values are included in output
        self.assertIsNone(json_output["originalPrice"])
        self.assertFalse(json_output["isNew"])
        self.assertFalse(json_output["isSale"])
        self.assertFalse(json_output["isRecommended"])


if __name__ == '__main__':
    unittest.main()