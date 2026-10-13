import { useEffect, useState } from "react";
import { api, type Answer, type Question } from "./api";
import "./styles.css";

function confClass(c: string) {
  if (c === "high") return "bad";
  if (c === "grounded") return "good";
  if (c === "abstained") return "abstain";
  return "warn";
}

function Panel({ title, a, accent }: { title: string; a: Answer; accent?: boolean }) {
  return (
    <div className={`panel ${accent ? "accent" : ""}`}>
      <div className="panel-head">
        <h3>{title}</h3>
        <span className={`conf ${confClass(a.confidence)}`}>{a.confidence}</span>
      </div>
      <p className="answer">{a.answer}</p>
      <p className="cites">
        {a.citations.length > 0 ? (
          <>cited: {a.citations.map((c) => <code key={c}>{c}</code>)}</>
        ) : (
          <>no citations — nothing grounded enough to cite</>
        )}
      </p>
      {a.grounding != null && (
        <p className="meta">grounding score: <b>{a.grounding.toFixed(2)}</b>
          {a.rewrites ? <> · query rewritten {a.rewrites}×</> : null}</p>
      )}
      {a.rewrites ? <p className="meta">final query: <code>{a.final_query}</code></p> : null}
      <details>
        <summary>retrieved docs ({a.retrieved.length})</summary>
        <table className="calls">
          <thead><tr><th>doc</th><th>title</th><th>grounding</th><th>kept</th></tr></thead>
          <tbody>
            {a.retrieved.map((h) => (
              <tr key={h.id} className={h.kept === false ? "dropped" : ""}>
                <td><code>{h.id}</code></td>
                <td>{h.title}</td>
                <td>{h.grounding != null ? h.grounding.toFixed(2) : (h.score ?? 0).toFixed(2)}</td>
                <td>{h.kept == null ? "—" : h.kept ? "yes" : "no"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
      <details>
        <summary>trace</summary>
        <pre className="trace">{a.trace.join("\n")}</pre>
      </details>
    </div>
  );
}

export default function App() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [custom, setCustom] = useState("");
  const [result, setResult] = useState<{ question: string; naive: Answer; verifiable: Answer } | null>(null);
  const [busy, setBusy] = useState(false);
  const [activeQ, setActiveQ] = useState("");

  useEffect(() => {
    api.questions().then((q) => setQuestions(q.questions)).catch(() => {});
  }, []);

  const ask = async (q: string) => {
    if (!q.trim()) return;
    setBusy(true);
    setActiveQ(q);
    try {
      setResult(await api.ask(q));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="page">
      <header>
        <div>
          <h1>verifiable-rag</h1>
          <p className="sub">a RAG pipeline that critiques its hits, rewrites weak queries, and abstains when grounding is thin</p>
        </div>
      </header>

      <section>
        <h2>ask something</h2>
        <div className="qgrid">
          {questions.map((q) => (
            <button key={q.id} className={`q ${activeQ === q.q ? "sel" : ""}`} disabled={busy}
              onClick={() => ask(q.q)} title={q.expect}>
              <strong>{q.label}</strong><span>{q.q}</span>
            </button>
          ))}
        </div>
        <div className="custom">
          <input value={custom} onChange={(e) => setCustom(e.target.value)}
            placeholder="or ask your own question about Acme Cloud…" disabled={busy}
            onKeyDown={(e) => { if (e.key === "Enter") ask(custom); }} />
          <button className="go" disabled={busy} onClick={() => ask(custom)}>ask</button>
        </div>
        <p className="hint">hover a question to see what behavior it exercises · the corpus is 30 synthetic Acme Cloud docs</p>
      </section>

      {result && (
        <section className="cols">
          <Panel title="naive RAG — top hit, always confident" a={result.naive} />
          <Panel title="verifiable RAG — critique · rewrite · abstain" a={result.verifiable} accent />
        </section>
      )}

      <section className="how">
        <h2>how the verifiable pipeline works</h2>
        <ol>
          <li><b>retrieve</b> — TF-IDF + cosine over the corpus (swap in embeddings via the Retriever protocol).</li>
          <li><b>critique</b> — score each hit: 60% query-term coverage + 40% retriever score. Drop the weak ones.</li>
          <li><b>rewrite</b> — best hit under 0.45? Expand synonyms, drop filler, retrieve once more.</li>
          <li><b>abstain</b> — still under 0.35? Say so explicitly instead of hallucinating.</li>
        </ol>
      </section>

      <footer>
        <p>verifiable-rag · pure-python tf-idf · deterministic demo, zero api keys · <a href="https://github.com/jerinjackj17/verifiable-rag">github</a></p>
      </footer>
    </div>
  );
}
