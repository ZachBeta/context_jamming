# MUD Benchmarking & Deterministic Test Plan

## 1. Deterministic Agent Mode
- Introduce a flag (`MUD_DETERMINISTIC=true` env or CLI arg `--deterministic`).
- When enabled, call `model_client.generate(..., temperature=0, top_p=1.0)` for repeatable outputs.
- Allow seeding local HF backends (e.g. `torch.manual_seed(seed)`) in future phases.

## 2. Structured JSON Output
- Update system prompt to enforce strict JSON schema:
  ```json
  {
    "description": "<scene text>",
    "choices": ["<opt1>", "<opt2>", ...]
  }
  ```
- Parse the LLM’s reply as JSON to eliminate formatting variation.

## 3. ModelClient Enhancements
- Add `temperature` and `top_p` parameters to `OpenRouterClient.generate()` signature.
- Respect the deterministic flag in `DomainAgent` to override defaults.

## 4. DomainAgent Enhancements
- Add `deterministic: bool` attribute.
- In `_build_context()`, include the JSON-output instructions in the system message.
- Pass `deterministic` settings down to `model_client.generate()`.

## 5. Scenario Definitions
- Place test scenarios in `tests/scenarios/` as YAML or JSON:
  ```yaml
  - input: "take the dagger"
    expect_description_contains: ["dagger"]
    expect_choices: ["Use the dagger", "Drop the dagger"]
  - input: "where is my dagger?"
    expect_description_contains: ["you have the dagger"]
  # … up to N turns
  ```

## 6. Benchmark Harness
- Create `benchmark.py` or use `pytest`:
  1. Load scenario file
  2. Instantiate `DomainAgent(deterministic=True)`
  3. Loop through steps: call `agent.step(input)`
  4. Parse JSON reply: extract `description` and `choices`
  5. Assert expectations and log pass/fail
- Measure latency per turn with `time.perf_counter()`.

## 7. Metrics & Reporting
- **Recall Rate**: `#passes / #checks` per scenario & turn-index.
- **Latency**: mean & p95 per model/memory axis.
- Output results as CSV/Markdown; generate recall-vs-turn plots.

## 8. Head-to-Head ELO Ranking (Optional)
- For each turn in scenario, run two agent configs (e.g. v0 vs v1).
- Use a judge LLM or a simple heuristic to choose which JSON reply is more coherent.
- Update ELO scores for each config pairing.

## 9. Next Steps
1. Implement deterministic & JSON support in `model_client.py` and `DomainAgent`.
2. Define sample scenarios in `tests/scenarios/`.
3. Scaffold `benchmark.py` runner.
4. Run v0 sliding-window benchmarks.
5. Iterate to v1 (rolling-summary) and re-run.
