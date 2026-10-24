from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.rag.llm import get_llm_provider
from app.core.config import settings
from langchain_core.messages import HumanMessage, SystemMessage
import json
import logging

logger = logging.getLogger(__name__)

class EvaluationScore(BaseModel):
    score: float
    reason: str
    passed: bool

class LLMJudge:
    def __init__(self):
        self.llm = get_llm_provider()
        
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        try:
            # Remove markdown formatting if any
            clean_str = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_str)
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}\nResponse: {response}")
            return {"score": 0.0, "reason": f"Failed to parse LLM response: {e}", "passed": False}
            
    def _mock_evaluate(self, metric: str, generated_answer: str, ground_truth: str, context: str) -> EvaluationScore:
        # Simple heuristic based mock evaluation
        generated_answer_lower = generated_answer.lower()
        ground_truth_lower = ground_truth.lower()
        context_lower = context.lower()
        
        score = 0.5
        reason = "Average based on mock heuristic."
        
        if metric == "correctness":
            if ground_truth_lower in generated_answer_lower or any(word in generated_answer_lower for word in ground_truth_lower.split() if len(word) > 4):
                score = 0.95
                reason = "Answer contains elements of ground truth."
            else:
                score = 0.2
                reason = "Answer does not align with ground truth."
                
        elif metric == "faithfulness":
            if "sorry, i couldn't find" in generated_answer_lower:
                score = 1.0
                reason = "Properly admitted lack of knowledge."
            elif all(word in context_lower for word in generated_answer_lower.split() if len(word) > 5):
                score = 0.9
                reason = "Words seem grounded in context."
            else:
                score = 0.6
                reason = "Some ungrounded terms used."
                
        elif metric == "answer_relevance":
            score = 0.9
            reason = "Answer seems relevant to the question format."
            
        elif metric in ["context_recall", "context_precision", "context_relevance"]:
            if ground_truth_lower in context_lower or any(word in context_lower for word in ground_truth_lower.split() if len(word) > 4):
                score = 0.95
                reason = "Context contains required information."
            else:
                score = 0.1
                reason = "Context misses ground truth."
                
        passed = score >= 0.8
        return EvaluationScore(score=score, reason=reason, passed=passed)

    def evaluate_correctness(self, question: str, generated_answer: str, ground_truth: str) -> EvaluationScore:
        if settings.MOCK_MODE or settings.LLM_PROVIDER == "mock":
            return self._mock_evaluate("correctness", generated_answer, ground_truth, "")
            
        prompt = f"""
Evaluate the correctness of the generated answer compared to the ground truth.
Question: {question}
Ground Truth: {ground_truth}
Generated Answer: {generated_answer}

Respond ONLY in JSON format:
{{
  "score": <float between 0.0 and 1.0>,
  "reason": "<brief explanation>",
  "passed": <boolean, true if score >= 0.8>
}}
"""
        response, _ = self.llm.generate_answer(prompt, "") 
        result = self._parse_json_response(response)
        return EvaluationScore(**result)

    def evaluate_faithfulness(self, question: str, generated_answer: str, context: str) -> EvaluationScore:
        if settings.MOCK_MODE or settings.LLM_PROVIDER == "mock":
            return self._mock_evaluate("faithfulness", generated_answer, "", context)
            
        prompt = f"""
Evaluate if the generated answer is faithful to the provided context. It should not contain hallucinations.
Question: {question}
Context: {context}
Generated Answer: {generated_answer}

Respond ONLY in JSON format:
{{
  "score": <float between 0.0 and 1.0>,
  "reason": "<brief explanation>",
  "passed": <boolean, true if score >= 0.8>
}}
"""
        response, _ = self.llm.generate_answer(prompt, "")
        result = self._parse_json_response(response)
        return EvaluationScore(**result)
        
    def evaluate_answer_relevance(self, question: str, generated_answer: str) -> EvaluationScore:
        if settings.MOCK_MODE or settings.LLM_PROVIDER == "mock":
            return self._mock_evaluate("answer_relevance", generated_answer, "", "")
            
        prompt = f"""
Evaluate if the generated answer directly addresses the question without unnecessary verbosity.
Question: {question}
Generated Answer: {generated_answer}

Respond ONLY in JSON format:
{{
  "score": <float between 0.0 and 1.0>,
  "reason": "<brief explanation>",
  "passed": <boolean, true if score >= 0.8>
}}
"""
        response, _ = self.llm.generate_answer(prompt, "")
        result = self._parse_json_response(response)
        return EvaluationScore(**result)

    def evaluate_context_relevance(self, question: str, context: str, ground_truth: str) -> EvaluationScore:
        if settings.MOCK_MODE or settings.LLM_PROVIDER == "mock":
            return self._mock_evaluate("context_relevance", "", ground_truth, context)
            
        prompt = f"""
Evaluate if the provided context contains the information needed to answer the question, compared to the ground truth.
Question: {question}
Ground Truth: {ground_truth}
Context: {context}

Respond ONLY in JSON format:
{{
  "score": <float between 0.0 and 1.0>,
  "reason": "<brief explanation>",
  "passed": <boolean, true if score >= 0.8>
}}
"""
        response, _ = self.llm.generate_answer(prompt, "")
        result = self._parse_json_response(response)
        return EvaluationScore(**result)

llm_judge = LLMJudge()
