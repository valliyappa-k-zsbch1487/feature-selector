"""
Tests for the Markdown Q&A API (app/main.py) and QA engine (app/qa_engine.py).
"""
import io
import pytest
from fastapi.testclient import TestClient

from app.main import app, _engine

client = TestClient(app)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SAMPLE_MD = """\
# Introduction

This document describes the feature-selector project.
The project is written in Python and uses FastAPI.

# Installation

To install the project run:

```
pip install -r requirements.txt
```

# Usage

Start the server with:

```
uvicorn app.main:app --reload
```

Then upload a markdown file and ask questions about it.

# FAQ

**Q: What Python version is required?**
A: Python 3.10 or higher is required.

**Q: What file formats are supported?**
A: Only markdown (.md) files are supported.
"""


def _upload_sample(filename: str = "sample.md", content: str = SAMPLE_MD):
    return client.post(
        "/upload",
        files={"file": (filename, io.BytesIO(content.encode()), "text/markdown")},
    )


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

def test_health_no_document():
    # Reset the engine so the health check reflects "no document loaded"
    _engine._chunks = []
    _engine._plain_chunks = []
    _engine._idf = {}
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["document_loaded"] is False


def test_health_with_document():
    _upload_sample()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["document_loaded"] is True


# ---------------------------------------------------------------------------
# POST /upload
# ---------------------------------------------------------------------------

def test_upload_valid_md():
    resp = _upload_sample()
    assert resp.status_code == 200
    data = resp.json()
    assert "loaded successfully" in data["message"]
    assert data["chunks_loaded"] > 0


def test_upload_non_md_extension_rejected():
    resp = client.post(
        "/upload",
        files={"file": ("notes.txt", io.BytesIO(b"some text"), "text/plain")},
    )
    assert resp.status_code == 400
    assert "markdown" in resp.json()["detail"].lower()


def test_upload_empty_file_rejected():
    resp = client.post(
        "/upload",
        files={"file": ("empty.md", io.BytesIO(b"   "), "text/markdown")},
    )
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_upload_replaces_previous_document():
    _upload_sample(content="# Doc A\nContent A.")
    _upload_sample(content="# Doc B\nContent B.")
    resp = client.post("/ask", json={"question": "Content B"})
    assert resp.status_code == 200
    assert "Content B" in resp.json()["answer"]


# ---------------------------------------------------------------------------
# POST /ask
# ---------------------------------------------------------------------------

def test_ask_before_upload_returns_no_document_message():
    # Reset engine
    _engine._chunks = []
    _engine._plain_chunks = []
    _engine._idf = {}
    resp = client.post("/ask", json={"question": "What is this about?"})
    assert resp.status_code == 200
    assert "No document" in resp.json()["answer"]


def test_ask_installation_question():
    _upload_sample()
    resp = client.post("/ask", json={"question": "How do I install the project?"})
    assert resp.status_code == 200
    data = resp.json()
    # The answer should mention pip or requirements
    assert "pip" in data["answer"] or "requirements" in data["answer"]


def test_ask_python_version_question():
    _upload_sample()
    resp = client.post("/ask", json={"question": "What Python version is required?"})
    assert resp.status_code == 200
    assert "3.10" in resp.json()["answer"]


def test_ask_file_formats_question():
    _upload_sample()
    resp = client.post("/ask", json={"question": "What file formats are supported?"})
    assert resp.status_code == 200
    assert "markdown" in resp.json()["answer"].lower() or ".md" in resp.json()["answer"]


def test_ask_empty_question_rejected():
    _upload_sample()
    resp = client.post("/ask", json={"question": "   "})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_ask_top_k_out_of_range():
    _upload_sample()
    resp = client.post("/ask", json={"question": "test", "top_k": 25})
    assert resp.status_code == 400


def test_ask_returns_source_chunks():
    _upload_sample()
    resp = client.post("/ask", json={"question": "start the server"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["source_chunks"], list)


def test_ask_top_k_limits_chunks():
    _upload_sample()
    resp = client.post("/ask", json={"question": "Python", "top_k": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["source_chunks"]) <= 1


# ---------------------------------------------------------------------------
# QA Engine unit tests
# ---------------------------------------------------------------------------

from app.qa_engine import QAEngine, _tokenize, _strip_markdown, _split_into_chunks


def test_tokenize():
    assert _tokenize("Hello, World! 123") == ["hello", "world", "123"]


def test_strip_markdown_removes_headings_markers():
    result = _strip_markdown("## My Heading\nsome text")
    assert "##" not in result
    assert "My Heading" in result


def test_strip_markdown_removes_code_fences():
    result = _strip_markdown("```python\nprint('hi')\n```")
    assert "```" not in result


def test_split_into_chunks_by_headings():
    md = "# Section 1\nContent 1.\n\n# Section 2\nContent 2."
    chunks = _split_into_chunks(md)
    assert len(chunks) == 2
    assert "Section 1" in chunks[0]
    assert "Section 2" in chunks[1]


def test_split_into_chunks_fallback_paragraphs():
    md = "Paragraph one.\n\nParagraph two."
    chunks = _split_into_chunks(md)
    assert len(chunks) == 2


def test_engine_load_and_answer():
    engine = QAEngine()
    engine.load("# Fruits\nApples and oranges are fruits.\n\n# Vegetables\nCarrots are vegetables.")
    result = engine.answer("What are some fruits?")
    assert "Fruits" in result["answer"] or "apple" in result["answer"].lower()


def test_engine_no_relevant_content():
    engine = QAEngine()
    engine.load("# Topic\nThis document is about cars.")
    # Use a completely fabricated term that cannot appear in the document
    result = engine.answer("zzzzzz xqxqxq fabricated8472 unrelated99")
    # Should gracefully say it couldn't find info
    assert "could not find" in result["answer"].lower() or len(result["source_chunks"]) == 0
