import sys
import os
import json
import argparse
import uuid
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.append(backend_dir)
os.chdir(backend_dir)

from app.db.database import SessionLocal
from app.db.models import EvaluationRun, EvaluationResult, Experiment
from app.evaluation.harness import harness

def run_eval(regression_check=False):
    print("Loading Golden Dataset...")
    dataset_path = Path("../datasets/golden/eval_dataset.json")
    if not dataset_path.exists():
        print(f"Error: {dataset_path} not found. Run seed_demo.py first.")
        sys.exit(1)
        
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
        
    db = SessionLocal()
    exp = db.query(Experiment).filter(Experiment.name == "baseline-v1").first()
    if not exp:
        print("Error: Experiment baseline-v1 not found. Run seed_demo.py first.")
        sys.exit(1)
        
    print(f"Starting evaluation on {len(dataset)} questions...")
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    db_run = EvaluationRun(id=run_id, experiment_id=exp.id, dataset_name="golden-v1", status="running")
    db.add(db_run)
    db.commit()
    
    # Run the harness
    evaluation_output = harness.run_evaluation(dataset)
    
    # Save results
    metrics = evaluation_output["metrics"]
    db_run.metrics = metrics
    db_run.status = "completed"
    
    for res in evaluation_output["results"]:
        db_res = EvaluationResult(
            id=f"res_{uuid.uuid4().hex[:8]}",
            evaluation_run_id=run_id,
            question_id="unknown",
            question=res["question"],
            ground_truth=res["ground_truth"],
            generated_answer=res["generated_answer"],
            retrieved_chunks=res["retrieved_chunks"],
            retrieval_scores=res["retrieval_scores"],
            latency_ms=res["latency_ms"],
            metrics=res["metrics"],
            failure_category=res.get("failure_category"),
            failure_reason=res.get("failure_reason"),
            passed=res["passed"]
        )
        db.add(db_res)
        
    db.commit()
    db.close()
    
    print("\n=============================")
    print("RAGBench AI Evaluation Report")
    print("=============================\n")
    print(f"Recall@5:        {metrics.get('recall_at_5', 0):.2f}")
    print(f"Precision@5:     {metrics.get('precision_at_5', 0):.2f}")
    print(f"MRR:             {metrics.get('mrr', 0):.2f}")
    print("-" * 29)
    print(f"Context Recall:  {metrics.get('context_relevance', 0):.2f}")
    print("-" * 29)
    print(f"Faithfulness:    {metrics.get('faithfulness', 0):.2f}")
    print(f"Answer Rel:      {metrics.get('answer_relevance', 0):.2f}")
    print(f"Correctness:     {metrics.get('correctness', 0):.2f}")
    print("-" * 29)
    print(f"Failure Rate:    {metrics.get('failure_rate', 0)*100:.0f}%")
    print(f"Avg Latency:     {metrics.get('average_latency_ms', 0):.0f} ms")
    
    if regression_check:
        print("\nRunning Regression Checks...")
        thresholds = {
            "recall_at_5": 0.85,
            "correctness": 0.85
        }
        passed = True
        for k, v in thresholds.items():
            actual = metrics.get(k, 0)
            if actual < v:
                print(f"FAILED: {k} = {actual:.2f} < {v}")
                passed = False
            else:
                print(f"PASSED: {k} = {actual:.2f} >= {v}")
                
        if not passed:
            print("\nREGRESSION DETECTED")
            sys.exit(1)
        else:
            print("\nALL REGRESSION CHECKS PASSED")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--regression-check", action="store_true", help="Fail if metrics drop below thresholds")
    args = parser.parse_args()
    
    run_eval(regression_check=args.regression_check)
