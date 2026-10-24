import faiss
import numpy as np
from typing import List, Dict, Any, Tuple
from app.rag.embeddings import get_embedding_provider

class FAISSVectorStore:
    def __init__(self, embedding_dim: int = 384): # 384 is dim for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.doc_map: Dict[int, Dict[str, Any]] = {}
        self.current_id = 0
        self.embedding_provider = get_embedding_provider()
        
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        if not texts:
            return
            
        embeddings = self.embedding_provider.embed_documents(texts)
        embeddings_np = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings_np)
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
            
        for text, meta in zip(texts, metadatas):
            self.doc_map[self.current_id] = {
                "content": text,
                "metadata": meta
            }
            self.current_id += 1
            
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        if self.current_id == 0:
            return []
            
        query_embedding = self.embedding_provider.embed_query(query)
        query_np = np.array([query_embedding]).astype('float32')
        
        # We might have less documents than k
        actual_k = min(k, self.current_id)
        
        distances, indices = self.index.search(query_np, actual_k)
        
        results = []
        for i in range(actual_k):
            idx = indices[0][i]
            if idx != -1: # -1 means not found
                dist = distances[0][i]
                # Invert distance to score (L2 distance: lower is better. Score: higher is better)
                score = 1.0 / (1.0 + float(dist))
                doc_info = self.doc_map[int(idx)]
                results.append((doc_info, score))
                
        return results

# Singleton instance for simplicity in memory
vector_store = FAISSVectorStore()
