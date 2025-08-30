# pip install azure-ai-projects==1.0.0b10
import json
import os
import re
import sys
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def get_recommendation(query="真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。"):
    """
    Get recommendation from Azure agent based on the provided query.
    
    Args:
        query (str): The query to send to the agent
        
    Returns:
        dict: The first recommendation in JSON format, or None if no recommendation found
    """
    conn_str = os.getenv("AZURE_AI_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("AZURE_AI_CONNECTION_STRING environment variable is required")
        
    # Parse connection string: endpoint;subscription_id;key;project_name
    parts = conn_str.split(';')
    if len(parts) != 4:
        raise ValueError(f"Expected 4 parts in connection string, got {len(parts)}")
    
    endpoint, subscription_id, key, project_name = parts
    print(f"Using key authentication for Azure AI Projects")
    
    # Use connection string with DefaultAzureCredential
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=conn_str,
        credential=credential)

    agent_id = os.getenv("AZURE_AI_AGENT_ID")
    if not agent_id:
        raise ValueError("AZURE_AI_AGENT_ID environment variable is required")
    agent = project_client.agents.get_agent(agent_id)

    thread = project_client.agents.create_thread()

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=f'''{query}返答は、  content.json の在庫から一件の JSON で出力してください。
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

    run = project_client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=agent.id)
    messages = project_client.agents.list_messages(thread_id=thread.id)

    # Variable to store the first recommendation
    recommendation = None

    for text_message in messages.text_messages:
        message_dict = text_message.as_dict()
        print("Full response:")
        print(message_dict)
        print("\n" + "="*50 + "\n")
        
        # Extract JSON from the text content
        if 'text' in message_dict and 'value' in message_dict['text']:
            text_content = message_dict['text']['value']
            json_data = extract_json_from_response(text_content)
            
            if json_data:
                print("Extracted JSON:")
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
                
                # Store the first recommendation if not already stored
                if recommendation is None:
                    recommendation = json_data
            else:
                print("No JSON found in response")
        
        print("\n" + "="*50 + "\n")

    # Display the stored recommendation
    if recommendation:
        print("First recommendation stored in 'recommendation' variable:")
        print(json.dumps(recommendation, indent=2, ensure_ascii=False))
    else:
        print("No recommendation was captured")
    
    return recommendation

def extract_json_from_response(text_content):
    """Extract JSON content from the agent response text."""
    # Look for JSON content between ```json and ``` markers
    json_pattern = r'```json\s*(.*?)\s*```'
    match = re.search(json_pattern, text_content, re.DOTALL)
    
    if match:
        json_str = match.group(1).strip()
        try:
            # Parse the JSON string to validate it
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        # If no markdown JSON block found, try to find JSON-like content
        # Look for content that starts with [ or { 
        json_pattern_alt = r'(\[.*?\]|\{.*?\})'
        match = re.search(json_pattern_alt, text_content, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            try:
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError:
                pass
    
    return None

# Main execution
if __name__ == "__main__":
    # Check if query is provided as command line argument
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "真夏になったので、今あるおすすめの水筒を値段等含めて教えてください。"
    
    # Get recommendation using the provided or default query
    recommendation = get_recommendation(query)
