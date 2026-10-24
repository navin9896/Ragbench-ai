from typing import Dict, Any, List

class FailureAnalyzer:
    def classify_failure(self, 
                         retrieval_metrics: Dict[str, float], 
                         generation_metrics: Dict[str, float]) -> Dict[str, str]:
        
        # Thresholds
        recall_threshold = 0.8
        faithfulness_threshold = 0.8
        correctness_threshold = 0.8
        
        recall = retrieval_metrics.get("recall_at_5", 0.0)
        faithfulness = generation_metrics.get("faithfulness", 0.0)
        correctness = generation_metrics.get("correctness", 0.0)
        
        if recall < recall_threshold:
            return {
                "category": "RETRIEVAL_FAILURE",
                "reason": "The system failed to retrieve relevant context to answer the question."
            }
            
        if faithfulness < faithfulness_threshold:
            return {
                "category": "HALLUCINATION",
                "reason": "The system retrieved relevant context but generated an answer not supported by it."
            }
            
        if correctness < correctness_threshold:
            return {
                "category": "GENERATION_FAILURE",
                "reason": "The system retrieved context and remained faithful, but failed to extract the correct answer."
            }
            
        return {
            "category": "OTHER",
            "reason": "The system failed for an unknown reason despite decent metrics."
        }
        
failure_analyzer = FailureAnalyzer()
