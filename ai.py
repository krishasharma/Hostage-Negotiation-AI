#""" 
# Old code but just in case, wanted to keep it
# AI model handling (loading, response generation)
from transformers import TFAutoModelForCausalLM, AutoTokenizer

class AIModel:
    def __init__(self):
        # Load the tokenizer and the model using TensorFlow
        self.tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-j-6B')
        self.model = TFAutoModelForCausalLM.from_pretrained('EleutherAI/gpt-j-6B')

    def generate_response(self, prompt):
        # Tokenize the input prompt
        inputs = self.tokenizer(prompt, return_tensors="tf")
        # Generate the response
        outputs = self.model.generate(inputs['input_ids'], max_length=150)
        # Decode the output into text
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
#"""
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re

# Load the pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

def clean_response(text):
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove any non-alphanumeric characters at the start of the text
    text = re.sub(r'^[^a-zA-Z0-9]+', '', text)
    
    # Capitalize the first letter
    text = text.capitalize()
    
    return text

def generate_hostage_taker_response(player_input):
    prompt = f"Negotiator: {player_input}\nHostage-taker:"

    # Tokenize the input prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    
    # Generate the response
    output = model.generate(
        input_ids,
        max_length=input_ids.shape[1] + 50,
        num_return_sequences=1,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    # Decode the output into text
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Extract only the hostage-taker's response
    hostage_taker_response = response.split("Hostage-taker:")[-1].strip()
    
    # Clean up the response
    cleaned_response = clean_response(hostage_taker_response)
    
    # Ensure the response is not too long (1-3 sentences)
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_response)
    if len(sentences) > 3:
        cleaned_response = ' '.join(sentences[:3])
    
    return cleaned_response
