# verifiable-rag, in 60 seconds

verifiable-rag is a retrieval pipeline built around one belief: a confident
wrong answer is worse than no answer. Most RAG demos take the top chunk and
answer confidently no matter what. Mine adds a self-correction loop with
three steps.

First, critique. Every retrieved hit gets a grounding score: sixty percent
query-term coverage, forty percent retriever score. A doc can rank first on
TF-IDF while covering almost none of the actual question, and that is exactly
the failure this catches. Weak hits get dropped, not stuffed into context.

Second, rewrite. If nothing scores above 0.45, the query gets one rewrite
hop: synonyms expanded, filler dropped, retrieve again. One hop max, because
endless rewriting is its own failure mode.

Third, abstain. Still under 0.35 after the rewrite, and the pipeline says so
out loud instead of hallucinating. The demo runs it side by side against
naive RAG. Ask about the CEO's favorite color and the naive one answers
confidently from a random doc while mine abstains. Ask something ambiguous
like how do I reset it and the rewrite finds the API key rotation doc.

Honest limits: the demo uses TF-IDF, not embeddings, and a synonym map, not
an LLM rewriter. The pipeline treats both as swappable black boxes, which is
the actual architecture. And the thresholds were tuned on five demo
questions, not a benchmark. In production you would tune the abstain decision
on a labeled eval set. That tradeoff is in the ADR.
