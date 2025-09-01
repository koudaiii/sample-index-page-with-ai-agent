import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import pytest
from azure_agent_sample import get_recommendation, main


class TestAzureAgentSample(unittest.TestCase):
    
    @patch('azure_agent_sample.get_project_client')
    def test_successful_recommendation_parsing(self, mock_get_project_client):
        """Test successful JSON parsing from assistant response"""
        # Mock the Azure AI project client response
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_agent.id = "test-agent-id"
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_message.id = "test-message-id"
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "completed"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        # Create mock message with valid JSON response
        mock_assistant_message = Mock()
        mock_assistant_message.role = "assistant"
        mock_text_message = Mock()
        mock_text_message.text.value = '''ここにおすすめの水筒をご紹介します。
        {
            "id": "bottle-001",
            "title": "保温水筒 500ml",
            "price": 2980,
            "rating": 4.5,
            "imageUrl": "/images/bottle.jpg",
            "category": "drinkware",
            "isRecommended": true
        }
        以上がおすすめの水筒です。'''
        mock_assistant_message.text_messages = [mock_text_message]
        
        mock_project.agents.messages.list.return_value = [mock_assistant_message]
        
        result = get_recommendation()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "bottle-001")
        self.assertEqual(result["title"], "保温水筒 500ml")
        self.assertEqual(result["price"], 2980)
        self.assertEqual(result["rating"], 4.5)
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_no_json_found_fallback(self, mock_get_project_client):
        """Test fallback response when no JSON is found in assistant response"""
        # Mock setup
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_agent.id = "test-agent-id"
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "completed"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        # Assistant message without JSON
        mock_assistant_message = Mock()
        mock_assistant_message.role = "assistant"
        mock_text_message = Mock()
        mock_text_message.text.value = "申し訳ございませんが、データを取得できませんでした。"
        mock_assistant_message.text_messages = [mock_text_message]
        
        mock_project.agents.messages.list.return_value = [mock_assistant_message]
        
        result = get_recommendation()
        
        # Should return fallback data
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-001")
        self.assertEqual(result["title"], "おすすめ商品（一時的に利用できません）")
        self.assertEqual(result["price"], 0)
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_invalid_json_parsing_fallback(self, mock_get_project_client):
        """Test fallback response when JSON parsing fails"""
        # Mock setup
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "completed"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        # Assistant message with malformed JSON
        mock_assistant_message = Mock()
        mock_assistant_message.role = "assistant"
        mock_text_message = Mock()
        mock_text_message.text.value = '''おすすめの水筒です。
        {
            "id": "bottle-001",
            "title": "保温水筒",
            "price": 2980,
            // invalid comment in JSON
            "rating": 4.5
        }'''
        mock_assistant_message.text_messages = [mock_text_message]
        
        mock_project.agents.messages.list.return_value = [mock_assistant_message]
        
        result = get_recommendation()
        
        # Should return fallback data for JSON parsing error
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-002")
        self.assertEqual(result["title"], "おすすめ商品（解析エラー）")
        self.assertEqual(result["price"], 0)
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_run_failed_fallback(self, mock_get_project_client):
        """Test fallback response when Azure AI run fails"""
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "failed"
        mock_run.last_error = "API quota exceeded"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        result = get_recommendation()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-006")
        self.assertEqual(result["title"], "おすすめ商品（実行失敗）")
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_run_in_progress_fallback(self, mock_get_project_client):
        """Test fallback response when Azure AI run is still in progress"""
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "in_progress"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        result = get_recommendation()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-007")
        self.assertEqual(result["title"], "おすすめ商品（処理中）")
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_no_assistant_messages_fallback(self, mock_get_project_client):
        """Test fallback response when no assistant messages found"""
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "completed"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        # No assistant messages
        mock_project.agents.messages.list.return_value = []
        
        result = get_recommendation()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-003")
        self.assertEqual(result["title"], "おすすめ商品（メッセージなし）")
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_unexpected_status_fallback(self, mock_get_project_client):
        """Test fallback response for unexpected run status"""
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        
        mock_agent = Mock()
        mock_project.agents.get_agent.return_value = mock_agent
        
        mock_thread = Mock()
        mock_project.agents.threads.create.return_value = mock_thread
        
        mock_message = Mock()
        mock_project.agents.messages.create.return_value = mock_message
        
        mock_run = Mock()
        mock_run.status = "unknown_status"
        mock_project.agents.runs.create_and_process.return_value = mock_run
        
        result = get_recommendation()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-004")
        self.assertEqual(result["title"], "おすすめ商品（ステータスエラー）")
        self.assertTrue(result["isRecommended"])
    
    @patch('azure_agent_sample.get_project_client')
    def test_exception_handling_fallback(self, mock_get_project_client):
        """Test fallback response when an exception occurs"""
        # Mock to raise an exception
        mock_project = Mock()
        mock_get_project_client.return_value = mock_project
        mock_project.agents.get_agent.side_effect = Exception("Network error")
        
        result = get_recommendation()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "fallback-005")
        self.assertEqual(result["title"], "おすすめ商品（システムエラー）")
        self.assertTrue(result["isRecommended"])
    
    def test_fallback_response_structure(self):
        """Test that all fallback responses have the correct structure"""
        fallback_ids = ["fallback-001", "fallback-002", "fallback-003", 
                       "fallback-004", "fallback-005", "fallback-006", "fallback-007"]
        
        for fallback_id in fallback_ids:
            with patch('azure_agent_sample.get_project_client') as mock_get_project_client:
                mock_project = Mock()
                mock_get_project_client.return_value = mock_project
                # Setup to trigger specific fallback
                if fallback_id == "fallback-005":
                    mock_project.agents.get_agent.side_effect = Exception("Test error")
                else:
                    mock_agent = Mock()
                    mock_project.agents.get_agent.return_value = mock_agent
                    mock_thread = Mock()
                    mock_project.agents.threads.create.return_value = mock_thread
                    mock_message = Mock()
                    mock_project.agents.messages.create.return_value = mock_message
                    mock_run = Mock()
                    
                    if fallback_id == "fallback-006":
                        mock_run.status = "failed"
                        mock_run.last_error = "Test error"
                    elif fallback_id == "fallback-007":
                        mock_run.status = "in_progress"
                    elif fallback_id == "fallback-004":
                        mock_run.status = "unknown"
                    else:
                        mock_run.status = "completed"
                        if fallback_id == "fallback-003":
                            mock_project.agents.messages.list.return_value = []
                        else:
                            mock_assistant_message = Mock()
                            mock_assistant_message.role = "assistant"
                            mock_text_message = Mock()
                            if fallback_id == "fallback-001":
                                mock_text_message.text.value = "No JSON here"
                            elif fallback_id == "fallback-002":
                                mock_text_message.text.value = '{"invalid": json}'
                            mock_assistant_message.text_messages = [mock_text_message]
                            mock_project.agents.messages.list.return_value = [mock_assistant_message]
                    
                    mock_project.agents.runs.create_and_process.return_value = mock_run
                
                result = get_recommendation()
                
                # Validate structure
                self.assertIsInstance(result, dict)
                self.assertIn("id", result)
                self.assertIn("title", result)
                self.assertIn("price", result)
                self.assertIn("rating", result)
                self.assertIn("imageUrl", result)
                self.assertIn("category", result)
                self.assertIn("isRecommended", result)
                
                self.assertEqual(result["price"], 0)
                self.assertEqual(result["rating"], 0)
                self.assertTrue(result["isRecommended"])


if __name__ == '__main__':
    unittest.main()