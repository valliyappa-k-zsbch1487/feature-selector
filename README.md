# feature-selector

A FastAPI-based service that lets you upload a Markdown (`.md`) file and then ask natural-language questions about its content.  Questions are answered by finding the most relevant sections of the document using **TF-IDF cosine similarity** — no external LLM or internet connection required.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/upload` | Upload a `.md` file. Replaces any previously loaded document. |
| `POST` | `/ask` | Ask a question about the uploaded document. |
| `GET` | `/health` | Check service status and whether a document is loaded. |

### `POST /upload`

Upload a markdown file using `multipart/form-data`.

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@my-document.md"
```

**Response**

```json
{
  "message": "Document 'my-document.md' loaded successfully.",
  "chunks_loaded": 5
}
```

### `POST /ask`

Ask a question about the uploaded document.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What Python version is required?", "top_k": 2}'
```

**Request body**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `question` | `string` | required | The question to ask |
| `top_k` | `integer` | `3` | Number of most-relevant chunks to include in the answer (1–20) |

**Response**

```json
{
  "question": "What Python version is required?",
  "answer": "## FAQ\n\n**Q: What Python version is required?**\nA: Python 3.10 or higher.",
  "source_chunks": [3]
}
```

---

## Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

The interactive API docs (Swagger UI) are available at <http://localhost:8000/docs>.

---

## Running tests

```bash
pytest tests/ -v
```
