# Core game logic, input handling, state management
import requests
from relationships import RelationshipManager
import random

class ScenarioGenerator:
    def __init__(self):
        self.location = ["bank", "school", "office building", "apartment complex", "mall"]
        self.motives = ["financail desperation", "political statement", "revenge", "mental health"]
        self.hostage_type = ["employees", "customers", "students", "random civilians"]
        self.demands = ["money", "safe passage out of the country", "public statement from authorities", "specific item or information"]

    def generate_scenario(self):
        location = random.choice(self.location)
        motive = random.choice(self.motives)
        hostages = random.choice(self.hostage_type)
        demand = random.choice(self.demands)
        num_hostages = random.randint(1, 20)
    
        scenario = f"""
        Scenario: A hostage situation has developed at a {location}.
        The hostage-taker appears to be motivated by {motive}.
        They are holding {num_hostages} {hostages} captive.
        Their primary demand is {demand}.
        Your job is to negotiate with the hostage-taker and resolve the situation peacefully.
        """
        return scenario

class Game:
    def __init__(self):
        self.relationship = RelationshipManager()
        self.scenario_generator = ScenarioGenerator()
        self.current_scenario = None

    def get_ai_response(self, player_input):
        url = 'http://localhost:5000/generate'
        data = {
            'input': player_input,
            'relationship_state': self.relationship.current_state()
        }
        response = requests.post(url, json=data)
        return response.json()['response']

    def start_new_scenario(self):
        self.current_scenario = self.scenario_generator.generate_scenario()
        print(self.current_scenario)

    def run(self):
        print("Welcome to Hostage Negotiator!")
        while True:
            self.start_new_scenario()
            print("Type 'exit' to end the game or 'new' to start a new scenario.")
            while True:
                player_input = input("You: ")
                if player_input.lower() == 'exit':
                    print("Thanks for playing!")
                    return
                elif player_input.lower() == 'new':
                    break
                ai_response = self.get_ai_response(player_input)
                print(f"AI: {ai_response}")
                self.relationship.update(player_input, ai_response)
            
            
if __name__ == "__main__":
    game = Game()
    game.run()
