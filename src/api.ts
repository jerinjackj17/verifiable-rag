export interface Hit {
  id: string;
  title: string;
  score?: number;
  retriever_score?: number;
  coverage?: number;
  grounding?: number;
  kept?: boolean;
}

export interface Answer {
  mode: string;
  answer: string;
  citations: string[];
  confidence: string;
  grounding?: number;
  rewrites?: number;
  final_query?: string;
  retrieved: Hit[];
  trace: string[];
}

export interface Question {
  id: string;
  label: string;
  q: string;
  expect: string;
}

async function j<T>(r: Response): Promise<T> {
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

export const api = {
  questions: () => fetch("/api/questions").then((r) => j<{ questions: Question[] }>(r)),
  ask: (question: string) =>
    fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    }).then((r) => j<{ question: string; naive: Answer; verifiable: Answer }>(r)),
};
