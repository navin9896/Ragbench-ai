from typing import List, Dict, Any
from app.rag.pipeline import rag_pipeline
from app.evaluation.retrieval_metrics import calculate_recall_at_k, calculate_precision_at_k, calculate_mrr, calculate_ndcg
from app.evaluation.llm_judge import llm_judge
from app.evaluation.failure_analyzer import failure_analyzer
import time

class EvaluationHarness:
    def run_evaluation(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = []
        
        # Aggregators
        total_latency = 0
        sum_recall_5 = 0
        sum_precision_5 = 0
        sum_mrr = 0
        
        sum_correctness = 0
        sum_faithfulness = 0
        sum_answer_relevance = 0
        sum_context_relevance = 0
        
        failures = 0
        
        for record in dataset:
            question = record["question"]
            ground_truth = record["ground_truth"]
            relevant_ids = set(record.get("relevant_chunk_ids", []))
            
            # 1. Run RAG Pipeline
            start_time = time.time()
            rag_result = rag_pipeline.run(question)
            latency = (time.time() - start_time) * 1000
            total_latency += latency
            
            # 2. Retrieval Metrics
            retrieved_chunks = rag_result["retrieved_chunks"]
            retrieved_ids = [doc.get("metadata", {}).get("chunk_id", str(hash(doc.get("content")))) for doc in retrieved_chunks]
            
            # Mocking relevant ids if not provided for pure functional testing of metrics
            if not relevant_ids and retrieved_ids:
                 relevant_ids = {retrieved_ids[0]}
            
            recall_5 = calculate_recall_at_k(retrieved_ids, relevant_ids, k=5)
            precision_5 = calculate_precision_at_k(retrieved_ids, relevant_ids, k=5)
            mrr = calculate_mrr(retrieved_ids, relevant_ids)
            
            retrieval_metrics = {
                "recall_at_5": recall_5,
                "precision_at_5": precision_5,
                "mrr": mrr
            }
            
            sum_recall_5 += recall_5
            sum_precision_5 += precision_5
            sum_mrr += mrr
            
            # 3. Generation Metrics (LLM as Judge)
            generated_answer = rag_result["answer"]
            
            # Construct full context string
            context_str = "\n\n".join([doc.get("content", "") for doc in retrieved_chunks])
            
            correctness_eval = llm_judge.evaluate_correctness(question, generated_answer, ground_truth)
            faithfulness_eval = llm_judge.evaluate_faithfulness(question, generated_answer, context_str)
            ans_rel_eval = llm_judge.evaluate_answer_relevance(question, generated_answer)
            ctx_rel_eval = llm_judge.evaluate_context_relevance(question, context_str, ground_truth)
            
            generation_metrics = {
                "correctness": correctness_eval.score,
                "faithfulness": faithfulness_eval.score,
                "answer_relevance": ans_rel_eval.score,
                "context_relevance": ctx_rel_eval.score
            }
            
            sum_correctness += correctness_eval.score
            sum_faithfulness += faithfulness_eval.score
            sum_answer_relevance += ans_rel_eval.score
            sum_context_relevance += ctx_rel_eval.score
            
            # 4. Failure Analysis
            passed = correctness_eval.passed
            failure_category = None
            failure_reason = None
            
            if not passed:
                failures += 1
                analysis = failure_analyzer.classify_failure(retrieval_metrics, generation_metrics)
                failure_category = analysis["category"]
                failure_reason = analysis["reason"]
                
            # Assemble result
            result_record = {
                "question": question,
                "ground_truth": ground_truth,
                "generated_answer": generated_answer,
                "retrieved_chunks": retrieved_chunks,
                "retrieval_scores": rag_result["retrieval_scores"],
                "latency_ms": latency,
                "metrics": {**retrieval_metrics, **generation_metrics},
                "passed": passed,
                "failure_category": failure_category,
                "failure_reason": failure_reason
            }
            results.append(result_record)
            
        # Aggregate
        n = len(dataset)
        aggregated_metrics = {}
        if n > 0:
            aggregated_metrics = {
                "recall_at_5": sum_recall_5 / n,
                "precision_at_5": sum_precision_5 / n,
                "mrr": sum_mrr / n,
                "correctness": sum_correctness / n,
                "faithfulness": sum_faithfulness / n,
                "answer_relevance": sum_answer_relevance / n,
                "context_relevance": sum_context_relevance / n,
                "failure_rate": failures / n,
                "average_latency_ms": total_latency / n
            }
            
        return {
            "metrics": aggregated_metrics,
            "results": results
        }

harness = EvaluationHarness()
