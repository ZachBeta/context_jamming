#!/usr/bin/env python3
import argparse
import os, sys
from head_to_head import run_benchmark

def main():
    parser = argparse.ArgumentParser(description="Sweep sliding-window sizes to find minimal size for 100% recall")
    parser.add_argument("scenario", help="Path to a YAML scenario file")
    parser.add_argument("--providers", required=True, help="Comma-separated OpenRouter provider IDs")
    parser.add_argument("--min-window", type=int, default=1, help="Minimum window size to test")
    parser.add_argument("--max-window", type=int, default=10, help="Maximum window size to test")
    args = parser.parse_args()

    providers = args.providers.split(',')
    print(f"Sweeping window sizes for scenario {args.scenario}")
    summary = []
    for provider in providers:
        print(f"\n### Sweeping {provider} ###", flush=True)
        last_pass = None
        # Test full window first
        print(f"Testing {provider} with full window_size={args.max_window}", flush=True)
        try:
            result = run_benchmark(args.scenario, provider, args.max_window)
            recall = result.get('recall', 0)
        except Exception as err:
            print(f"Error for {provider} at full window {args.max_window}: {err}", flush=True)
            summary.append({'provider': provider, 'window_size': None})
            continue
        if recall < 1.0:
            print(f"❌ {provider} failed full window {args.max_window}: recall={recall:.2f}", flush=True)
            summary.append({'provider': provider, 'window_size': None})
            continue
        # Step down to find minimal passing window
        for window in range(args.max_window, args.min_window - 1, -1):
            print(f"Testing {provider} with window_size={window}", flush=True)
            try:
                res = run_benchmark(args.scenario, provider, window)
                rec = res.get('recall', 0)
            except Exception as err:
                print(f"Error for {provider} at window {window}: {err}", flush=True)
                continue
            print(f"Result: recall={rec:.2f}", flush=True)
            if rec >= 1.0:
                last_pass = window
            else:
                break
        if last_pass is not None:
            print(f"✅ {provider} minimal window_size for 100% recall = {last_pass}", flush=True)
            summary.append({'provider': provider, 'window_size': last_pass})
        else:
            summary.append({'provider': provider, 'window_size': None})

    print("\nSweep Summary:")
    for entry in summary:
        ws = entry['window_size'] if entry['window_size'] is not None else '>='+str(args.max_window)
        print(f"{entry['provider']}: minimal window_size = {ws}")

if __name__ == '__main__':
    main()
