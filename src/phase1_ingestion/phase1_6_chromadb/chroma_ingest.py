import os
import json
import numpy as np
import chromadb

def run_chroma_ingest():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(script_dir, "..", "..", "data", "index")
    chroma_db_dir = os.path.join(script_dir, "..", "..", "data", "chroma_db")
    
    os.makedirs(chroma_db_dir, exist_ok=True)
    
    metadata_path = os.path.join(index_dir, "metadata_bge.json")
    embeddings_path = os.path.join(index_dir, "embeddings_bge.npy")
    
    if not os.path.exists(metadata_path) or not os.path.exists(embeddings_path):
        print("Error: BGE metadata or embeddings not found. Please run Phase 1.5 first.")
        return
        
    with open(metadata_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    embeddings = np.load(embeddings_path)
    
    print(f"Starting Phase 1.6: Ingesting {len(chunks)} chunks into ChromaDB...")
    
    # Initialize ChromaDB persistent client
    client = chromadb.PersistentClient(path=chroma_db_dir)
    
    collection_name = "mutual_fund_schemes"
    
    # Delete if exists to ensure a clean, idempotent ingest
    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection: {collection_name}")
    except Exception:
        pass
        
    # Create collection configured for cosine similarity (optimal for normalized BGE embeddings)
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Prepare data arrays for ChromaDB
    ids = [chunk['chunk_id'] for chunk in chunks]
    documents = [chunk['text'] for chunk in chunks]
    metadatas = [{"scheme_id": chunk['scheme_id'], "url": chunk['url'], "last_updated": chunk['last_updated']} for chunk in chunks]
    embeddings_list = embeddings.tolist()
    
    print("Writing data to database...")
    # Add to collection
    collection.add(
        ids=ids,
        embeddings=embeddings_list,
        metadatas=metadatas,
        documents=documents
    )
    
    print(f"\nIngestion complete. Added {collection.count()} documents to ChromaDB collection '{collection_name}'.")
    print(f"ChromaDB persistent storage saved to: {os.path.abspath(chroma_db_dir)}")

if __name__ == "__main__":
    run_chroma_ingest()
