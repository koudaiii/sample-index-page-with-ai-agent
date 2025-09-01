import os
import json
import re
import logging
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Azure AI Project Client
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("PROJECT_ENDPOINT"))

def main(query: str = None):
    try:
        agent = project.agents.get_agent(os.getenv("AZURE_AI_AGENT_ID"))
        logger.info(f"Got agent: {agent.id}")

        thread = project.agents.threads.create()
        logger.info(f"Created thread, ID: {thread.id}")

        # Use provided query or default query
        user_query = query if query else "真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。"
        
        message = project.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=f'''{user_query}返答は、 content.json から次のようなフォーマットで一件 JSON 形式で出力してください。
                {{
                "id": "",
                "title": "",
                "price": 0,
                "rating": 0,
                "imageUrl": "",
                "category": "",
                "isRecommended": false
              }}'''
        )
        logger.info(f"Created message, ID: {message.id}")

        logger.info("Starting run creation and processing...")
        run = project.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id)
        
        logger.info(f"Run completed with status: {run.status}")
        
        if run.status == "failed":
            logger.error(f"Run failed: {run.last_error}, returning fallback data")
            return {
                "id": "fallback-006",
                "title": "おすすめ商品（実行失敗）",
                "price": 0,
                "rating": 0,
                "imageUrl": "/placeholder-image.jpg",
                "category": "general",
                "isRecommended": True
            }
        elif run.status == "in_progress":
            logger.warning(f"Run is still in progress (status: {run.status}). This might cause inconsistent results. Returning fallback data.")
            return {
                "id": "fallback-007",
                "title": "おすすめ商品（処理中）",
                "price": 0,
                "rating": 0,
                "imageUrl": "/placeholder-image.jpg",
                "category": "general",
                "isRecommended": True
            }
        elif run.status == "completed":
            logger.info("Run completed successfully, retrieving messages...")
            messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
            logger.info(f"Retrieved {len(list(messages))} messages")

            messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
            for message in messages:
                logger.info(f"Processing message with role: {message.role}")
                if message.role == "assistant" and message.text_messages:
                    text_content = message.text_messages[-1].text.value
                    logger.info(f"Assistant response: {text_content[:200]}...")
                    # Extract JSON from the response text
                    json_match = re.search(r'\{[\s\S]*\}', text_content)
                    if json_match:
                        try:
                            json_str = json_match.group(0)
                            result = json.loads(json_str)
                            logger.info(f"Successfully parsed JSON recommendation: {result}")
                            return result
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON: {e}, returning fallback data")
                            # Return fallback recommendation when JSON parsing fails
                            return {
                                "id": "fallback-002",
                                "title": "おすすめ商品（解析エラー）",
                                "price": 0,
                                "rating": 0,
                                "imageUrl": "/placeholder-image.jpg",
                                "category": "general",
                                "isRecommended": True
                            }
                    else:
                        logger.warning("No JSON found in assistant response, returning fallback data")
                        # Return fallback recommendation when JSON parsing fails
                        return {
                            "id": "fallback-001",
                            "title": "おすすめ商品（一時的に利用できません）",
                            "price": 0,
                            "rating": 0,
                            "imageUrl": "/placeholder-image.jpg",
                            "category": "general",
                            "isRecommended": True
                        }
            
            logger.warning("No assistant messages found, returning fallback data")
            return {
                "id": "fallback-003",
                "title": "おすすめ商品（メッセージなし）",
                "price": 0,
                "rating": 0,
                "imageUrl": "/placeholder-image.jpg",
                "category": "general",
                "isRecommended": True
            }
        else:
            logger.warning(f"Unexpected run status: {run.status}, returning fallback data")
            return {
                "id": "fallback-004",
                "title": "おすすめ商品（ステータスエラー）",
                "price": 0,
                "rating": 0,
                "imageUrl": "/placeholder-image.jpg",
                "category": "general",
                "isRecommended": True
            }
            
    except Exception as e:
        logger.error(f"Error in main function: {e}, returning fallback data")
        return {
            "id": "fallback-005",
            "title": "おすすめ商品（システムエラー）",
            "price": 0,
            "rating": 0,
            "imageUrl": "/placeholder-image.jpg",
            "category": "general",
            "isRecommended": True
        }

def get_recommendation(query: str = None):
    return main(query)

if __name__ == "__main__":
    result = get_recommendation()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
