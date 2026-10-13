"""verifiable-rag: a RAG pipeline that knows when it doesn't know.

Naive chunk-and-retrieve answers confidently from whatever came back,
even when it's irrelevant. This pipeline adds three self-correction steps:

  1. CRITIQUE — score every retrieved hit for query-term coverage and
     relevance; drop the weak ones instead of stuffing them into context.
  2. REWRITE — if nothing scores well, rewrite the query (expand synonyms,
     drop filler) and retrieve again. One rewrite hop max.
  3. ABSTAIN — if grounding is still weak, say so explicitly rather than
     hallucinate. "I don't have enough grounded information" is a feature.

Demo mode (default) uses a pure-Python TF-IDF retriever and a deterministic
answer composer — zero API keys, zero network. The Retriever and Generator
are protocols: plug in embeddings + an LLM via env vars without touching
the pipeline logic.
"""
