"""
Subphase 2b: Scheme Entity Extraction

Extracts mutual fund scheme references from user queries
and maps them to the known scheme IDs in our config.
"""

import json
import os

# Scheme aliases: maps common references to the canonical scheme_id
SCHEME_ALIASES = {
    "hdfc-mid-cap-opportunities-fund": [
        "mid cap", "mid-cap", "midcap", "mid cap opportunities",
        "hdfc mid cap", "hdfc midcap", "hdfc mid-cap"
    ],
    "hdfc-flexi-cap-fund": [
        "flexi cap", "flexi-cap", "flexicap", "equity fund",
        "hdfc flexi cap", "hdfc flexicap", "hdfc equity"
    ],
    "hdfc-focused-30-fund": [
        "focused", "focused 30", "focused fund", "hdfc focused",
        "hdfc focused 30"
    ],
    "hdfc-elss-tax-saver-fund": [
        "elss", "tax saver", "tax saving", "hdfc elss",
        "hdfc tax saver", "tax fund", "elss fund"
    ],
    "hdfc-top-100-fund": [
        "large cap", "large-cap", "largecap", "top 100",
        "hdfc large cap", "hdfc largecap", "hdfc top 100"
    ]
}


def load_scheme_urls():
    """Load scheme URLs from config for metadata enrichment."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "phase0_config", "config.json")
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return {s["id"]: s["url"] for s in config["target_schemes"]}
    except FileNotFoundError:
        return {}


def extract_scheme(query: str) -> dict:
    """
    Extracts the scheme_id from a user query using fuzzy alias matching.
    
    Returns:
        dict with keys:
            - scheme_id: the matched scheme ID or None
            - scheme_url: the Groww URL for the matched scheme or None
            - matched_alias: the alias string that was matched or None
    """
    query_lower = query.lower().strip()
    scheme_urls = load_scheme_urls()
    
    # Sort aliases by length (longest first) to match most specific alias
    best_match = None
    best_alias = None
    best_length = 0
    
    for scheme_id, aliases in SCHEME_ALIASES.items():
        for alias in aliases:
            if alias in query_lower and len(alias) > best_length:
                best_match = scheme_id
                best_alias = alias
                best_length = len(alias)
    
    if best_match:
        return {
            "scheme_id": best_match,
            "scheme_url": scheme_urls.get(best_match),
            "matched_alias": best_alias
        }
    
    return {
        "scheme_id": None,
        "scheme_url": None,
        "matched_alias": None
    }


if __name__ == "__main__":
    test_queries = [
        "What is the expense ratio of HDFC Mid Cap fund?",
        "What is the exit load for ELSS?",
        "Tell me about the focused 30 fund",
        "What is the minimum SIP for large cap?",
        "What is the lock-in period?",
        "HDFC flexi cap NAV",
    ]
    
    print("Subphase 2b: Scheme Entity Extraction Test\n")
    for q in test_queries:
        result = extract_scheme(q)
        if result["scheme_id"]:
            print(f"[MATCHED] \"{q}\" → {result['scheme_id']} (via '{result['matched_alias']}')")
        else:
            print(f"[NO MATCH] \"{q}\" → Will search all schemes")
    print()
