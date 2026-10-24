from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(content: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """
    Split the document into chunks using RecursiveCharacterTextSplitter.
    """
    if not content:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(content)
    return chunks
