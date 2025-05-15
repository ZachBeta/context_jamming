# Benchmark Improvement Roadmap

This document outlines our path to achieve perfect recall on the MUD CLI simple scenario and beyond.

**Important Note**
- `window_size` refers to the number of (user,assistant) turn **pairs** retained. With `window_size=3`, up to 3 user messages + 3 GM replies (6 total messages) are included.

## Phase 1: Sliding-Window Sweep

1. Sweep `window_size` from 1 to N (e.g. 10) on the 3-step scenario.
2. Stop at the first size achieving 3/3 PASS.
3. Record minimal window for perfect recall.

## Phase 2: Rolling-Summary Memory (v1)

1. Implement `RollingSummaryMemory` in `memory.py` to compress evicted turns into a short recap.
2. Swap in the new memory store in `head_to_head.py`.
3. Benchmark with same scenario and compare recall/latency to v0.

## Phase 3: Vector-Retrieval Memory (v2)

1. Integrate embeddings (e.g. OpenAI embeddings API).
2. Store embedding per turn and retrieve top-K relevant memories each step.
3. Benchmark for K = [1,2,3], measure recall vs. overhead.

## Phase 4: Prompt Engineering

- Add explicit directives: e.g., “Always mention when the player still holds an item.”
- Prepend a concise memory recap before each user input.
- Evaluate gains when combined with other strategies.

## Phase 5: Hybrid Pruning (v3)

- Combine raw sliding window (last M pairs) with a rolling summary of older turns.
- Sweep M to find optimal trade-off of context length vs. recall.

## Phase 6: Scenario Expansion

- Handcraft or auto-generate longer scenarios (Fibonacci lengths: 3,5,8,13…).
- Include multiple pick-up and recall checkpoints.
- Run head-to-head across all scenarios.

## Analysis & Visualization

- Write a script or notebook to parse `logs/*.json` and plot:
  - Recall vs. window size  
  - Latency per turn  
  - Cost/token usage per call
- Summarize findings in `REPORT.md` or a Jupyter notebook.

---

**Next Steps**
Choose the phase you’d like to tackle:
- Sliding-window sweep  
- Rolling-summary implementation  
- Vector-retrieval prototype  
- Prompt-engineering experiments  
- Hybrid pruning  
- Scenario expansion & analysis
