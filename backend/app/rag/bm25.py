from rank_bm25 import BM25Okapi
from typing import List, Dict, Any, Tuple
import string

class BM25Store:
    def __init__(self):
        self.corpus: List[str] = []
        self.tokenized_corpus: List[List[str]] = []
        self.metadata: List[Dict[str, Any]] = []
        self.bm25 = None
        
    def _tokenize(self, text: str) -> List[str]:
        # Simple tokenization: lowercase, remove punctuation, split by space
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.split()
        
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        if not texts:
            return
            
        if metadatas is None:
            metadatas = [{} for _ in texts]
            
        self.corpus.extend(texts)
        self.metadata.extend(metadatas)
        
        # Tokenize new texts and add to tokenized_corpus
        new_tokenized = [self._tokenize(text) for text in texts]
        self.tokenized_corpus.extend(new_tokenized)
        
        # Re-initialize BM25 model
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        if self.bm25 is None or len(self.corpus) == 0:
            return []
            
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k indices
        actual_k = min(k, len(self.corpus))
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:actual_k]
        
        results = []
        for idx in top_k_indices:
            score = scores[idx]
            if score > 0: # Only return documents with some matching terms
                doc_info = {
                    "content": self.corpus[idx],
                    "metadata": self.metadata[idx]
                }
                results.append((doc_info, score))
                
        return results

# Singleton instance
bm25_store = BM25Store()
