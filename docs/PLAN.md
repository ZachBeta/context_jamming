# Benchmark Improvement Plan

This plan outlines steps to achieve perfect recall (3/3) on our simple scenario, then extend to 10/10 prompts.

## 1. Objectives

- Increase pass rate from 0.67 to 1.0 on the 3-step scenario.
- Scale memory tests to a 10-step scenario and maintain high recall.
- Compare memory strategies: sliding window, rolling summary, vector retrieval, hybrid.
- Measure trade-offs between accuracy, latency, and cost.

## 2. Metrics & Reporting

- **Recall**: #PASS / #steps.
- **Latency**: wall-time and CPU-time per turn.
- **Cost**: token usage and API cost per call.
- **Break Point**: smallest window where recall ≥ threshold (e.g. 0.8).

Store logs as `logs/{scenario}_{provider}_{timestamp}.json` and errors in `.log` files.

## 3. Phase 1: Sliding Window Sweep

1. Modify `head_to_head.py` to accept `--window-size`.
2. Run benchmarks for sizes: `[2,4,6,8,10]`.
3. Collect recall/latency data per size.
4. Plot recall vs. window-size to identify minimal viable window.

## 4. Phase 2: Rolling-Summary Memory (v1)

1. Implement `RollingSummaryMemory` in `memory.py`:
   - After each turn, compress oldest N turns into a short summary.
2. Swap memory store in head-to-head harness.
3. Benchmark with window_size=4 + summary of evicted turns.
4. Compare recall & latency against pure sliding window.

## 5. Phase 3: Vector-Based Retrieval (v2)

1. Integrate an embedding service (e.g. OpenAI embeddings).
2. On each turn, store embedding of conversation state.
3. Retrieve top-K relevant memories to include in prompt.
4. Benchmark retrieval strategy with k=[1,2,3].
5. Analyze memory overhead vs. recall improvement.

## 6. Phase 4: Prompt Engineering

- Add explicit system prompts to emphasize item retention:
  - "You must remember every object the player picks up."
- Introduce a memory recap snippet before user input.
- Measure gains when combined with other strategies.

## 7. Phase 5: Hybrid Pruning

- Combine sliding window + rolling summary:
  - Keep last M raw turns + summary of older turns.
- Benchmark to find optimal M.

## 8. Scenario Expansion

- Create `tests/scenarios/long.yaml` with 10+ steps and multiple recall checks.
- Include varied contexts: nested items, multiple pickups, dialogue references.
- Run head-to-head across scenarios.

## 9. Analysis & Visualization

- Write a Python script or Jupyter notebook to:
  - Parse all JSON logs.
  - Generate tables and plots: recall vs. window, latency vs. turn, cost vs. strategy.
- Summarize findings in `REPORT.md`.

## 10. Timeline & Next Steps

| Phase                        | ETA       |
| ---------------------------- | --------- |
| Sliding Window Sweep         | Today     |
| Rolling Summary Implementation | +1 day   |
| Vector Retrieval Prototype   | +2 days   |
| Prompt Eng. Experiments      | +3 days   |
| Hybrid Pruning Test          | +4 days   |
| Scenario Expansion & Report  | +5 days   |
