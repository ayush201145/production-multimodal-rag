from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from ingestion.multimodal_parser import MultimodalPDFParser
from retrieval.reranker import CrossEncoderReranker
from eval.guardrails import HallucinationGuardrail

app = FastAPI(
    title="Production Multimodal RAG System API",
    description="Vector retrieval with cross-encoder reranking, PDF table/chart parsing, and hallucination guardrail evaluation."
)

parser = MultimodalPDFParser()
reranker = CrossEncoderReranker()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/api/index")
async def index_pdf(file: UploadFile = File(...)):
    chunks = parser.parse_pdf(file.filename)
    return {
        "filename": file.filename,
        "indexed_chunks": len(chunks),
        "status": "SUCCESS"
    }

@app.post("/api/rag/query")
def rag_query(req: QueryRequest):
    # Simulated vector retrieval
    raw_docs = parser.parse_pdf("sample.pdf")
    
    # Apply Cross-Encoder Reranking
    reranked = reranker.rerank(req.query, raw_docs, top_k=req.top_k)

    # Generate Response with context
    context_str = "\n".join([f"[{d['type'].upper()} Page {d['page']}]: {d['content']}" for d in reranked])
    generated_response = f"Based on retrieved document context:\n{context_str}"

    # Evaluate Guardrails
    guardrail_eval = HallucinationGuardrail.evaluate_groundedness(req.query, generated_response, reranked)

    return {
        "query": req.query,
        "response": generated_response,
        "citations": reranked,
        "guardrail_evaluation": guardrail_eval
    }
