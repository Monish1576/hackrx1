import fitz  # PyMuPDF
import re


def extract_atomic_clauses(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    clause_id = 0
    clauses = []

    for page in doc:
        text = page.get_text("text")
        # Hierarchical clause splitting
        for section in re.split(r'\n\s*(?:[A-Z][A-Z\s]+\:|\d+\.\s|[a-z]\)\s)', text):
            if not section.strip():
                continue
            # Clause-level segmentation
            sub_clauses = re.split(r'(?<=\;|\]|\.)\s+(?=\w)', section)
            for i, clause in enumerate(sub_clauses):
                clauses.append({
                    "id": f"pg{page.number}_cl{clause_id}",
                    "text": clause.strip(),
                    "page": page.number,
                    "coords": page.get_text("dict")["blocks"][0]["bbox"] if page.get_text("dict")["blocks"] else None
                })
                clause_id += 1
    return clauses
