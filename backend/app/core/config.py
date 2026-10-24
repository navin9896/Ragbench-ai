from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAGBench AI"
    
    # Database
    DATABASE_URL: str = "sqlite:///./ragbench.db"
    
    # RAG Settings
    MOCK_MODE: bool = True
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "mock"
    
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_STORE: str = "faiss"
    
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    
    TOP_K: int = 5
    RERANKER_ENABLED: bool = False
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
