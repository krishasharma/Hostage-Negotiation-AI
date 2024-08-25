 # Logic for managing relationship states
 
from transformers import AutoTokenizer, TFAutoModelForTokenClassification
from transformers import pipeline

class RelationshipManager:
    def __init__(self):
        self.states = {
            "trust": 0,
            "fear": 0,
            "hostility": 0
        }

        # Load a pre-trained model for NER
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.model = TFAutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer)

        # Define AI's interests with core keywords
        self.interests = {
            "movies": {
                "keywords": ["movie", "film", "cinema", "hollywood", "netflix"],  # Core keywords
                "positive": 2,  # Trust increases by 2 for positive talk
                "neutral": 1,   # Trust increases by 1 for neutral talk
                "negative": -1  # Trust decreases by 1 for negative talk, hostility increases by 2
            },
            # Add more interests if needed
        }

    def current_state(self):
        if self.states["hostility"] > 5:
            return "hostile"
        elif self.states["trust"] > 5:
            return "friendly"
        else:
            return "neutral"

    def recognize_entities(self, text):
        ner_results = self.ner_pipeline(text)
        recognized_entities = [result['word'].lower() for result in ner_results if result['entity'].startswith('B-')]
        return recognized_entities

    def update(self, player_input, ai_response):
        # Analyze the sentiment of the player's input using TextBlob
        sentiment_analysis = TextBlob(player_input)
        polarity = sentiment_analysis.sentiment.polarity
        
        # Determine sentiment based on polarity
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Recognize named entities in the player's input
        recognized_entities = self.recognize_entities(player_input)

        # Check if the input mentions any of the AI's interests or recognized entities
        for interest, details in self.interests.items():
            for keyword in details["keywords"]:
                # Check for direct keyword match or recognized entities
                if keyword in player_input.lower() or any(keyword in entity for entity in recognized_entities):
                    # Adjust relationship states based on the sentiment and interest
                    if sentiment == 'positive':
                        self.states["trust"] += details["positive"]
                    elif sentiment == 'negative':
                        self.states["trust"] += details["negative"]
                        self.states["hostility"] += 2  # Increase hostility for negative talk
                    else:
                        self.states["trust"] += details["neutral"]
                    break  # Stop after finding the first matching interest

        # General sentiment-based relationship update (if no interest was matched)
        if "calm" in player_input.lower():
            self.states["trust"] += 1
        if "threaten" in player_input.lower():
            self.states["hostility"] += 1

        # Optionally, update based on overall sentiment if no specific interest was triggered
        if sentiment == 'positive':
            self.states["trust"] += 1
        elif sentiment == 'negative':
            self.states["hostility"] += 1
