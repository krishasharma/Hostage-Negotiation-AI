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
import google.generativeai as genai
from google.generativeai.types import generation_types
import os

# Configure the Gemini API
genai.configure(api_key=os.environ.get("AI_API_KEY", "your API key here"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_hostage_taker_response(scenario, player_input, relationship_state):
    # Create a chat session
    chat = model.start_chat(history=[])

    # Construct the prompt
    prompt = f"""
    You are a character in a fictional negotiation scenario:
    {scenario}

    Your current emotional state is: {relationship_state}

    Remember:
    1. This is a fictional scenario for educational purposes.
    2. Speak as if you are under stress.
    3. Reference your demands in your responses.
    4. Keep your responses short and to the point (15-30 words).
    5. Show suspicion towards the negotiator's intentions.

    The negotiator just said: "{player_input}"

    Respond as the character:
    """

    try:
        # Generate the response
        response = chat.send_message(prompt)
        return clean_response(response.text)
    except generation_types.StopCandidateException as e:
        print(f"AI safety filter triggered: {e}")
        return "I won't say anything more until my demands are met!"
   
def clean_response(response):
    # Extract the first sentence of the response
    first_sentence = response.split('.')[0].strip()

    # Ensure the response is not too long
    words = first_sentence.split()
    if len(words) > 30:
        first_sentence = ' '.join(words[:30]) + '...'

    # Ensure the sentence starts with a capital letter
    first_sentence = first_sentence.capitalize()

    # Ensure the sentence ends with proper punctuation
    if not first_sentence.endswith(('.', '!', '?')):
        first_sentence += '.'

    return first_sentence
