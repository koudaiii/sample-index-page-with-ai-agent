import os
import json
import re
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Azure AI Project Client
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("PROJECT_ENDPOINT"))

def main():
    agent = project.agents.get_agent(os.getenv("AZURE_AI_AGENT_ID"))

    thread = project.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    message = project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=f'''真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。返答は、 content.json の在庫から一件の JSON で出力してください。
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

    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        return None
    else:
        messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

        for message in messages:
            if message.role == "assistant" and message.text_messages:
                text_content = message.text_messages[-1].text.value
                # Extract JSON from the response text
                json_match = re.search(r'\{[\s\S]*\}', text_content)
                if json_match:
                    try:
                        json_str = json_match.group(0)
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        return None
                return None
        
        return None

def get_recommendation():
    return main()

if __name__ == "__main__":
    result = get_recommendation()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
