import hashlib
from typing import List
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MockEmbeddingProvider:
    def __init__(self, model_name: str = "mock-model"):
        self.dim = 384
        
    def _string_to_vector(self, text: str) -> List[float]:
        # Generate a deterministic pseudo-random vector based on text hash
        h = hashlib.sha256(text.encode('utf-8')).digest()
        vec = [float(b) / 255.0 for b in h]
        # Pad or truncate to self.dim
        while len(vec) < self.dim:
            vec.extend(vec)
        return vec[:self.dim]
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        return [self._string_to_vector(t) for t in texts]
        
    def embed_query(self, text: str) -> List[float]:
        return self._string_to_vector(text)

try:
    from sentence_transformers import SentenceTransformer
    class EmbeddingProvider:
        def __init__(self, model_name: str = None):
            if model_name is None:
                model_name = settings.EMBEDDING_MODEL
            self.model = SentenceTransformer(model_name)
            
        def embed_documents(self, texts: List[str]) -> List[List[float]]:
            if not texts:
                return []
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
            
        def embed_query(self, text: str) -> List[float]:
            return self.model.encode([text])[0].tolist()
except Exception as e:
    print(f"Failed to load sentence_transformers ({e}). Using mock embeddings.")
    EmbeddingProvider = MockEmbeddingProvider

embedding_provider = None

def get_embedding_provider():
    global embedding_provider
    if embedding_provider is None:
        embedding_provider = EmbeddingProvider()
    return embedding_provider
