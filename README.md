## Benchmarking

Run a head-to-head benchmark between models:
```bash
uv run python head_to_head.py tests/scenarios \
  --providers deepseek/deepseek-r1,deepseek/deepseek-chat-v3-0324 \
  --workers 2
```

Confirming the sliding window size for perfect recall with naive chat history memory:
```
context_jamming % uv run python sweep_window.py tests/scenarios/minimal.yaml \
  --providers deepseek/deepseek-chat-v3-0324 \
  --min-window 2 --max-window 3
Sweeping window sizes for scenario tests/scenarios/minimal.yaml

### Sweeping deepseek/deepseek-chat-v3-0324 ###
Testing deepseek/deepseek-chat-v3-0324 with full window_size=3
[DEBUG] OPENROUTER_API_KEY loaded length: 73
[deepseek/deepseek-chat-v3-0324] Starting job: scenario=minimal, window_size=3
[deepseek/deepseek-chat-v3-0324] Step 1/3 input: 'take the dagger'
[deepseek/deepseek-chat-v3-0324] Step 1 done: status=PASS, wall=5.25s, cpu=0.01s
[deepseek/deepseek-chat-v3-0324] Step 2/3 input: 'look at the stone wall'
[deepseek/deepseek-chat-v3-0324] Step 2 done: status=PASS, wall=14.90s, cpu=0.02s
[deepseek/deepseek-chat-v3-0324] Step 3/3 input: 'where is my dagger?'
[deepseek/deepseek-chat-v3-0324] Step 3 done: status=PASS, wall=5.13s, cpu=0.01s
[deepseek/deepseek-chat-v3-0324] Job done: total_wall=25.28s, total_cpu=0.04s
Testing deepseek/deepseek-chat-v3-0324 with window_size=3
[DEBUG] OPENROUTER_API_KEY loaded length: 73
[deepseek/deepseek-chat-v3-0324] Starting job: scenario=minimal, window_size=3
[deepseek/deepseek-chat-v3-0324] Step 1/3 input: 'take the dagger'
[deepseek/deepseek-chat-v3-0324] Step 1 done: status=PASS, wall=2.99s, cpu=0.01s
[deepseek/deepseek-chat-v3-0324] Step 2/3 input: 'look at the stone wall'
[deepseek/deepseek-chat-v3-0324] Step 2 done: status=PASS, wall=13.67s, cpu=0.02s
[deepseek/deepseek-chat-v3-0324] Step 3/3 input: 'where is my dagger?'
[deepseek/deepseek-chat-v3-0324] Step 3 done: status=PASS, wall=25.83s, cpu=0.03s
[deepseek/deepseek-chat-v3-0324] Job done: total_wall=42.50s, total_cpu=0.07s
Result: recall=1.00
Testing deepseek/deepseek-chat-v3-0324 with window_size=2
[DEBUG] OPENROUTER_API_KEY loaded length: 73
[deepseek/deepseek-chat-v3-0324] Starting job: scenario=minimal, window_size=2
[deepseek/deepseek-chat-v3-0324] Step 1/3 input: 'take the dagger'
[deepseek/deepseek-chat-v3-0324] Step 1 done: status=PASS, wall=4.81s, cpu=0.01s
[deepseek/deepseek-chat-v3-0324] Step 2/3 input: 'look at the stone wall'
[deepseek/deepseek-chat-v3-0324] Step 2 done: status=PASS, wall=11.40s, cpu=0.02s
[deepseek/deepseek-chat-v3-0324] Step 3/3 input: 'where is my dagger?'
[deepseek/deepseek-chat-v3-0324] Step 3 done: status=PASS, wall=6.62s, cpu=0.01s
[deepseek/deepseek-chat-v3-0324] Job done: total_wall=22.83s, total_cpu=0.04s
Result: recall=1.00
✅ deepseek/deepseek-chat-v3-0324 minimal window_size for 100% recall = 2

Sweep Summary:
deepseek/deepseek-chat-v3-0324: minimal window_size = 2
```