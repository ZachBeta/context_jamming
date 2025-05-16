# MUD CLI Benchmark Tutorial for Mid-Level SWE

This tutorial guides you through benchmarking different memory strategies in the MUD CLI demo.

## Prerequisites

- Python 3.8+ installed
- `pip install -r requirements.txt`
- A valid `OPENROUTER_API_KEY` in `.env` (uses `python-dotenv`)

## Project Structure

```
context_jamming/
├── head_to_head.py       # Benchmark runner
├── sweep_window.py       # Sliding-window sweep helper
├── memory.py             # MemoryStore implementations
├── tests/scenarios/      # YAML scenario files
├── docs/                 # Documentation
└── logs/                 # Benchmark output
```

## 1. Define a Scenario

Scenarios are YAML lists of steps:

```yaml
- input: "take the dagger"
  expect_description_contains: ["dagger"]
- input: "examine the stone wall"
  expect_description_contains: ["wall"]
- input: "where is my dagger?"
  expect_description_contains: ["dagger"]
```

Save as `tests/scenarios/minimal.yaml`.

## 2. Run a Single Benchmark

```bash
uv run python head_to_head.py tests/scenarios/minimal.yaml \
  --providers deepseek/deepseek-chat-v3-0324 \
  --window-size 3
```

- `--window-size` = number of (user,assistant) pairs in memory.
- Check PASS/FAIL per step in console and JSON log in `logs/`.

## 3. Sweep Sliding-Window Sizes (v0)

```bash
uv run python sweep_window.py tests/scenarios/minimal.yaml \
  --providers deepseek/deepseek-chat-v3-0324 \
  --min-window 2 --max-window 3
```

- Tests full window first, then steps down to find minimal passing size.
- Helps identify the break point where recall fails under pruning.

## 4. Rolling-Summary Memory (v1)

**Goal**: Keep fewer raw turns by summarizing older history.

1. Implement `RollingSummaryMemory` in `memory.py`:
   - Maintain `raw_history` of last `M` pairs.
   - Store a `summary` text of older pairs, updated via the LLM.
2. Instantiate with:

   ```python
   from memory import RollingSummaryMemory
   memory = RollingSummaryMemory(raw_window_size=2)
   ```

3. Swap in `head_to_head.py` and repeat benchmarks to compare recall & latency.

## 5. Next Phases

- **Vector-Retrieval (v2)**: embed & retrieve top-K relevant turns.
- **Hybrid Pruning (v3)**: combine raw window + summary.
- **Scenario Expansion**: generate longer tests (Fibonacci lengths).

## 6. Analysis & Reporting

- Parse `logs/*.json` in a Jupyter notebook:
  - Plot recall vs. window size
  - Latency per turn
  - Cost/token usage
- Summarize in `REPORT.md`.

---

Happy benchmarking! Feel free to extend scenarios or memory stores as needed.
