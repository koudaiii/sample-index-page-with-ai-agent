import os
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
else:
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

    for message in messages:
        if message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")
