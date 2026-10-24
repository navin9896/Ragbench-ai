from typing import List, Dict, Any, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
import time
import json

class LLMProvider:
    def generate_answer(self, query: str, context: str) -> Tuple[str, Dict[str, Any]]:
        raise NotImplementedError

class MockLLMProvider(LLMProvider):
    def generate_answer(self, query: str, context: str) -> Tuple[str, Dict[str, Any]]:
        start_time = time.time()
        time.sleep(0.1) # Simulate some latency
        
        if not context.strip():
            answer = "I'm sorry, I couldn't find relevant information in the provided context to answer your question."
        else:
            if "shipping" in query.lower():
                answer = "Based on the shipping policy, standard delivery takes 3-5 business days."
            elif "leave" in query.lower() or "pto" in query.lower():
                answer = "Employees are entitled to 20 days of paid time off per year according to the HR policy."
            elif "refund" in query.lower():
                answer = "Refunds are processed within 7 business days of receiving the returned item."
            else:
                words = context.split()
                summary = " ".join(words[:25]) + "..."
                answer = f"Based on the provided context: {summary}"
                
        latency = (time.time() - start_time) * 1000
        usage = {"input_tokens": len(context.split()), "output_tokens": len(answer.split()), "total_cost": 0.0}
        
        return answer, usage

class OpenAIProvider(LLMProvider):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAIProvider")
        self.llm = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
        
    def generate_answer(self, query: str, context: str) -> Tuple[str, Dict[str, Any]]:
        system_prompt = """
You are a grounded knowledge assistant.

Answer only using the supplied context.

Do not invent facts.

If the answer cannot be determined from the context,
say that the information is not available.

Do not fabricate sources.

Prefer concise, direct answers.
"""
        
        user_prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
        
        start_time = time.time()
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        meta = response.response_metadata
        token_usage = meta.get("token_usage", {})
        
        input_tokens = token_usage.get("prompt_tokens", 0)
        output_tokens = token_usage.get("completion_tokens", 0)
        cost = (input_tokens * 0.0000015) + (output_tokens * 0.000002)
        
        usage = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": cost
        }
        
        return response.content, usage

def get_llm_provider() -> LLMProvider:
    if settings.MOCK_MODE or settings.LLM_PROVIDER == "mock":
        return MockLLMProvider()
    else:
        return OpenAIProvider()
