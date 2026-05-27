import os
import json

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def naive_text_chunker(text, chunk_size=1000, overlap=100):
    """
    Splits text into chunks of `chunk_size` characters (~250 tokens), 
    with a slight overlap. Tries to split on paragraphs to preserve context.
    """
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if not para.strip():
            continue
            
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n"
        else:
            # If current chunk is not empty, save it
            if current_chunk:
                chunks.append(current_chunk.strip())
                
            # Handle extremely long single paragraphs
            if len(para) > chunk_size:
                for i in range(0, len(para), chunk_size - overlap):
                    chunks.append(para[i:i+chunk_size])
                current_chunk = ""
            else:
                current_chunk = para + "\n"
                
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def run_chunker():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_dir = os.path.join(script_dir, "..", "..", "data", "cleaned")
    chunked_dir = os.path.join(script_dir, "..", "..", "data", "chunked")
    
    os.makedirs(chunked_dir, exist_ok=True)
    
    if not os.path.exists(cleaned_dir):
        print(f"Error: Cleaned directory not found at {cleaned_dir}")
        return
        
    json_files = [f for f in os.listdir(cleaned_dir) if f.endswith(".json")]
    
    print(f"Starting Subphase 1c: Chunking {len(json_files)} cleaned files...\n")
    
    success_count = 0
    total_chunks = 0
    
    for json_file in json_files:
        file_path = os.path.join(cleaned_dir, json_file)
        data = load_json(file_path)
        
        text = data.get("text", "")
        # Approx 1000 chars ~ 250 tokens
        chunks = naive_text_chunker(text, chunk_size=1000, overlap=100)
        
        chunk_data = []
        for idx, chunk in enumerate(chunks):
            chunk_data.append({
                "chunk_id": f"{data['id']}-chunk-{idx}",
                "scheme_id": data["id"],
                "url": data["url"],
                "last_updated": data["last_updated"],
                "text": chunk
            })
            
        output_file = os.path.join(chunked_dir, json_file)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, indent=4)
            
        print(f"[OK] Chunked {data['id']}: generated {len(chunks)} chunks.")
        success_count += 1
        total_chunks += len(chunks)
        
    print(f"\nChunking complete. Successfully processed {success_count} files into {total_chunks} total chunks.")
    print(f"Chunked data saved to: {os.path.abspath(chunked_dir)}")

if __name__ == "__main__":
    run_chunker()
