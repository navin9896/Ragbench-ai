import os
import pymupdf
import docx
from pathlib import Path

def extract_text_from_pdf(filepath: str) -> str:
    text = ""
    try:
        doc = pymupdf.open(filepath)
        for page in doc:
            text += page.get_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
    return text

def extract_text_from_docx(filepath: str) -> str:
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
    return text

def extract_text_from_txt(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {filepath}: {e}")
        return ""

def load_document(filepath: str, file_type: str) -> str:
    file_type = file_type.lower()
    if file_type == 'pdf':
        return extract_text_from_pdf(filepath)
    elif file_type == 'docx':
        return extract_text_from_docx(filepath)
    elif file_type in ['txt', 'md']:
        return extract_text_from_txt(filepath)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
