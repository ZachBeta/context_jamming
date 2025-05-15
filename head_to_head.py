#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()
import os, sys, argparse, yaml, json, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from agent import DomainAgent
from model_client import OpenRouterClient
from memory import SlidingWindowMemory
from prompts import STATIC_PRIMER
import os.path
import datetime

def run_benchmark(scenario_path: str, provider: str, window_size: int):
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"[DEBUG] OPENROUTER_API_KEY loaded length: {len(api_key) if api_key else 0}", flush=True)
    if not api_key:
        raise RuntimeError("Please set OPENROUTER_API_KEY in your environment.")
    client = OpenRouterClient(api_key, provider)
    memory = SlidingWindowMemory(window_size=window_size)
    agent = DomainAgent(client, memory, STATIC_PRIMER, deterministic=True)
    scenario = yaml.safe_load(open(scenario_path))
    # Timestamp to avoid overwriting logs
    timestamp = datetime.datetime.now().isoformat(timespec='minutes')
    # Profiling: record job start
    base = os.path.splitext(os.path.basename(scenario_path))[0]
    print(f"[{provider}] Starting job: scenario={base}, window_size={window_size}", flush=True)
    total_start = time.perf_counter()
    cpu_start = time.process_time()
    entries = []
    passes = 0
    # Execute each step with per-step profiling and progress logs
    for idx, step in enumerate(scenario, 1):
        user = step.get("input", "")
        print(f"[{provider}] Step {idx}/{len(scenario)} input: '{user}'", flush=True)
        step_cpu_start = time.process_time()
        start = time.perf_counter()
        raw = agent.step(user)
        elapsed = time.perf_counter() - start
        cpu_elapsed = time.process_time() - step_cpu_start
        result = all(token.lower() in raw.lower() for token in step.get("expect_description_contains", []))
        status = "PASS" if result else "FAIL"
        if result:
            passes += 1
        entries.append({"input": user, "response": raw, "status": status, "elapsed": elapsed})
        print(f"[{provider}] Step {idx} done: status={status}, wall={elapsed:.2f}s, cpu={cpu_elapsed:.2f}s", flush=True)
    # Write logs
    os.makedirs("logs", exist_ok=True)
    base = os.path.splitext(os.path.basename(scenario_path))[0]
    prov_name = provider.replace("/", "_")
    log_file = f"logs/{base}_{prov_name}_{timestamp}.json"
    with open(log_file, "w") as f:
        json.dump(entries, f, indent=2)
    total_elapsed = time.perf_counter() - total_start
    cpu_elapsed = time.process_time() - cpu_start
    print(f"[{provider}] Job done: total_wall={total_elapsed:.2f}s, total_cpu={cpu_elapsed:.2f}s", flush=True)
    recall = passes / len(scenario) if scenario else 0
    return {"provider": provider, "scenario": base, "recall": recall, "log_file": log_file}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Head-to-head benchmark runner for MUD CLI")
    parser.add_argument("scenarios", nargs='+', help="Paths to scenario YAML files or directories")
    parser.add_argument("--providers", required=True, help="Comma-separated OpenRouter provider IDs")
    parser.add_argument("--workers", type=int, default=1, help="Number of concurrent workers")
    parser.add_argument("--window-size", type=int, default=4, help="Sliding window size for memory")
    args = parser.parse_args()
    # Ensure logs directory exists for outputs and error logs
    os.makedirs("logs", exist_ok=True)

    # Resolve scenario files
    scenario_paths = []
    for path in args.scenarios:
        if os.path.isdir(path):
            for fname in os.listdir(path):
                if fname.endswith(('.yaml', '.yml')):
                    scenario_paths.append(os.path.join(path, fname))
        else:
            scenario_paths.append(path)

    providers = args.providers.split(',')
    jobs = [(s, p) for s in scenario_paths for p in providers]
    results = []

    print(f"Running {len(jobs)} jobs with {args.workers} workers...")
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_job = {executor.submit(run_benchmark, s, p, args.window_size): (s, p) for s, p in jobs}
        for future in as_completed(future_to_job):
            s, p = future_to_job[future]
            try:
                res = future.result()
                results.append(res)
                print(f"Completed {res['scenario']} @ {res['provider']}: recall={res['recall']:.2f}")
            except Exception as e:
                tb = traceback.format_exc()
                print(f"Error on {s} @ {p}: {e}")
                print(tb)
                # Save detailed traceback to error log
                base = os.path.splitext(os.path.basename(s))[0]
                prov_name = p.replace('/', '_')
                timestamp = datetime.datetime.now().isoformat(timespec='minutes')
                error_log_file = f"logs/{base}_{prov_name}_{timestamp}_error.log"
                with open(error_log_file, "w") as ef:
                    ef.write(tb)
                print(f"Detailed traceback saved to: {error_log_file}")

    # Summary
    print("\nSummary:")
    for r in results:
        print(f"{r['scenario']:<20} {r['provider']:<30} recall={r['recall']:.2f} log={r['log_file']}")
