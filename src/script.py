import requests
import os
# set environment variables before importing any other code (in particular the openai module)
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

url = "https://ai-gmonneai947472757823.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2024-02-15-preview"
payload = '{"model": "text-embedding-ada-002", "input": "Hello, world!"}'
headers = {
    'api-key': f'{os.getenv("OPENAI_API_KEY")}',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(f"API endpoint - {url}")
#print(f"API key - {os.getenv("OPENAI_API_KEY")}")
print(response.text)
