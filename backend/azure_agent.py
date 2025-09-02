from inspect import trace
import os
import json
import re
import logging
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from azure.core.settings import settings

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

from azure.monitor.opentelemetry import configure_azure_monitor
from azure.ai.agents.telemetry import AIAgentsInstrumentor
AIAgentsInstrumentor().instrument()

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Azure AI Project Client lazily
project = None

def get_project_client():
    global project
    if project is None:
        endpoint = os.getenv("PROJECT_ENDPOINT")
        if not endpoint:
            raise ValueError("PROJECT_ENDPOINT environment variable is not set")
        project = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=endpoint)
    return project

def main(query: str = None):
    try:
        project_client = get_project_client()

        connection_string = project_client.telemetry.get_application_insights_connection_string()
        configure_azure_monitor(connection_string=connection_string) #enable telemetry collection

        settings.tracing_implementation = "opentelemetry"

        # Setup tracing to console
        span_exporter = ConsoleSpanExporter()
        tracer_provider = TracerProvider()
        tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
        trace.set_tracer_provider(tracer_provider)
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("example-tracing"):    
            agent = project_client.agents.get_agent(os.getenv("AZURE_AI_AGENT_ID"))
            logger.info(f"Got agent: {agent.id}")

            thread = project_client.agents.threads.create()
            logger.info(f"Created thread, ID: {thread.id}")

            # Use provided query or default query
            user_query = query if query else "真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。"
        
            message = project_client.agents.messages.create(
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
            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id)
        
            logger.info(f"Run completed with status: {run.status}")
        
        if run.status == "failed":
            logger.error(f"Run failed: {run.last_error}, returning fallback data")
            return {
                "id": "fallback-006",
                "title": "プレミアムワイヤレスヘッドホン",
                "price": 15800,
                "originalPrice": 19800,
                "rating": 4.8,
                "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
                "category": "オーディオ",
                "isRecommended": True
            }
        elif run.status == "in_progress":
            logger.warning(f"Run is still in progress (status: {run.status}). This might cause inconsistent results. Returning fallback data.")
            return {
                "id": "fallback-007",
                "title": "プレミアムワイヤレスヘッドホン",
                "price": 15800,
                "originalPrice": 19800,
                "rating": 4.8,
                "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
                "category": "オーディオ",
                "isRecommended": True
            }
        elif run.status == "completed":
            logger.info("Run completed successfully, retrieving messages...")
            messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
            logger.info(f"Retrieved {len(list(messages))} messages")

            messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
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
                                "title": "プレミアムワイヤレスヘッドホン",
                                "price": 15800,
                                "originalPrice": 19800,
                                "rating": 4.8,
                                "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
                                "category": "オーディオ",
                                "isRecommended": True
                            }
                    else:
                        logger.warning("No JSON found in assistant response, returning fallback data")
                        # Return fallback recommendation when JSON parsing fails
                        return {
                            "id": "fallback-001",
                            "title": "プレミアムワイヤレスヘッドホン",
                            "price": 15800,
                            "originalPrice": 19800,
                            "rating": 4.8,
                            "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
                            "category": "オーディオ",
                            "isRecommended": True
                        }
            
            logger.warning("No assistant messages found, returning fallback data")
            return {
                "id": "fallback-003",
                "title": "プレミアムワイヤレスヘッドホン",
                "price": 15800,
                "originalPrice": 19800,
                "rating": 4.8,
                "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
                "category": "オーディオ",
                "isRecommended": True
            }
        else:
            logger.warning(f"Unexpected run status: {run.status}, returning fallback data")
            return {
                "id": "fallback-004",
                "title": "プレミアムワイヤレスヘッドホン",
                "price": 15800,
                "originalPrice": 19800,
                "rating": 4.8,
                "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
                "category": "オーディオ",
                "isRecommended": True
            }
            
    except Exception as e:
        logger.error(f"Error in main function: {e}, returning fallback data")
        return {
            "id": "fallback-005",
            "title": "プレミアムワイヤレスヘッドホン",
            "price": 15800,
            "originalPrice": 19800,
            "rating": 4.8,
            "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
            "category": "オーディオ",
            "isRecommended": True
        }

def get_recommendation(query: str = None):
    return main(query)

if __name__ == "__main__":
    result = get_recommendation()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
