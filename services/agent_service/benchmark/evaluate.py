# benchmark/evaluate.py
import json
import os
import glob
from datetime import datetime

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

CRITERIA = {
    "uses_run_pipeline":        {"weight": 25, "description": "Agent uses run_pipeline directly"},
    "extracts_fields":          {"weight": 25, "description": "Extracts fields from user message"},
    "asks_one_at_a_time":       {"weight": 20, "description": "Asks one field at a time"},
    "remembers_context":        {"weight": 20, "description": "Remembers context across turns"},
    "never_invents_fields":     {"weight": 10, "description": "Never asks for non-existent fields"},
}

INVENTED_FIELDS = ["project name", "test plan"]


def auto_score(results: dict) -> dict:
    scores = {k: 0 for k in CRITERIA}
    notes = []

    all_agent_responses = " ".join(
        t["agent"].lower() for t in results["turns"]
    )

    # Check if run_pipeline was used
    if "run_pipeline" in all_agent_responses or "pipeline completed" in all_agent_responses:
        scores["uses_run_pipeline"] = 100
    else:
        notes.append("❌ Agent did not use run_pipeline")

    # Check for invented fields
    invented = [f for f in INVENTED_FIELDS if f in all_agent_responses]
    if not invented:
        scores["never_invents_fields"] = 100
    else:
        notes.append(f"❌ Invented fields detected: {invented}")

    # Check one field at a time (heuristic: count question marks per turn)
    multi_question_turns = 0
    for turn in results["turns"]:
        agent_response = turn["agent"]
        question_count = agent_response.count("?")
        if question_count > 2:
            multi_question_turns += 1

    if multi_question_turns == 0:
        scores["asks_one_at_a_time"] = 100
    elif multi_question_turns == 1:
        scores["asks_one_at_a_time"] = 50
        notes.append("⚠️  Agent asked multiple questions in one turn")
    else:
        notes.append(f"❌ Agent asked multiple questions in {multi_question_turns} turns")

    return {"scores": scores, "notes": notes}


def compute_final_score(scores: dict) -> float:
    total = 0
    for criterion, score in scores.items():
        weight = CRITERIA[criterion]["weight"]
        total += (score / 100) * weight
    return round(total, 2)


def evaluate_model(model_name: str) -> dict:
    safe_model = model_name.replace(":", "_").replace("/", "_")
    model_dir = os.path.join(RESULTS_DIR, safe_model)

    if not os.path.exists(model_dir):
        print(f"❌ No results found for model: {model_name}")
        return {}

    result_files = glob.glob(os.path.join(model_dir, "*.json"))
    all_scores = []

    print(f"\n{'='*60}")
    print(f"Model: {model_name}")
    print(f"{'='*60}")

    for filepath in sorted(result_files):
        with open(filepath) as f:
            results = json.load(f)

        evaluation = auto_score(results)
        final_score = compute_final_score(evaluation["scores"])
        all_scores.append(final_score)

        print(f"\n📋 Scenario: {results['scenario_name']}")
        print(f"   Final Score: {final_score}/100")

        for criterion, score in evaluation["scores"].items():
            weight = CRITERIA[criterion]["weight"]
            label = "✅" if score == 100 else ("⚠️ " if score >= 50 else "❌")
            print(f"   {label} {CRITERIA[criterion]['description']}: {score}/100 (weight: {weight}%)")

        if evaluation["notes"]:
            for note in evaluation["notes"]:
                print(f"   {note}")

    avg_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    print(f"\n🏆 Average Score: {avg_score}/100")

    return {"model": model_name, "average_score": avg_score, "scenario_scores": all_scores}


def compare_models():
    if not os.path.exists(RESULTS_DIR):
        print("❌ No results directory found. Run run_benchmark.py first.")
        return

    models = [d for d in os.listdir(RESULTS_DIR) if os.path.isdir(os.path.join(RESULTS_DIR, d))]

    if not models:
        print("❌ No model results found.")
        return

    model_results = []
    for model_dir in models:
        model_name = model_dir.replace("_", ":", 1)
        result = evaluate_model(model_name)
        if result:
            model_results.append(result)

    # Final comparison table
    if len(model_results) > 1:
        print(f"\n{'='*60}")
        print("COMPARISON SUMMARY")
        print(f"{'='*60}")
        print(f"{'Model':<25} {'Avg Score':>10}")
        print("-" * 37)
        for r in sorted(model_results, key=lambda x: x["average_score"], reverse=True):
            print(f"{r['model']:<25} {r['average_score']:>10}/100")

        winner = max(model_results, key=lambda x: x["average_score"])
        print(f"\n🏆 Winner: {winner['model']} ({winner['average_score']}/100)")


if __name__ == "__main__":
    compare_models()