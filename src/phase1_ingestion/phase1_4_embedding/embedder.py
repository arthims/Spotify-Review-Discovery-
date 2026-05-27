import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def run_embedder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chunked_dir = os.path.join(script_dir, "..", "..", "data", "chunked")
    index_dir = os.path.join(script_dir, "..", "..", "data", "index")
    
    os.makedirs(index_dir, exist_ok=True)
    
    if not os.path.exists(chunked_dir):
        print(f"Error: Chunked directory not found at {chunked_dir}")
        return
        
    json_files = [f for f in os.listdir(chunked_dir) if f.endswith(".json")]
    
    print("Loading model 'all-MiniLM-L6-v2' (this may download model weights the first time)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    all_chunks = []
    
    for json_file in json_files:
        file_path = os.path.join(chunked_dir, json_file)
        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
            
    print(f"\nStarting Subphase 1d: Embedding {len(all_chunks)} chunks...")
    
    texts = [chunk['text'] for chunk in all_chunks]
    
    # Generate embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Save embeddings to numpy array
    embeddings_path = os.path.join(index_dir, "embeddings.npy")
    np.save(embeddings_path, embeddings)
    
    # Save metadata (the chunks themselves contain all necessary metadata + text)
    metadata_path = os.path.join(index_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)
        
    print(f"\nEmbedding complete. Generated vectors with shape: {embeddings.shape}")
    print(f"Saved embeddings to: {os.path.abspath(embeddings_path)}")
    print(f"Saved metadata to: {os.path.abspath(metadata_path)}")

if __name__ == "__main__":
    run_embedder()
