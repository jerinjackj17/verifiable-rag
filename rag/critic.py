"""The self-correction loop: critique, rewrite, abstain.

CRITIQUE: score each hit 0..1 as 0.6 * query-term coverage + 0.4 * retriever
score. Coverage = fraction of the query's content words appearing in the doc.
A doc can rank #1 on TF-IDF yet cover almost none of the actual question —
that is exactly the failure this catches.

REWRITE: if the best hit scores below REWRITE_THRESHOLD, expand the query
once: drop filler, expand known synonyms, and retry. One hop max — endless
rewriting is its own failure mode.

ABSTAIN: if the best hit is still below ABSTAIN_THRESHOLD after the rewrite,
return an explicit abstention. A confident wrong answer is worse than none.
"""
from __future__ import annotations

from .retrieve import Retriever, content_words

REWRITE_THRESHOLD = 0.45
ABSTAIN_THRESHOLD = 0.35
MAX_REWRITES = 1

# Small synonym map for the demo rewriter. A production rewriter would use
# an LLM; the pipeline doesn't care which.
SYNONYMS = {
    "cost": ["price", "pricing", "per"],
    "price": ["cost", "pricing"],
    "reset": ["rotation", "rotate", "revoke", "regenerate"],
    "key": ["api key", "token", "credentials"],
    "refund": ["cancel", "money back", "pro-rated"],
    "downtime": ["uptime", "sla", "outage", "credit"],
    "delete": ["remove", "purge"],
}


def critique(query: str, hits: list[dict]) -> list[dict]:
    """Attach a 0..1 grounding score to each hit. Mutates copies, not inputs."""
    qwords = set(content_words(query))
    out = []
    for h in hits:
        doc = h["doc"]
        dwords = set(content_words(doc["title"] + " " + doc["text"]))
        coverage = len(qwords & dwords) / max(1, len(qwords))
        score = round(0.6 * coverage + 0.4 * min(1.0, h["score"] * 3), 3)
        out.append({**h, "coverage": round(coverage, 3), "grounding": score,
                    "kept": score >= ABSTAIN_THRESHOLD})
    return out


def rewrite_query(query: str) -> str:
    """One deterministic rewrite hop: expand synonyms, drop filler."""
    words = content_words(query)
    expanded: list[str] = []
    for w in words:
        expanded.append(w)
        expanded.extend(SYNONYMS.get(w, []))
    # de-dup, keep order
    seen, uniq = set(), []
    for w in expanded:
        if w not in seen:
            seen.add(w)
            uniq.append(w)
    return " ".join(uniq)


def retrieve_with_correction(query: str, retriever: Retriever, k: int = 5) -> dict:
    """Full loop. Returns hits, trace of what happened, and the verdict."""
    trace: list[str] = [f"retrieve: {query!r}"]
    hits = critique(query, retriever.search(query, k))
    best = max((h["grounding"] for h in hits), default=0.0)
    trace.append(f"critique: best grounding {best:.2f} "
                 f"({sum(1 for h in hits if h['kept'])}/{len(hits)} kept)")

    rewrites = 0
    current_query = query
    while best < REWRITE_THRESHOLD and rewrites < MAX_REWRITES:
        rewrites += 1
        current_query = rewrite_query(current_query)
        trace.append(f"rewrite #{rewrites}: {current_query!r}")
        hits = critique(current_query, retriever.search(current_query, k))
        best = max((h["grounding"] for h in hits), default=0.0)
        trace.append(f"critique: best grounding {best:.2f}")

    kept = [h for h in hits if h["kept"]]
    verdict = "answer" if best >= ABSTAIN_THRESHOLD else "abstain"
    if verdict == "abstain":
        trace.append(f"abstain: grounding {best:.2f} < {ABSTAIN_THRESHOLD} — "
                     "refusing to guess")
    return {"hits": hits, "kept": kept, "best": round(best, 3),
            "rewrites": rewrites, "final_query": current_query,
            "verdict": verdict, "trace": trace}
