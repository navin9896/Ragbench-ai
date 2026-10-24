from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String)
    source = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    error_message = Column(String, nullable=True)

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, ForeignKey("documents.id"))
    chunk_index = Column(Integer)
    content = Column(String)
    page_number = Column(Integer, nullable=True)
    metadata_json = Column(JSON, nullable=True)

    document = relationship("Document", back_populates="chunks")

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    config = Column(JSON)  # Stores embedding_model, chunk_size, chunk_overlap, top_k, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    evaluation_runs = relationship("EvaluationRun", back_populates="experiment", cascade="all, delete-orphan")

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String, primary_key=True, index=True)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    dataset_name = Column(String)
    status = Column(String, default="running") # running, completed, failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Aggregated metrics
    metrics = Column(JSON, nullable=True) 

    experiment = relationship("Experiment", back_populates="evaluation_runs")
    results = relationship("EvaluationResult", back_populates="evaluation_run", cascade="all, delete-orphan")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(String, primary_key=True, index=True)
    evaluation_run_id = Column(String, ForeignKey("evaluation_runs.id"))
    question_id = Column(String)
    question = Column(String)
    ground_truth = Column(String)
    generated_answer = Column(String)
    
    # Execution details
    retrieved_chunks = Column(JSON, nullable=True)  # List of chunk contents/metadata
    retrieval_scores = Column(JSON, nullable=True)
    latency_ms = Column(Float, nullable=True)
    
    # Individual question metrics
    metrics = Column(JSON, nullable=True) 
    
    # Failure analysis
    failure_category = Column(String, nullable=True)
    failure_reason = Column(String, nullable=True)
    passed = Column(Boolean, default=False)

    evaluation_run = relationship("EvaluationRun", back_populates="results")
