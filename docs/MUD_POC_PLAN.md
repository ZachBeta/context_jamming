# MUD CLI PoC Project Plan

## 1. Domain Overview
A CLI-based MUD (interactive fiction) driven by an LLM. The agent narrates scene descriptions and offers numbered choices.

## 2. User Stories

### Player Stories
- Launch the game and see a _world primer_ (lore, map legend).
- Read a _scene description_ and a list of numbered choices.
- Select an option and see the world respond.
- Enjoy a coherent narrative that remembers past actions.

### Developer Stories
- CLI REPL (`main.py`) for rapid iteration.
- Configurable `MemoryStore` (v0–v3).
- Pluggable `ModelClient` (DeepSeek vs Qwen-3).
- Benchmark harness for ELO-style model/memory comparison.

## 3. Project Layout
```
project/
├─ main.py           # game loop (input → agent.step() → output)
├─ agent.py          # DomainAgent: step(), _build_context()
├─ memory.py         # SlidingWindowMemory(N=4)
├─ model_client.py   # OpenRouterClient → deepseek-chat-v3-0324
├─ prompts.py        # templates: primer, history, player turn
├─ requirements.txt  # dependencies
└─ docs/
   └─ MUD_POC_PLAN.md  # this file
```

## 4. Memory Strategy (v0)
- **Sliding-window** of the last **4** turns.
- Context = static primer + last 4 turns + `Player: <input>`.

## 5. Model (v0)
- Provider: **OpenRouter**
- Model: `deepseek/deepseek-chat-v3-0324`
- API key via `OPENROUTER_API_KEY` env var

## 6. Benchmark Harness
- Swap in a second model (e.g. Qwen-3) via `OPENROUTER_PROVIDER` env var.
- Replay fixed scripts; collect pairwise “coherence” votes.
- ELO-style ranking of model+memory combos.

## 7. Roadmap
1. **v0** – CLI + Sliding-window
2. **v1** – Rolling-summary memory
3. **v2** – Vector-backed event memory
4. **v3** – Advanced agent layer (hot/cold cache, map-reduce)
5. **UI & Domain Swap** – Discord/Web UI; swap story → code chunks
