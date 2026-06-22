"""
Phase 3: Generation & Formatting

Takes the output from Phase 2 (Query Processing & Retrieval)
and generates a constraint-bound response using an LLM.
Handles post-processing (citations, footers) and unknown answer scenarios.
"""
import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the phase2 directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase2_retrieval"))
from query_pipeline import process_query

SYSTEM_PROMPT = """You are a strict, facts-only mutual fund assistant.
Answer using ONLY the provided context.
If the context does not contain the answer, state exactly: 'I do not know the answer based on the provided context'.
Do not provide financial advice, opinions, or performance comparisons.
Never ask for, process, or include any Personal Identifiable Information (PII).
Limit your response to a maximum of 3 sentences."""

UNKNOWN_STRING = "I do not know the answer based on the provided context"

def generate_llm_response(query: str, context_chunks: list) -> str:
    """
    Calls the Groq API (Llama-3) to generate an answer.
    If GROQ_API_KEY is not set in the environment, it falls back to a mock for local testing.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    combined_context = "\n\n".join([f"--- Chunk ---\n{c['text']}" for c in context_chunks])
    
    if not groq_api_key:
        # --- MOCK FALLBACK (for testing without API key) ---
        query_lower = query.lower()
        combined_lower = combined_context.lower()
        if "expense ratio" in query_lower and "expense ratio" in combined_lower:
            return "The expense ratio for this fund is explicitly mentioned in the document. It is currently at 1.45%."
        elif "exit load" in query_lower and "exit load" in combined_lower:
            return "An exit load of 1% is applicable if units are redeemed within 1 year from the date of allotment."
        elif "sip" in query_lower and "minimum sip" in combined_lower:
            return "The minimum SIP investment for this scheme is set to ₹100."
        return UNKNOWN_STRING

    # --- ACTUAL GROQ INTEGRATION ---
    from groq import Groq
    client = Groq(api_key=groq_api_key)
    
    user_prompt = f"Context Information:\n{combined_context}\n\nUser Query: {query}\n\nAnswer strictly based on the context above."
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0, # 0.0 for maximum factual determinism
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()

def generate_response(query: str) -> dict:
    """
    Runs Phase 2 to get context, then Phase 3 to generate the final response.
    """
    phase2_result = process_query(query)
    
    # 1. Handle Advisory queries (Refusal)
    if phase2_result["intent"] == "advisory":
        return {
            "query": query,
            "status": "refused",
            "response": phase2_result["refusal_response"]["answer"],
            "source_url": phase2_result["refusal_response"]["source_url"],
            "footer": phase2_result["refusal_response"]["disclaimer"]
        }
        
    # 2. Factual Query: Retrieve chunks
    chunks = phase2_result["results"]
    if not chunks:
        # Should rarely happen with vector search, but handled just in case
        return {
            "query": query,
            "status": "unknown",
            "response": UNKNOWN_STRING,
            "source_url": None,
            "footer": None
        }
        
    # 3. LLM Inference
    llm_output = generate_llm_response(query, chunks)
    
    # 4. Post-Processing & Citations
    if UNKNOWN_STRING in llm_output:
        # Constraint: If unknown, NO URL is attached.
        return {
            "query": query,
            "status": "unknown",
            "response": llm_output,
            "source_url": None,
            "footer": None
        }
        
    # If the LLM successfully answered, attach the primary source link and footer
    # We take the metadata from the top retrieved chunk
    top_chunk = chunks[0]
    
    return {
        "query": query,
        "status": "success",
        "response": llm_output,
        "source_url": top_chunk["url"],
        "footer": f"Last updated from sources: {top_chunk['last_updated']}"
    }

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))

if __name__ == "__main__":
    test_queries = [
        "What is the expense ratio of HDFC Mid Cap fund?",
        "Should I invest in this fund?",
        "What is the exit load for the focused fund?",
        "What is the name of the fund manager's pet dog?", # Deliberately unknown scenario
    ]
    
    safe_print("=" * 60)
    safe_print("  PHASE 3: GENERATION & FORMATTING - FULL TEST")
    safe_print("=" * 60)
    
    for q in test_queries:
        safe_print(f"\n{'-'*60}")
        safe_print(f"Query: \"{q}\"")
        
        final_result = generate_response(q)
        
        safe_print(f"Status: {final_result['status'].upper()}")
        safe_print(f"Response: {final_result['response']}")
        
        if final_result['source_url']:
            safe_print(f"Source: {final_result['source_url']}")
        else:
            safe_print("Source: None (Intentionally omitted)")
            
        if final_result['footer']:
            safe_print(f"Footer: {final_result['footer']}")
            
    safe_print(f"\n{'='*60}")
    safe_print("  TEST COMPLETE")
    safe_print(f"{'='*60}")
