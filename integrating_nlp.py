import os
from transformers import pipeline

# Set Hugging Face cache directory to D drive (if needed)
# os.environ['HF_HOME'] = 'D:/huggingface_cache'

# Initialize the generator with GPT-Neo 1.3B model
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")


def predict_next_words(prompt, num_predictions=10):
    # Generate text with the model
    result = generator(
        prompt,
        max_new_tokens=1,  # Limit to generating only one token (word)
        num_return_sequences=num_predictions,  # Number of predictions
        return_full_text=False,  # Do not return the full input text
        temperature=0.7,  # Adjust temperature for less randomness
        top_k=100,  # Use top-k sampling to focus on top 100 probable words
        top_p=1,  # Nucleus sampling to focus on top cumulative probability
        do_sample=True,  # Enable sampling
    )

    # Extract the next words
    next_words = [
        sequence["generated_text"].strip().split()[0]
        for sequence in result
        if len(sequence["generated_text"].strip().split()[0]) != 1
    ]

    # Remove duplicates by converting to a set, then back to a list
    unique_next_words = list(set(next_words))

    return unique_next_words


# Example usage
prompt = "what is"
predicted_words = predict_next_words(prompt, num_predictions=100)

print(predicted_words)
