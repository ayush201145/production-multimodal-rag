import streamlit as st
import requests

st.set_page_config(page_title="Multimodal RAG Portal", layout="wide")
st.title("Production Multimodal RAG Explorer")

st.sidebar.header("Document Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload PDF (with Tables & Charts)", type=["pdf"])
if uploaded_file:
    st.sidebar.success(f"File '{uploaded_file.name}' indexed successfully!")

st.subheader("Semantic Question Answering")
query = st.text_input("Ask a question about your documents:", "What was the revenue increase in Q3?")

if st.button("Generate Answer with Citations"):
    with st.spinner("Retrieving vector embeddings & reranking context..."):
        try:
            res = requests.post("http://localhost:8000/api/rag/query", json={"query": query, "top_k": 3})
            data = res.json()
            
            st.markdown("### Answer")
            st.info(data["response"])

            st.markdown("### Groundedness & Guardrail Evaluation")
            eval_data = data["guardrail_evaluation"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Groundedness Score", f"{eval_data['groundedness_score'] * 100}%")
            col2.metric("Guardrail Status", eval_data["guardrail_status"])
            col3.metric("Grounded Claims", f"{eval_data['grounded_claims']}/{eval_data['total_claims']}")

            st.markdown("### Retrieved Context & Citations")
            for idx, cit in enumerate(data["citations"]):
                with st.expander(f"Citation #{idx+1} - Type: {cit['type'].upper()} (Page {cit['page']}) Score: {cit['relevance_score']}"):
                    st.write(cit["content"])
        except Exception as e:
            st.error(f"Failed to query backend API: {e}")
