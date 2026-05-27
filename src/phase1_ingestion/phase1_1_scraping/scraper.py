import json
import os
import urllib.request
import urllib.error

def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

def fetch_and_save_html(url, scheme_id, output_dir):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        response = urllib.request.urlopen(req, timeout=15)
        html_content = response.read()
        
        output_file = os.path.join(output_dir, f"{scheme_id}.html")
        with open(output_file, "wb") as f:
            f.write(html_content)
        
        print(f"[OK] Fetched and saved: {scheme_id}.html")
        return True
    except urllib.error.URLError as e:
        print(f"[FAILED] Error fetching {url}: {e.reason}")
        return False
    except Exception as e:
        print(f"[FAILED] Unexpected error for {url}: {e}")
        return False

def run_scraper():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "..", "phase0_config", "config.json")
    output_dir = os.path.join(script_dir, "..", "..", "data", "raw")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading configuration from {config_path}")
    try:
        config = load_config(config_path)
    except FileNotFoundError:
        print("Config file not found. Please ensure Phase 0 config exists.")
        return
        
    schemes = config.get("target_schemes", [])
    if not schemes:
        print("No schemes found in config.")
        return
        
    print(f"Starting Subphase 1a: Scraping {len(schemes)} target URLs...\n")
    
    success_count = 0
    for scheme in schemes:
        url = scheme["url"]
        scheme_id = scheme["id"]
        if fetch_and_save_html(url, scheme_id, output_dir):
            success_count += 1
            
    print(f"\nScraping complete. Successfully fetched {success_count}/{len(schemes)} URLs.")
    print(f"Raw HTML files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    run_scraper()
