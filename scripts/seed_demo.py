import sys
import os
import json
import uuid
import shutil
from pathlib import Path

# Add project root and backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.append(backend_dir)

# Ensure we are working relative to backend for imports
os.chdir(backend_dir)

from app.db.database import SessionLocal, engine, Base
from app.db.models import Document, Chunk, Experiment, EvaluationRun, EvaluationResult
from app.rag.vector_store import vector_store
from app.rag.bm25 import bm25_store
from app.rag.chunking import chunk_document

print("Creating database tables...")
Base.metadata.create_all(bind=engine)

print("Writing sample documents...")
# Paths relative to backend
docs_dir = Path("../datasets/documents")
docs_dir.mkdir(parents=True, exist_ok=True)

with open(docs_dir / "hr_policy.txt", "w") as f:
    f.write("Company HR Policy\n=================\n\nLeave Policy:\nEmployees are entitled to 20 days of paid time off (PTO) per year according to the HR policy.\nPart-time employees get 3 paid sick days per year.\n\nBenefits:\nFull-time employees receive health insurance, dental insurance, and a 401k match up to 4%.\n\nLeadership:\nSarah Jenkins is the VP of Engineering.\nMichael Scott is the Regional Manager.\n")

with open(docs_dir / "shipping_policy.txt", "w") as f:
    f.write("Shipping and Returns\n====================\n\nShipping:\nStandard shipping takes 3-5 business days across the continental US.\nFor urgent orders, customers can select expedited shipping for 1-2 business day delivery.\n\nReturns:\nElectronics can be returned within 14 days in original packaging.\nApparel has a 30-day return window.\nRefunds are processed within 7 business days of receiving the returned item.\n")

print("Processing documents and chunks...")
db = SessionLocal()

# Add to DB and Stores
all_chunks_text = []
all_metadatas = []

for filepath in docs_dir.glob("*.txt"):
    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    db_doc = Document(id=doc_id, filename=filepath.name, file_type="txt", status="completed")
    db.add(db_doc)
    
    with open(filepath, "r") as f:
        content = f.read()
        
    chunks = chunk_document(content, chunk_size=200, chunk_overlap=50)
    for i, c_text in enumerate(chunks):
        chunk_id = f"chunk_{uuid.uuid4().hex[:8]}"
        meta = {"document_id": doc_id, "chunk_id": chunk_id, "source": filepath.name}
        
        db_chunk = Chunk(id=chunk_id, document_id=doc_id, chunk_index=i, content=c_text, metadata_json=meta)
        db.add(db_chunk)
        
        all_chunks_text.append(c_text)
        all_metadatas.append(meta)

db.commit()

print("Building vector and keyword indexes...")
vector_store.add_texts(all_chunks_text, all_metadatas)
bm25_store.add_texts(all_chunks_text, all_metadatas)

print("Generating Golden Dataset (50 questions)...")
golden_dir = Path("../datasets/golden")
golden_dir.mkdir(parents=True, exist_ok=True)

base_questions = [
    {"q": "How many PTO days do we get?", "a": "Employees are entitled to 20 days of paid time off (PTO) per year.", "c": "hr_policy.txt"},
    {"q": "What is the return policy for electronics?", "a": "Electronics can be returned within 14 days in original packaging.", "c": "shipping_policy.txt"},
    {"q": "Who is the VP of Engineering?", "a": "Sarah Jenkins is the VP of Engineering.", "c": "hr_policy.txt"},
    {"q": "How long does standard shipping take?", "a": "Standard shipping takes 3-5 business days across the continental US.", "c": "shipping_policy.txt"},
    {"q": "Do part-time employees get sick days?", "a": "Yes, part-time employees get 3 paid sick days per year.", "c": "hr_policy.txt"},
    {"q": "When are refunds processed?", "a": "Refunds are processed within 7 business days of receiving the returned item.", "c": "shipping_policy.txt"}
]

dataset = []
# Replicate and perturb slightly to reach 50
for i in range(50):
    base = base_questions[i % len(base_questions)]
    dataset.append({
        "id": f"q_{i}",
        "question": base["q"].replace("?", f" {i}?") if i >= len(base_questions) else base["q"],
        "ground_truth": base["a"],
        "relevant_document_ids": [],
        "relevant_chunk_ids": [],
        "category": "simple",
        "difficulty": "easy"
    })

with open(golden_dir / "eval_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Creating baseline experiment...")
exp_id = f"exp_{uuid.uuid4().hex[:8]}"
db_exp = Experiment(
    id=exp_id, 
    name="baseline-v1", 
    config={
        "chunk_size": 200, 
        "chunk_overlap": 50, 
        "retrieval": {"type": "hybrid", "top_k": 5}
    }
)
db.add(db_exp)
db.commit()
db.close()

print("Seed complete.")
