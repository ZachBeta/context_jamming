import os
import sys
import json
import yaml
import time
from agent import DomainAgent
from model_client import OpenRouterClient
from memory import SlidingWindowMemory
from prompts import STATIC_PRIMER


def load_scenario(path):
    with open(path) as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <scenario.yaml>")
        sys.exit(1)
    scen_path = sys.argv[1]

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: please set the OPENROUTER_API_KEY environment variable.")
        sys.exit(1)

    provider = os.getenv("OPENROUTER_PROVIDER", "deepseek/deepseek-chat-v3-0324")
    client = OpenRouterClient(api_key, provider)
    memory = SlidingWindowMemory(window_size=4)
    agent = DomainAgent(client, memory, STATIC_PRIMER, deterministic=True)

    scenario = load_scenario(scen_path)
    print(f"Running benchmark for scenario: {scen_path}\n")
    log_entries = []
    for step in scenario:
        user = step.get('input', '')
        start = time.perf_counter()
        raw = agent.step(user)
        dt = time.perf_counter() - start
        result = True
        for token in step.get('expect_description_contains', []):
            if token.lower() not in raw.lower():
                result = False
        status = 'PASS' if result else 'FAIL'
        print(f"{user:<40} [{status}] ({dt:.2f}s)")
        log_entries.append({
            "input": user,
            "response": raw,
            "status": status,
            "elapsed": dt
        })

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    basename = os.path.splitext(os.path.basename(scen_path))[0]
    log_file = os.path.join(log_dir, f"{basename}_benchmark.json")
    with open(log_file, "w") as f:
        json.dump(log_entries, f, indent=2)
    print(f"\nChat and results logged to: {log_file}")
