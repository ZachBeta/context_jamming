## Benchmarking

Run a head-to-head benchmark between models:
```bash
uv run python head_to_head.py tests/scenarios \
  --providers deepseek/deepseek-r1,deepseek/deepseek-chat-v3-0324 \
  --workers 2