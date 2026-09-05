# Production-Ready Multimodal RAG (Retrieval-Augmented Generation) System

Vector search, hybrid retrieval, PDF table/chart chunking, cross-encoder semantic reranking, citations, and automated hallucination-guardrail evaluations served via FastAPI & Streamlit UI.

## Architecture
```
[ Multimodal PDF Ingestion ] -> [ Chunk & Embedding Indexing ]
                                          |
[ User Query ] -> [ Hybrid Retrieval ] -> [ Cross-Encoder Reranker ]
                                          |
                                          v
                              [ LLM Response Generation ]
                                          |
                              [ Hallucination Guardrail ] -> Pass / Flag
```

## Features
- **Multimodal Document Parsing**: Table Markdown conversion, chart caption extraction, and text chunking.
- **Cross-Encoder Reranking**: Re-orders vector search hits according to query context alignment.
- **Hallucination Guardrails**: Evaluates response groundedness against retrieved source chunks before outputting to the user.
- **Streamlit Interactive UI**: Built-in visual dashboard displaying groundedness scores, citation source cards, and query controls.

## Quick Start

### Local Execution
```bash
pip install -r requirements.txt
# Terminal 1: API backend
uvicorn app:app --port 8000
# Terminal 2: Streamlit Dashboard
streamlit run streamlit_ui.py
```

## Tech Stack
- **Framework**: Python 3.11, FastAPI, Streamlit
- **Vector DB / Search**: ChromaDB / Sentence-Transformers
- **Reranker**: Cross-Encoder (MiniLM)
- **Guardrails**: Automated Claim Groundedness Assessor
