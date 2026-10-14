# verifiable-rag

A retrieval pipeline built around one belief: a confident wrong answer is
worse than no answer. Most RAG demos take the top chunk and answer confidently
no matter what. This one critiques its own hits, rewrites weak queries, and
abstains when the grounding is thin.

Live demo: https://verifiable-rag-rho.vercel.app

## The side-by-side

Same corpus, same retriever. The only difference is the decision logic.

| Question | Naive RAG | This pipeline |
|---|---|---|
| How much does the Pro plan cost? | cites the wrong doc, confident | cites pricing-01, grounded |
| How do I reset it? | answers about workspaces | rewrites, finds the API key rotation doc |
| 2021 enterprise refund policy? | confidently cites the wrong policy | low confidence, related citations only |
| CEO's favorite color? | confident nonsense | abstains |
| Uptime SLA and downtime credits? | correct | correct, grounded |

## How it works

1. **Critique.** Every hit gets a grounding score: 60% query-term coverage,
   40% retriever score. A doc can rank first on TF-IDF while covering almost
   none of the actual question. That is exactly the failure this catches. Weak
   hits get dropped, not stuffed into context.
2. **Rewrite.** Best hit under 0.45 and the query gets one rewrite hop:
   synonyms expanded, filler dropped, retrieve again. One hop max. Endless
   rewriting is its own failure mode.
3. **Abstain.** Still under 0.35 after the rewrite and the pipeline says so
   out loud instead of hallucinating.

## Run it

```bash
pip install -r requirements.txt
uvicorn api.index:app --port 8000
npm install && npm run dev   # UI on :5173, proxies /api
```

Or skip the servers:

```bash
python - <<'EOF'
from rag.pipeline import ask
r = ask("What was the enterprise refund policy for contracts signed in 2021?")
print(r["naive"]["answer"][:120])
print(r["verifiable"]["answer"][:120])
EOF
```

Deploy: push to `main`. Vercel builds the UI and serves `api/index.py`.

## Limits, stated plainly

* Retrieval is TF-IDF, not embeddings. It works because the corpus is small
  and the questions are lexical. On a real corpus you would plug in vectors;
  the `Retriever` protocol exists for exactly that.
* The rewriter is a synonym map, not an LLM. The pipeline treats it as a
  black box: one hop, then decide.
* The thresholds (0.45 rewrite, 0.35 abstain) were tuned by hand on the 5
  demo questions below, not on a benchmark. In production you would tune the
  abstain decision on a labeled eval set and report "when it answers, how
  often is it right" instead of answer rate.

## Eval (the tuning set, all 5 of them)

| Question | Naive | Verifiable |
|---|---|---|
| Pro plan cost | wrong doc, high confidence | correct, grounded |
| "How do I reset it?" | nonsense answer | rewrite, correct doc |
| 2021 enterprise refunds | wrong policy, high confidence | low confidence, related cites |
| CEO's favorite color | confident nonsense | abstains |
| Uptime SLA + credits | correct | correct, grounded |

## Layout

```
rag/              corpus.py (30 synthetic docs), retrieve.py (TF-IDF),
                  critic.py (critique, rewrite, abstain), pipeline.py
api/index.py      FastAPI: GET /api/questions, POST /api/ask
src/              React UI: naive vs verifiable, side by side
docs/ADR-001.md   why abstention is a feature, not a failure mode
INTERVIEW.md      how I explain this in 60 seconds
```
