from typing import List, Dict, Any, Tuple
from app.rag.vector_store import vector_store
from app.rag.bm25 import bm25_store

def normalize_scores(results: List[Tuple[Dict[str, Any], float]]) -> List[Tuple[Dict[str, Any], float]]:
    if not results:
        return []
    
    scores = [score for _, score in results]
    min_score = min(scores)
    max_score = max(scores)
    
    if max_score == min_score:
        # Avoid division by zero, give all max normalized score of 1.0
        return [(doc, 1.0) for doc, _ in results]
        
    normalized_results = []
    for doc, score in results:
        normalized_score = (score - min_score) / (max_score - min_score)
        normalized_results.append((doc, normalized_score))
        
    return normalized_results

class HybridRetriever:
    def __init__(self, vector_weight: float = 0.7, bm25_weight: float = 0.3):
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight
        
    def get_relevant_documents(self, query: str, k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        # Fetch more to allow good hybrid ranking
        fetch_k = max(k * 2, 20)
        
        vector_results = vector_store.similarity_search(query, k=fetch_k)
        bm25_results = bm25_store.similarity_search(query, k=fetch_k)
        
        # Normalize scores
        norm_vector_results = normalize_scores(vector_results)
        norm_bm25_results = normalize_scores(bm25_results)
        
        # Combine results using chunk_id as key
        # Assuming metadata has a 'chunk_id'
        combined_scores = {}
        combined_docs = {}
        
        for doc, score in norm_vector_results:
            chunk_id = doc.get("metadata", {}).get("chunk_id", hash(doc["content"]))
            combined_docs[chunk_id] = doc
            combined_scores[chunk_id] = combined_scores.get(chunk_id, 0.0) + (score * self.vector_weight)
            
        for doc, score in norm_bm25_results:
            chunk_id = doc.get("metadata", {}).get("chunk_id", hash(doc["content"]))
            combined_docs[chunk_id] = doc
            combined_scores[chunk_id] = combined_scores.get(chunk_id, 0.0) + (score * self.bm25_weight)
            
        # Sort by combined score
        sorted_results = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)
        
        # Format output and take top k
        final_results = []
        for chunk_id, score in sorted_results[:k]:
            final_results.append((combined_docs[chunk_id], score))
            
        return final_results
