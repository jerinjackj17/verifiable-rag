"""Answer composers: naive baseline vs the verifiable pipeline.

Both are extractive and deterministic in demo mode — the comparison is about
*decision logic*, not model quality:

NAIVE: take the top TF-IDF hit, quote its first two sentences, cite it,
always sound confident. This is what ships in most tutorials, and it is
exactly how you get a confident answer to a question the docs never address.

VERIFIABLE: run retrieve_with_correction. Answer only from kept hits, cite
every claim, and abstain when grounding is weak. The abstention is the feature.
"""
from __future__ import annotations

import re

from .corpus import DOCS, QUESTIONS
from .critic import retrieve_with_correction
from .retrieve import TfidfRetriever, content_words

_retriever: TfidfRetriever | None = None


def get_retriever() -> TfidfRetriever:
    global _retriever
    if _retriever is None:
        _retriever = TfidfRetriever(DOCS)
    return _retriever


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def _extract_answer(query: str, docs: list[dict], max_sentences: int = 3) -> tuple[str, list[str]]:
    """Pick the sentences with the most query-term overlap. Returns (text, [doc_ids])."""
    qwords = set(content_words(query))
    scored = []
    for d in docs:
        for s in _sentences(d["text"]):
            overlap = len(qwords & set(content_words(s)))
            scored.append((overlap, s, d["id"]))
    scored.sort(key=lambda t: t[0], reverse=True)
    picked = [s for s in scored if s[0] > 0][:max_sentences]
    if not picked:
        picked = scored[:1]
    cites = sorted({doc_id for _, _, doc_id in picked})
    text = " ".join(s for _, s, _ in picked)
    return text, cites


def naive_ask(question: str) -> dict:
    """The tutorial baseline: top hit, first two sentences, full confidence."""
    hits = get_retriever().search(question, k=1)
    doc = hits[0]["doc"]
    sents = _sentences(doc["text"])[:2]
    return {
        "mode": "naive",
        "answer": " ".join(sents),
        "citations": [doc["id"]],
        "confidence": "high",  # always. that is the bug.
        "retrieved": [{"id": doc["id"], "title": doc["title"],
                       "score": hits[0]["score"]}],
        "trace": [f"took top TF-IDF hit ({doc['id']}, "
                  f"score {hits[0]['score']}) and answered confidently"],
    }


def verifiable_ask(question: str) -> dict:
    """The self-correcting pipeline."""
    res = retrieve_with_correction(question, get_retriever(), k=5)
    if res["verdict"] == "abstain":
        return {
            "mode": "verifiable",
            "answer": ("I don't have enough grounded information to answer that. "
                       "Nothing in the docs covers it with confidence, so I'm "
                       "abstaining rather than guessing."),
            "citations": [],
            "confidence": "abstained",
            "grounding": res["best"],
            "rewrites": res["rewrites"],
            "final_query": res["final_query"],
            "retrieved": [
                {"id": h["doc"]["id"], "title": h["doc"]["title"],
                 "retriever_score": h["score"], "coverage": h["coverage"],
                 "grounding": h["grounding"], "kept": h["kept"]}
                for h in res["hits"]
            ],
            "trace": res["trace"],
        }
    kept_docs = [h["doc"] for h in res["kept"]][:3]
    text, cites = _extract_answer(res["final_query"], kept_docs)
    return {
        "mode": "verifiable",
        "answer": text,
        "citations": cites,
        "confidence": "grounded" if res["best"] >= 0.6 else "low",
        "grounding": res["best"],
        "rewrites": res["rewrites"],
        "final_query": res["final_query"],
        "retrieved": [
            {"id": h["doc"]["id"], "title": h["doc"]["title"],
             "retriever_score": h["score"], "coverage": h["coverage"],
             "grounding": h["grounding"], "kept": h["kept"]}
            for h in res["hits"]
        ],
        "trace": res["trace"],
    }


def ask(question: str) -> dict:
    return {"question": question,
            "naive": naive_ask(question),
            "verifiable": verifiable_ask(question)}
