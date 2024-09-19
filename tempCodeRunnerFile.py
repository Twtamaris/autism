import requests
import time

# Define API URL for a smaller model
api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"

# Set your Hugging Face API token
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 503:
        # If the model is loading, wait and retry
        loading_info = response.json()
        wait_time = loading_info.get('estimated_time', 30)  # Default to 30 seconds if no time provided
        print(f"Model is loading. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        response = requests.post(api_url, headers=headers, json=payload)  # Retry after waiting
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API returned {response.status_code}: {response.text}"}

# Input text prompt
data = query({"inputs": "I am a man and you"})

print(data)
