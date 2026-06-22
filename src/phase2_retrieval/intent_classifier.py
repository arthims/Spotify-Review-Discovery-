"""
Subphase 2a: Intent Classification & Guardrails (Refusal Handling)

Classifies user queries as either 'factual' or 'advisory'.
Advisory queries are refused with a polite message and educational link.
"""

import re

# Keywords and patterns that indicate advisory/subjective intent
ADVISORY_KEYWORDS = [
    "should i", "recommend", "suggest", "advice", "advise",
    "worth it", "good idea", "bad idea", "opinion",
    "which is better", "which one", "which fund",
    "best fund", "worst fund", "top fund",
    "better than", "worse than", "compare",
    "outperform", "underperform",
    "will it grow", "will it fall", "predict",
    "guaranteed", "safe investment", "risk free",
    "buy", "sell", "hold",
    "invest in", "put money in",
    "how much return", "expected return", "future return"
]

ADVISORY_PATTERNS = [
    r"\bshould\b.*\b(invest|buy|sell|switch|redeem)\b",
    r"\b(best|better|worst|top|safest)\b.*\b(fund|scheme|option)\b",
    r"\b(compare|comparison|vs|versus)\b",
    r"\bwhich\b.*\b(fund|scheme|one|better)\b",
    r"\b(predict|forecast|expect)\b.*\b(return|growth|performance)\b",
]

REFUSAL_RESPONSE = {
    "answer": "I appreciate your question, but I'm designed to provide only factual information about mutual fund schemes — not investment advice or recommendations. For personalized guidance, please consult a SEBI-registered financial advisor.",
    "source_url": "https://www.amfiindia.com/investor-corner/knowledge-center/what-are-mutual-funds.html",
    "disclaimer": "Facts-only. No investment advice."
}


def classify_intent(query: str) -> dict:
    """
    Classifies the user's query as 'factual' or 'advisory'.
    
    Returns:
        dict with keys:
            - intent: 'factual' or 'advisory'
            - refusal_response: None if factual, else the refusal dict
    """
    query_lower = query.lower().strip()
    
    # Check against keyword list
    for keyword in ADVISORY_KEYWORDS:
        if keyword in query_lower:
            return {
                "intent": "advisory",
                "refusal_response": REFUSAL_RESPONSE
            }
    
    # Check against regex patterns
    for pattern in ADVISORY_PATTERNS:
        if re.search(pattern, query_lower):
            return {
                "intent": "advisory",
                "refusal_response": REFUSAL_RESPONSE
            }
    
    return {
        "intent": "factual",
        "refusal_response": None
    }


if __name__ == "__main__":
    # Quick test
    test_queries = [
        "What is the expense ratio of HDFC Mid-Cap Fund?",
        "Should I invest in HDFC ELSS?",
        "What is the exit load?",
        "Which fund is better - HDFC Mid Cap or HDFC Flexi Cap?",
        "What is the minimum SIP amount?",
        "Will this fund give good returns?",
        "What is the lock-in period for ELSS?",
        "Recommend a good fund for me",
    ]
    
    print("Subphase 2a: Intent Classification Test\n")
    for q in test_queries:
        result = classify_intent(q)
        status = "REFUSED" if result["intent"] == "advisory" else "ALLOWED"
        print(f"[{status}] \"{q}\"")
    print()
