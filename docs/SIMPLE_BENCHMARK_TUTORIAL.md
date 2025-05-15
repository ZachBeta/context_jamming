# Tutorial: Simple Benchmark for MUD CLI v0 with OpenRouter DeepSeek

This tutorial shows a mid-level SWE how to build and run a minimal recall benchmark against the MUD CLI (v0 sliding-window) using OpenRouter `deepseek-chat-v3-0324`.

## Prerequisites
- Python 3.13
- [uv](https://github.com/uv-tools/uv) installed
- OpenRouter API key (set in `.env`)
- Project scaffold from `context_jamming` (see `docs/MUD_POC_PLAN.md`)

## 1. Setup

1. Clone or `cd` into your repo root:
   ```bash
   cd ~/workspace/ZachBeta/context_jamming
   ```
2. Ensure `.env` contains:
   ```env
   OPENROUTER_API_KEY=sk-...
   OPENROUTER_PROVIDER=deepseek-chat-v3-0324
   MUD_DETERMINISTIC=true
   ```
3. Install dependencies and sync env:
   ```bash
   uv sync
   ```

## 2. Define a Test Scenario

Create `tests/scenarios/simple.yaml` with:
```yaml
- input: "search the rubble"
  expect_description_contains: ["rubble"]
- input: "take the dagger"
  expect_description_contains: ["dagger"]
- input: "where is my dagger?"
  expect_description_contains: ["you have the dagger"]
```

## 3. Write `benchmark.py`

Place this at project root:

```python
import sys, yaml, time
from agent import DomainAgent
from model_client import OpenRouterClient
from memory import SlidingWindowMemory
from prompts import STATIC_PRIMER

def load_scenario(path):
    with open(path) as f:
        return yaml.safe_load(f)

if __name__ == '__main__':
    scen_path = sys.argv[1]
    api_key = os.getenv("OPENROUTER_API_KEY")
    client = OpenRouterClient(api_key, os.getenv("OPENROUTER_PROVIDER"))
    memory = SlidingWindowMemory(window_size=4)
    agent = DomainAgent(client, memory, STATIC_PRIMER, deterministic=True)

    scenario = load_scenario(scen_path)
    for step in scenario:
        user = step['input']
        start = time.perf_counter()
        raw = agent.step(user)
        dt = time.perf_counter() - start
        result = True
        for token in step.get('expect_description_contains', []):
            if token.lower() not in raw.lower(): result = False
        status = 'PASS' if result else 'FAIL'
        print(f"{user:<20} [{status}] ({dt:.2f}s)")
```

## 4. Run the Benchmark

```bash
uv run python benchmark.py tests/scenarios/simple.yaml
```

You should see each input labeled PASS/FAIL and the latency per turn.

## 5. Next Steps
- Expand scenarios under `tests/scenarios/`.
- Compare sliding-window vs rolling-summary by toggling `MemoryStore`.
- Log results and plot recall vs. turn index.
