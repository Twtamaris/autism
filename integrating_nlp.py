from transformers import pipeline

# Initialize the generator with GPT model
generator = pipeline("text-generation", model="openai-gpt")

# Generate only the next word (max_new_tokens=1) for the input
result = generator(
    "wow",
    max_new_tokens=1,  # Limit to generating only one token (word)
    num_return_sequences=100,  # Get 10 next word predictions
    return_full_text=False,  # Do not return the full input text
    temperature=0.7,  # Adjust temperature for less randomness
    top_k=50,  # Use top-k sampling to focus on top 50 probable words
    top_p=0.9,  # Nucleus sampling to focus on top cumulative probability
)

# Define a list of unwanted tokens like punctuation and connectors
unwanted_tokens = [".", ","]

# Filter out unwanted tokens and extract the next words
next_words = [
    sequence["generated_text"].strip()
    for sequence in result
    if sequence["generated_text"].strip() not in unwanted_tokens
]

# Remove duplicates by converting to a set, then back to a list
unique_next_words = list(set(next_words))

# Print the filtered and unique next words
print(unique_next_words)
