"""
FastAPI application for markdown-based Q&A.

Endpoints
---------
POST /upload
    Upload a markdown file.  The content replaces any previously uploaded document.

POST /ask
    Ask a question about the currently uploaded document.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

from app.qa_engine import QAEngine

app = FastAPI(
    title="Markdown Q&A API",
    description=(
        "Upload a markdown file and ask questions about its content. "
        "The API reads the document and returns the most relevant sections as the answer."
    ),
    version="1.0.0",
)

# Shared in-memory engine instance
_engine = QAEngine()


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3


class UploadResponse(BaseModel):
    message: str
    chunks_loaded: int


class AnswerResponse(BaseModel):
    question: str
    answer: str
    source_chunks: list[int]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/upload", response_model=UploadResponse, summary="Upload a markdown file")
async def upload_markdown(file: UploadFile = File(...)):
    """
    Upload a **markdown (.md)** file.

    The file content is parsed and stored in memory.  Any previously uploaded
    document is replaced.  After uploading, use `POST /ask` to ask questions.
    """
    if not file.filename or not file.filename.lower().endswith(".md"):
        raise HTTPException(
            status_code=400,
            detail="Only markdown files (.md) are accepted.",
        )

    raw_bytes = await file.read()
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="The file could not be decoded as UTF-8.",
        )

    if not content.strip():
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    chunks = _engine.load(content)
    return UploadResponse(
        message=f"Document '{file.filename}' loaded successfully.",
        chunks_loaded=chunks,
    )


@app.post("/ask", response_model=AnswerResponse, summary="Ask a question about the uploaded document")
async def ask_question(body: QuestionRequest):
    """
    Ask a **natural-language question** about the previously uploaded markdown document.

    The API locates the most relevant sections of the document using TF-IDF
    similarity and returns them as the answer.

    - **question**: The question you want answered.
    - **top_k**: Number of most-relevant chunks to include in the answer (default 3).
    """
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    if body.top_k < 1 or body.top_k > 20:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 20.")

    result = _engine.answer(body.question, top_k=body.top_k)
    return AnswerResponse(
        question=body.question,
        answer=result["answer"],
        source_chunks=result["source_chunks"],
    )


@app.get("/health", summary="Health check")
async def health():
    """Returns the current status of the service and whether a document is loaded."""
    return {
        "status": "ok",
        "document_loaded": _engine.is_loaded,
    }
