from typing import List, Set
import math

def calculate_recall_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    if not relevant_ids:
        return 0.0
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = set(retrieved_k).intersection(relevant_ids)
    return len(relevant_retrieved) / len(relevant_ids)

def calculate_precision_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    if k == 0:
        return 0.0
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = set(retrieved_k).intersection(relevant_ids)
    return len(relevant_retrieved) / min(k, len(retrieved_ids) if len(retrieved_ids) > 0 else k)

def calculate_mrr(retrieved_ids: List[str], relevant_ids: Set[str]) -> float:
    for i, doc_id in enumerate(retrieved_ids):
        if doc_id in relevant_ids:
            return 1.0 / (i + 1)
    return 0.0

def calculate_ndcg(retrieved_ids: List[str], relevant_ids: Set[str], k: int = None) -> float:
    if k is not None:
        retrieved_ids = retrieved_ids[:k]
        
    dcg = 0.0
    for i, doc_id in enumerate(retrieved_ids):
        if doc_id in relevant_ids:
            # Relevance score is binary (1 or 0)
            dcg += 1.0 / math.log2(i + 2) # i is 0-indexed, so i+1 is rank, i+2 for log2 base
            
    idcg = 0.0
    for i in range(min(len(relevant_ids), len(retrieved_ids) if k is None else k)):
        idcg += 1.0 / math.log2(i + 2)
        
    if idcg == 0.0:
        return 0.0
        
    return dcg / idcg
