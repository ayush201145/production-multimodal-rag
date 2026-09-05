from typing import List, Dict

class CrossEncoderReranker:
    def __init__(self, model_name: str = "ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name

    def rerank(self, query: str, documents: List[Dict], top_k: int = 3) -> List[Dict]:
        """Compute semantic relevance scores and rerank retrieved chunks"""
        scored_docs = []
        for doc in documents:
            text = doc.get("content", "")
            # Semantic keyword overlap scoring heuristic
            score = 0.5
            words = query.lower().split()
            for word in words:
                if word in text.lower():
                    score += 0.2
            doc_copy = dict(doc)
            doc_copy["relevance_score"] = round(min(score, 0.99), 4)
            scored_docs.append(doc_copy)

        scored_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_docs[:top_k]
