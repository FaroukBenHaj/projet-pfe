# benchmark/run_benchmark.py
import json
import os
import sys
import argparse
from datetime import datetime

# Add parent directory to path so we can import agent modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from react_loop import run

SCENARIOS_DIR = os.path.join(os.path.dirname(__file__), "scenarios")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def load_scenarios() -> list:
    scenarios = []
    for filename in sorted(os.listdir(SCENARIOS_DIR)):
        if filename.endswith(".json"):
            with open(os.path.join(SCENARIOS_DIR, filename)) as f:
                scenarios.append(json.load(f))
    return scenarios


def run_scenario(scenario: dict, model_name: str) -> dict:
    print(f"\n{'='*60}")
    print(f"Running: {scenario['name']}")
    print(f"{'='*60}")

    results = {
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "turns": []
    }

    # Handle edge case scenarios (list of turns with different structure)
    turns = scenario.get("turns", [])

    for turn in turns:
        # Support both simple turns and edge case turns
        user_msg = turn.get("user", "")
        turn_id = turn.get("turn", turn.get("id", "?"))

        print(f"\n[Turn {turn_id}] You: {user_msg}")

        try:
            response = run(user_msg , thread_id=scenario["id"])
            print(f"[Turn {turn_id}] Agent: {response}")
        except Exception as e:
            response = f"ERROR: {str(e)}"
            print(f"[Turn {turn_id}] ERROR: {str(e)}")

        results["turns"].append({
            "turn": turn_id,
            "user": user_msg,
            "agent": response,
        })

    return results


def save_results(results: dict, model_name: str):
    # Sanitize model name for folder
    safe_model = model_name.replace(":", "_").replace("/", "_")
    model_dir = os.path.join(RESULTS_DIR, safe_model)
    os.makedirs(model_dir, exist_ok=True)

    filename = f"{results['scenario_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(model_dir, filename)

    with open(filepath, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Run DefectDojo Agent Benchmark")
    parser.add_argument("--model", default="qwen2.5:7b", help="Ollama model name")
    parser.add_argument("--scenario", default=None, help="Run specific scenario ID (e.g. scenario_01)")
    args = parser.parse_args()

    scenarios = load_scenarios()

    if args.scenario:
        scenarios = [s for s in scenarios if s["id"] == args.scenario]
        if not scenarios:
            print(f"❌ Scenario '{args.scenario}' not found.")
            sys.exit(1)

    print(f"\n🚀 Running benchmark with model: {args.model}")
    print(f"📋 Scenarios to run: {len(scenarios)}")

    for scenario in scenarios:
        # Skip edge case scenarios in auto mode (they need manual evaluation)
        if scenario["id"] == "scenario_04":
            print(f"\n⚠️  Skipping {scenario['name']} — requires manual evaluation")
            continue

        results = run_scenario(scenario, args.model)
        save_results(results, args.model)

    print(f"\n✅ Benchmark complete. Check benchmark/results/{args.model.replace(':', '_')}/")


if __name__ == "__main__":
    main()