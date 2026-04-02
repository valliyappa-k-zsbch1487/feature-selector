"""
Q&A engine that finds answers in a markdown document using TF-IDF text similarity.
"""
import re
import math
from collections import Counter
from typing import Optional


def _tokenize(text: str) -> list[str]:
    """Lowercase and split text into word tokens, stripping punctuation."""
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def _strip_markdown(text: str) -> str:
    """Remove common markdown syntax to get plain text."""
    # Remove code fences
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r"`[^`]{1,2000}`", " ", text)
    # Remove links [text](url) — bounded lengths prevent ReDoS
    text = re.sub(r"\[([^\]]{1,1000})\]\([^\)\s]{1,2000}\)", r"\1", text)
    # Remove images ![alt](url) — bounded lengths prevent ReDoS
    text = re.sub(r"!\[[^\]]{0,1000}\]\([^\)\s]{1,2000}\)", " ", text)
    # Remove headings markers but keep heading text
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r"[*_]{1,3}([^*_]{1,2000})[*_]{1,3}", r"\1", text)
    # Remove horizontal rules
    text = re.sub(r"^\s*[-*_]{3,}\s*$", " ", text, flags=re.MULTILINE)
    # Remove HTML tags — bounded length prevents ReDoS
    text = re.sub(r"<[^>]{1,500}>", " ", text)
    return text


def _split_into_chunks(markdown_text: str) -> list[str]:
    """
    Split a markdown document into logical chunks.

    Chunks are created at each heading boundary.  If there are no headings,
    the document is split into paragraphs.  Empty chunks are discarded.
    """
    # Split on lines that start with a '#' heading
    heading_chunks = re.split(r"(?m)^(?=#{1,6}\s)", markdown_text)
    heading_chunks = [c.strip() for c in heading_chunks if c.strip()]

    # Only use heading-based split when multiple headings were actually found
    if len(heading_chunks) > 1:
        chunks = heading_chunks
    else:
        # Fallback: split on blank lines (paragraphs)
        chunks = [p.strip() for p in re.split(r"\n\s*\n", markdown_text) if p.strip()]
        if not chunks:
            chunks = heading_chunks

    return chunks


class QAEngine:
    """In-memory Q&A engine backed by a single markdown document."""

    def __init__(self) -> None:
        self._chunks: list[str] = []
        self._plain_chunks: list[str] = []
        self._idf: dict[str, float] = {}

    # ------------------------------------------------------------------
    # Document management
    # ------------------------------------------------------------------

    def load(self, markdown_text: str) -> int:
        """Load (or replace) the current document.  Returns the number of chunks."""
        self._chunks = _split_into_chunks(markdown_text)
        self._plain_chunks = [_strip_markdown(c) for c in self._chunks]
        self._idf = self._compute_idf(self._plain_chunks)
        return len(self._chunks)

    @property
    def is_loaded(self) -> bool:
        return bool(self._chunks)

    # ------------------------------------------------------------------
    # Q&A
    # ------------------------------------------------------------------

    def answer(self, question: str, top_k: int = 3) -> dict:
        """
        Return an answer for *question* based on the loaded document.

        Strategy:
        1. Rank all chunks by TF-IDF cosine similarity to the question.
        2. Return the top-k most relevant chunks as the answer context.
        """
        if not self.is_loaded:
            return {
                "answer": "No document has been loaded yet.  Please upload a markdown file first.",
                "source_chunks": [],
            }

        question_plain = _strip_markdown(question)
        question_tokens = _tokenize(question_plain)
        q_tf = Counter(question_tokens)

        scores: list[tuple[float, int]] = []
        for idx, chunk_plain in enumerate(self._plain_chunks):
            score = self._cosine_similarity(q_tf, _tokenize(chunk_plain))
            scores.append((score, idx))

        scores.sort(key=lambda x: x[0], reverse=True)
        top_indices = [idx for _, idx in scores[:top_k] if scores[0][0] > 0]

        if not top_indices:
            return {
                "answer": "I could not find relevant information in the document to answer your question.",
                "source_chunks": [],
            }

        answer_parts = [self._chunks[i] for i in top_indices]
        return {
            "answer": "\n\n---\n\n".join(answer_parts),
            "source_chunks": top_indices,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_idf(corpus: list[str]) -> dict[str, float]:
        n = len(corpus)
        if n == 0:
            return {}
        doc_freq: Counter = Counter()
        for doc in corpus:
            for token in set(_tokenize(doc)):
                doc_freq[token] += 1
        return {token: math.log((n + 1) / (freq + 1)) + 1 for token, freq in doc_freq.items()}

    def _tfidf_vector(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        return {
            token: (count / total) * self._idf.get(token, 1.0)
            for token, count in tf.items()
        }

    def _cosine_similarity(self, q_tf: Counter, doc_tokens: list[str]) -> float:
        if not doc_tokens:
            return 0.0
        q_vec = self._tfidf_vector(list(q_tf.elements()))
        d_vec = self._tfidf_vector(doc_tokens)
        dot = sum(q_vec.get(t, 0) * d_vec.get(t, 0) for t in q_vec)
        q_norm = math.sqrt(sum(v ** 2 for v in q_vec.values())) or 1e-9
        d_norm = math.sqrt(sum(v ** 2 for v in d_vec.values())) or 1e-9
        return dot / (q_norm * d_norm)
