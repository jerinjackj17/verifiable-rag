"""Retrieval: pure-Python TF-IDF + cosine similarity. Zero dependencies.

This is deliberately the *boring* part. The research contribution of this
project is the critique/rewrite/abstain loop around retrieval, not the
retriever itself. The Retriever protocol lets you swap in embeddings
(HF, OpenAI) without touching the pipeline.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Protocol

WORD_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


STOP = frozenset(
    "a an the and or of to in on for with is are was were be been it its "
    "this that these those i you he she we they my your his her our their "
    "do does did how what when where which who whom why can could should "
    "would will just than then so such no not me".split()
)


def content_words(text: str) -> list[str]:
    return [w for w in tokenize(text) if w not in STOP and len(w) > 2]


class Retriever(Protocol):
    def search(self, query: str, k: int = 5) -> list[dict]: ...


class TfidfRetriever:
    """TF-IDF over the corpus, cosine similarity. Built once, queried often."""

    def __init__(self, docs: list[dict]):
        self.docs = docs
        self._doc_terms = [Counter(tokenize(d["title"] + " " + d["text"])) for d in docs]
        df: Counter = Counter()
        for terms in self._doc_terms:
            for t in terms:
                df[t] += 1
        n = len(docs)
        self._idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
        self._doc_vecs = [self._vec(terms) for terms in self._doc_terms]

    def _vec(self, terms: Counter) -> dict[str, float]:
        total = sum(terms.values()) or 1
        return {t: (c / total) * self._idf.get(t, 1.0) for t, c in terms.items()}

    @staticmethod
    def _cos(a: dict[str, float], b: dict[str, float]) -> float:
        dot = sum(a[t] * b.get(t, 0.0) for t in a)
        na = math.sqrt(sum(v * v for v in a.values())) or 1
        nb = math.sqrt(sum(v * v for v in b.values())) or 1
        return dot / (na * nb)

    def search(self, query: str, k: int = 5) -> list[dict]:
        qv = self._vec(Counter(tokenize(query)))
        scored = [
            {"doc": doc, "score": round(self._cos(qv, dv), 4)}
            for doc, dv in zip(self.docs, self._doc_vecs)
        ]
        scored.sort(key=lambda h: h["score"], reverse=True)
        return scored[:k]
