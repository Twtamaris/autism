import requests

# Your Hugging Face API token
api_token = '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'  # Replace with your actual Hugging Face token

# Model and endpoint configuration
model_name = "meta-llama/Llama-2-7b-hf"  # Update this to your model of choice
url = f"https://api-inference.huggingface.co/models/{model_name}"

headers = {
    "Authorization": f"Bearer {api_token}"
}

def predict_next_words(sentence, num_words=3):
    # Prepare the payload
    payload = {
        "inputs": sentence,
        "options": {
            "use_cache": False  # Disable caching if needed
        }
    }
    
    # Send request to Hugging Face Inference API
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the generated text from the response
        response_json = response.json()
        generated_text = response_json.get('generated_text', '')
        
        # Extract the next words from the generated text
        next_words = generated_text[len(sentence):].strip().split()[:num_words]
        return next_words
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

# Example usage
current_sentence = "I"
next_words = predict_next_words(current_sentence)
print(f"Next word predictions: {next_words}")
