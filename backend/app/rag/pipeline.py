from typing import Dict, Any, List
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.llm import get_llm_provider
from app.core.config import settings
import time

class RAGPipeline:
    def __init__(self):
        self.retriever = HybridRetriever(
            vector_weight=0.7, 
            bm25_weight=0.3
        )
        self.llm = get_llm_provider()
        
    def run(self, query: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Retrieval
        retrieval_start = time.time()
        raw_results = self.retriever.get_relevant_documents(query, k=settings.TOP_K)
        retrieval_latency = (time.time() - retrieval_start) * 1000
        
        # Extract chunks and scores
        retrieved_chunks = []
        retrieval_scores = []
        sources = set()
        
        context_parts = []
        
        for doc, score in raw_results:
            retrieved_chunks.append(doc)
            retrieval_scores.append(score)
            
            meta = doc.get("metadata", {})
            source_id = meta.get("document_id")
            if source_id:
                sources.add(source_id)
                
            content = doc.get("content", "")
            context_parts.append(f"Source [{source_id}]:\n{content}")
            
        context_str = "\n\n".join(context_parts)
        
        # 2. Generation
        gen_start = time.time()
        answer, token_usage = self.llm.generate_answer(query, context_str)
        gen_latency = (time.time() - gen_start) * 1000
        
        total_latency = (time.time() - start_time) * 1000
        
        return {
            "question": query,
            "answer": answer,
            "sources": list(sources),
            "retrieved_chunks": retrieved_chunks,
            "retrieval_scores": retrieval_scores,
            "reranker_scores": [],
            "latency_ms": total_latency,
            "retrieval_latency_ms": retrieval_latency,
            "generation_latency_ms": gen_latency,
            "token_usage": token_usage,
            "estimated_cost": token_usage.get("total_cost", 0.0),
            "metadata": {}
        }

rag_pipeline = RAGPipeline()
