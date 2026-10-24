import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation.retrieval_metrics import calculate_recall_at_k, calculate_precision_at_k, calculate_mrr

def test_recall():
    retrieved = ["a", "b", "c", "d", "e"]
    relevant = {"b", "e", "f"}
    assert calculate_recall_at_k(retrieved, relevant, 5) == 2 / 3

def test_precision():
    retrieved = ["a", "b", "c", "d", "e"]
    relevant = {"b", "e", "f"}
    assert calculate_precision_at_k(retrieved, relevant, 5) == 2 / 5
    
def test_mrr():
    retrieved = ["a", "b", "c", "d", "e"]
    relevant = {"c"}
    assert calculate_mrr(retrieved, relevant) == 1 / 3
