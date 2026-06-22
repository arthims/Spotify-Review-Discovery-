"""
Subphase 2c & 2d: Query Embedding + Metadata-Filtered Vector Search

Embeds the user query using BGE (with the required query prefix)
and searches ChromaDB with optional scheme_id filtering.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

# BGE query prefix (required for asymmetric retrieval)
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# Singleton model loader
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    return _model


def get_chroma_collection():
    """Initialize ChromaDB client and return the mutual_fund_schemes collection."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_db_dir = os.path.join(script_dir, "..", "data", "chroma_db")
    
    client = chromadb.PersistentClient(path=chroma_db_dir)
    collection = client.get_collection(name="mutual_fund_schemes")
    return collection


def embed_query(query: str) -> list:
    """
    Embed the user query using BGE with the required query prefix.
    Returns a normalized embedding vector.
    """
    model = get_model()
    prefixed_query = BGE_QUERY_PREFIX + query
    embedding = model.encode(prefixed_query, normalize_embeddings=True)
    return embedding.tolist()


def search(query: str, scheme_id: str = None, top_k: int = 3) -> list:
    """
    Perform metadata-filtered semantic search against ChromaDB.
    
    Args:
        query: The user's factual question
        scheme_id: Optional scheme_id to filter results (from Subphase 2b)
        top_k: Number of top results to return
        
    Returns:
        List of dicts, each containing:
            - chunk_id, text, scheme_id, url, last_updated, distance
    """
    collection = get_chroma_collection()
    query_embedding = embed_query(query)
    
    # Build query params
    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }
    
    # Apply metadata filter if scheme was identified
    if scheme_id:
        query_params["where"] = {"scheme_id": scheme_id}
    
    results = collection.query(**query_params)
    
    # Format results
    formatted = []
    for i in range(len(results["ids"][0])):
        formatted.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "scheme_id": results["metadatas"][0][i].get("scheme_id"),
            "url": results["metadatas"][0][i].get("url"),
            "last_updated": results["metadatas"][0][i].get("last_updated"),
            "distance": results["distances"][0][i]
        })
    
    return formatted


if __name__ == "__main__":
    # Quick test
    test_query = "What is the expense ratio of HDFC Mid Cap fund?"
    test_scheme = "hdfc-mid-cap-opportunities-fund"
    
    print("Subphase 2c+2d: Query Embedding & Vector Search Test\n")
    
    print(f"Query: \"{test_query}\"")
    print(f"Filter: scheme_id = {test_scheme}\n")
    
    results = search(test_query, scheme_id=test_scheme, top_k=3)
    
    for i, r in enumerate(results):
        print(f"--- Result {i+1} (distance: {r['distance']:.4f}) ---")
        print(f"Chunk: {r['chunk_id']}")
        print(f"Text: {r['text'][:200]}...")
        print(f"URL: {r['url']}")
        print()
