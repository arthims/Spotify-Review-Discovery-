import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.models import UserPreferences
from backend.filter_engine import load_data, filter_restaurants
from llm.recommender import generate_recommendations

def run_test():
    print("Loading data...")
    df = load_data()
    
    prefs = UserPreferences(
        location="Bellandur",
        min_budget=0,
        max_budget=2000,
        min_rating=4.0,
        cuisines=[],
        additional_prefs="Please provide top 5 options."
    )
    
    print(f"Filtering data for Location: {prefs.location}, Budget: <={prefs.max_budget}, Rating: >={prefs.min_rating}")
    filtered_df = filter_restaurants(df, prefs, top_n=15)
    
    print(f"Found {len(filtered_df)} candidates. Sending to Groq LLM...")
    
    result = generate_recommendations(filtered_df, prefs.model_dump())
    
    print("\n--- LLM Response ---")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run_test()
