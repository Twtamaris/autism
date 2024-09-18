from transformers import LlamaTokenizer, LlamaForCausalLM
import sentencepiece
from huggingface_hub import HfApi

# Authenticate with Hugging Face Hub
api = HfApi()
token = 'your_open_api_key'  # Replace with your actual Hugging Face token

# Function to load models with authentication
def load_model_and_tokenizer(model_name, token):
    tokenizer = LlamaTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = LlamaForCausalLM.from_pretrained(model_name, use_auth_token=token)
    return tokenizer, model

# Load the tokenizer and model with token authentication
tokenizer, model = load_model_and_tokenizer("meta-llama/Llama-2-7b-hf", token)

# Function to predict the next words
def predict_next_words(sentence, num_words=3):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=len(inputs["input_ids"][0]) + num_words, num_return_sequences=1)

    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    next_words = predicted_text[len(sentence):].strip().split()[:num_words]

    return next_words

# Example usage
current_sentence = "I"
next_words = predict_next_words(current_sentence)
print(f"Next word predictions: {next_words}")
