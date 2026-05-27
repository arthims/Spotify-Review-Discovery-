import json
import urllib.request
import urllib.error
import os

def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def check_url(url):
    # Use a standard user-agent to avoid immediate 403 blocks from simple bot protection
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    try:
        response = urllib.request.urlopen(req, timeout=10)
        return response.getcode() == 200
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def run_health_check():
    # Resolve paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    
    try:
        config = load_config(config_path)
    except FileNotFoundError:
        print(f"Error: Could not find config file at {config_path}")
        return

    urls = [item['url'] for item in config.get('target_schemes', [])]
    
    if not urls:
        print("No URLs found in configuration.")
        return

    print("Running Phase 0 Health Check on Target URLs...\n")
    all_healthy = True
    
    for url in urls:
        print(f"Checking: {url}")
        is_healthy = check_url(url)
        if is_healthy:
            print("Status: [OK]\n")
        else:
            print("Status: [FAILED]\n")
            all_healthy = False
            
    print("-" * 50)
    if all_healthy:
        print("Result: PASS - All target URLs are accessible.")
    else:
        print("Result: FAIL - One or more target URLs failed accessibility check.")

if __name__ == "__main__":
    run_health_check()
