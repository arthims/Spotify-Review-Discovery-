import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def run_embedder_bge():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chunked_dir = os.path.join(script_dir, "..", "..", "data", "chunked")
    index_dir = os.path.join(script_dir, "..", "..", "data", "index")
    
    os.makedirs(index_dir, exist_ok=True)
    
    if not os.path.exists(chunked_dir):
        print(f"Error: Chunked directory not found at {chunked_dir}")
        return
        
    json_files = [f for f in os.listdir(chunked_dir) if f.endswith(".json")]
    
    print("Loading model 'BAAI/bge-small-en-v1.5' (this may download model weights the first time)...")
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    
    all_chunks = []
    
    for json_file in json_files:
        file_path = os.path.join(chunked_dir, json_file)
        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
            
    print(f"\nStarting Phase 1.5: Embedding {len(all_chunks)} chunks with BGE model...")
    
    # For passage embedding in BGE, we don't need any special prefixes. 
    # (The prefix 'Represent this sentence for searching relevant passages: ' is only used for QUERIES)
    texts = [chunk['text'] for chunk in all_chunks]
    
    # Generate embeddings and normalize them (standard practice for BGE models to use cosine similarity via dot product)
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    
    # Save embeddings to numpy array
    embeddings_path = os.path.join(index_dir, "embeddings_bge.npy")
    np.save(embeddings_path, embeddings)
    
    # Save metadata specifically for BGE (though it's the exact same chunks)
    metadata_path = os.path.join(index_dir, "metadata_bge.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)
        
    print(f"\nEmbedding complete. Generated optimized vectors with shape: {embeddings.shape}")
    print(f"Saved BGE embeddings to: {os.path.abspath(embeddings_path)}")
    print(f"Saved BGE metadata to: {os.path.abspath(metadata_path)}")

if __name__ == "__main__":
    run_embedder_bge()
