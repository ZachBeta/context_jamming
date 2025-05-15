import os
from dotenv import load_dotenv
load_dotenv()
from model_client import OpenRouterClient
from memory import SlidingWindowMemory
from agent import DomainAgent
from prompts import STATIC_PRIMER

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: please set the OPENROUTER_API_KEY environment variable.")
        return

    model_name = os.getenv("OPENROUTER_PROVIDER", "deepseek/deepseek-chat-v3-0324")
    client = OpenRouterClient(api_key, model_name)
    memory = SlidingWindowMemory(window_size=4)
    agent = DomainAgent(client, memory, STATIC_PRIMER)

    print("Welcome to the MUD! Type 'quit' or 'exit' to leave the game.")
    while True:
        user_input = input("\n> ")
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        response = agent.step(user_input)
        print("\n" + response)


if __name__ == "__main__":
    main()
