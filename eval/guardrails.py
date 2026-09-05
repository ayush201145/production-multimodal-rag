from typing import List, Dict

class HallucinationGuardrail:
    @staticmethod
    def evaluate_groundedness(query: str, response: str, context_chunks: List[Dict]) -> Dict:
        context_text = " ".join([c.get("content", "") for c in context_chunks])
        
        # Check claim overlap with retrieved context
        claims = [s.strip() for s in response.split(".") if s.strip()]
        grounded_claims = 0

        for claim in claims:
            # Check if key tokens in claim appear in context
            tokens = [t for t in claim.lower().split() if len(t) > 3]
            match_count = sum(1 for t in tokens if t in context_text.lower())
            if tokens and (match_count / len(tokens)) > 0.4:
                grounded_claims += 1

        groundedness_score = round(grounded_claims / max(len(claims), 1), 2)
        passed = groundedness_score >= 0.7

        return {
            "groundedness_score": groundedness_score,
            "passed": passed,
            "total_claims": len(claims),
            "grounded_claims": grounded_claims,
            "guardrail_status": "PASSED" if passed else "FLAGGED_HALLUCINATION"
        }
