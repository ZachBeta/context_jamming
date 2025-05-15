# MUD CLI Benchmarking Tutorial

This tutorial guides a mid-level SWE through setting up, extending, and running benchmarks on the MUD CLI project using OpenRouter models.

## 1. Prerequisites

- Python 3.11+ (macOS, Linux, or Windows)
- `git`, `pip` or `pipx`
- An [OpenRouter](https://openrouter.ai/) API key

## 2. Clone & Install

```bash
git clone https://github.com/your-org/context_jamming.git
cd context_jamming
python -m venv .venv
source .venv/bin/activate      # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
```  
*Requirements include:* `httpx`, `pyyaml`, `python-dotenv`.

## 3. Configure Environment

Create a `.env` file in the project root:

```ini
OPENROUTER_API_KEY=sk-...
# Optional: set default model
OPENROUTER_PROVIDER=deepseek/deepseek-chat-v3-0324
```  
*Your key* will be picked up by `dotenv` in `main.py` and `head_to_head.py`.

## 4. Project Structure

```text
context_jamming/
├── agent.py           # DomainAgent: builds prompts & tracks memory
├── benchmark.py      # Simple runner: single scenario + provider
├── head_to_head.py   # Parallel runner for multiple models & scenarios
├── memory.py         # MemoryStore implementations (sliding window, future v1/v2)
├── model_client.py   # OpenRouterClient: calls API + error handling
├── prompts.py        # JSON-only primer for deterministic LLM responses
├── tests/scenarios/  # YAML files defining input & expected tokens
└── logs/             # JSON logs & error files after runs
```  

## 5. Run a Single-Model Benchmark

```bash
uv run python benchmark.py tests/scenarios/simple.yaml
```  
Outputs JSON to `logs/simple_<provider>_<timestamp>.json`.

## 6. Head-to-Head Comparison

Compare two or more models in parallel:

```bash
uv run python head_to_head.py tests/scenarios \
  --providers deepseek/deepseek-r1,deepseek/deepseek-chat-v3-0324 \
  --workers 2
```  
- Live per-step profiling (wall & CPU times).  
- Logs in `logs/{scenario}_{provider}_{timestamp}.json`.

## 7. Interpreting Logs

Each entry contains:

```json
{
  "input": "<user input>",
  "response": "<raw LLM output>",
  "status": "PASS"|"FAIL",
  "elapsed": <seconds>
}
```

- **status**: checks `expect_description_contains` tokens.  
- **elapsed**: wall-clock time per call.

## 8. Extending Memory Strategies

1. **SlidingWindowMemory** (v0) – current, keeps last N turns.
2. **RollingSummaryMemory** (v1) – compress old turns into a summary.
3. **VectorMemory** (v2) – store & retrieve with embeddings.

To trial: implement new class in `memory.py`, swap in `head_to_head.py` (pass `--window-size` or add `--memory-class`).

## 9. Creating New Scenarios

Add YAML under `tests/scenarios/your_test.yaml`:

```yaml
- input: "look around"
  expect_description_contains: ["forest", "trees"]
- input: "take torch"
  expect_description_contains: ["torch", "lit"]
```

Then rerun the benchmark commands above.

## 10. Analysis & Next Steps

- Write a Python script or notebook to parse `logs/*.json` and plot:
  - Recall vs. window size
  - Latency per step
  - Cost (token usage) per call
- Prototype phases:
  1. Window-size sweep  
  2. Rolling summary  
  3. Vector retrieval  
  4. Prompt engineering  

See `docs/PLAN.md` for a full roadmap.
