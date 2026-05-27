import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script, style, nav, header, footer elements to reduce noise
    for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
        element.decompose()
        
    # Attempt to extract text from the body
    text = soup.get_text(separator='\n', strip=True)
    
    # Simple cleaning: remove multiple newlines
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
    return cleaned_text

def run_parser():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "..", "phase0_config", "config.json")
    raw_dir = os.path.join(script_dir, "..", "..", "data", "raw")
    cleaned_dir = os.path.join(script_dir, "..", "..", "data", "cleaned")
    
    os.makedirs(cleaned_dir, exist_ok=True)
    
    config = load_config(config_path)
    schemes = config.get("target_schemes", [])
    
    print(f"Starting Subphase 1b: Parsing and Cleaning {len(schemes)} HTML files...\n")
    
    success_count = 0
    for scheme in schemes:
        scheme_id = scheme["id"]
        url = scheme["url"]
        
        raw_file = os.path.join(raw_dir, f"{scheme_id}.html")
        if not os.path.exists(raw_file):
            print(f"[SKIPPED] Missing raw file for {scheme_id}")
            continue
            
        with open(raw_file, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()
            
        cleaned_text = clean_html(html_content)
        
        # Save as JSON with metadata
        output_data = {
            "id": scheme_id,
            "url": url,
            "last_updated": datetime.now().isoformat(), # Fallback if explicit date is missing
            "text": cleaned_text
        }
        
        cleaned_file = os.path.join(cleaned_dir, f"{scheme_id}.json")
        with open(cleaned_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)
            
        print(f"[OK] Parsed and cleaned: {scheme_id}.json")
        success_count += 1
        
    print(f"\nParsing complete. Successfully cleaned {success_count}/{len(schemes)} files.")
    print(f"Cleaned JSON files saved to: {os.path.abspath(cleaned_dir)}")

if __name__ == "__main__":
    run_parser()
