from typing import List, Dict
from model_client import OpenRouterClient
from memory import SlidingWindowMemory

class DomainAgent:
    """
    Orchestrates the game loop: builds context, calls the LLM, and updates memory.
    """
    def __init__(self, model_client: OpenRouterClient, memory_store: SlidingWindowMemory, static_primer: str):
        self.model_client = model_client
        self.memory = memory_store
        self.static_primer = static_primer

    def step(self, user_input: str) -> str:
        # 1. Build the prompt messages
        messages: List[Dict[str, str]] = []
        messages.append({"role": "system", "content": self.static_primer})
        messages.extend(self.memory.get_messages())
        messages.append({"role": "user", "content": f"Player: {user_input}"})

        # 2. Call the LLM
        response = self.model_client.generate(messages)

        # 3. Record turn in memory and return
        self.memory.add_turn(user_input, response)
        return response
