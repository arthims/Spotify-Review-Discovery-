"""
Phase 2: Query Processing & Retrieval - Pipeline

Orchestrates the full Phase 2 pipeline:
  Subphase 2a: Intent Classification
  Subphase 2b: Scheme Entity Extraction
  Subphase 2c: Query Embedding (BGE with prefix)
  Subphase 2d: Metadata-Filtered Vector Search
"""

from intent_classifier import classify_intent
from scheme_extractor import extract_scheme
from retriever import search


def process_query(query: str) -> dict:
    """
    Full Phase 2 pipeline: classify intent, extract scheme, retrieve context.
    
    Returns:
        dict with keys:
            - query: original query
            - intent: 'factual' or 'advisory'
            - refusal_response: refusal dict if advisory, else None
            - scheme: extracted scheme info
            - results: list of retrieved chunks (empty if advisory)
    """
    # Step 1: Intent Classification (Subphase 2a)
    intent_result = classify_intent(query)
    
    if intent_result["intent"] == "advisory":
        return {
            "query": query,
            "intent": "advisory",
            "refusal_response": intent_result["refusal_response"],
            "scheme": None,
            "results": []
        }
    
    # Step 2: Scheme Entity Extraction (Subphase 2b)
    scheme_result = extract_scheme(query)
    
    # Step 3 & 4: Query Embedding + Vector Search (Subphase 2c + 2d)
    results = search(
        query=query,
        scheme_id=scheme_result["scheme_id"],
        top_k=3
    )
    
    return {
        "query": query,
        "intent": "factual",
        "refusal_response": None,
        "scheme": scheme_result,
        "results": results
    }


def safe_print(text):
    """Print with fallback for Unicode characters that can't be encoded on Windows console."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))


if __name__ == "__main__":
    test_queries = [
        "What is the expense ratio of HDFC Mid Cap fund?",
        "Should I invest in HDFC ELSS?",
        "What is the exit load for the focused fund?",
        "Which fund is better for tax saving?",
        "What is the minimum SIP amount for large cap?",
        "What is the lock-in period for ELSS?",
        "What is the benchmark index?",
    ]
    
    safe_print("=" * 60)
    safe_print("  PHASE 2: QUERY PROCESSING & RETRIEVAL - FULL TEST")
    safe_print("=" * 60)
    
    for q in test_queries:
        safe_print(f"\n{'-'*60}")
        safe_print(f"Query: \"{q}\"")
        
        result = process_query(q)
        
        if result["intent"] == "advisory":
            safe_print(f"Intent: ADVISORY (REFUSED)")
            safe_print(f"Response: {result['refusal_response']['answer']}")
        else:
            scheme_info = result["scheme"]
            if scheme_info and scheme_info["scheme_id"]:
                safe_print(f"Intent: FACTUAL | Scheme: {scheme_info['scheme_id']} (via '{scheme_info['matched_alias']}')")
            else:
                safe_print(f"Intent: FACTUAL | Scheme: None (searching all)")
            
            safe_print(f"Top {len(result['results'])} results:")
            for i, r in enumerate(result["results"]):
                safe_print(f"  [{i+1}] (dist: {r['distance']:.4f}) {r['chunk_id']}")
                safe_print(f"      {r['text'][:120]}...")
    
    safe_print(f"\n{'='*60}")
    safe_print("  TEST COMPLETE")
    safe_print(f"{'='*60}")
