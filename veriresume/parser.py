from io import BytesIO

def extract_text(data: bytes, filename: str) -> str:
    name = filename.lower()
    if name.endswith(".txt"):
        return data.decode("utf-8", errors="replace")
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install requirements.txt to enable PDF support.") from exc
        reader = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("Install requirements.txt to enable DOCX support.") from exc
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type. Upload PDF, DOCX or TXT.")
