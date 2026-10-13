"""verifiable-rag API (FastAPI, Vercel serverless entry).

  GET  /api/questions   demo questions, each exercising a pipeline behavior
  POST /api/ask         {question} -> {naive: {...}, verifiable: {...}}
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.corpus import QUESTIONS
from rag.pipeline import ask

app = FastAPI(title="verifiable-rag")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


class AskBody(BaseModel):
    question: str


@app.get("/api/questions")
def questions() -> dict:
    return {"questions": QUESTIONS}


@app.post("/api/ask")
def ask_q(body: AskBody) -> dict:
    return ask(body.question.strip())


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "docs": len(__import__("rag.corpus", fromlist=["DOCS"]).DOCS),
            "mode": "demo (tf-idf + deterministic composer)"}
