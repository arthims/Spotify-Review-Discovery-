import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add root project dir to path to import from backend and llm modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserPreferences
from backend.filter_engine import load_data, filter_restaurants
from llm.recommender import generate_recommendations

app = FastAPI(title="AI Restaurant Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development (Next.js will call this)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Preload data on startup to save time during requests
try:
    df = load_data()
    print(f"Loaded dataset with {len(df)} rows.")
except Exception as e:
    print(f"Warning: Could not load data on startup: {e}")
    df = None

@app.get("/health")
def health_check():
    return {"status": "ok", "data_loaded": df is not None}

@app.post("/recommendations")
def get_recommendations(prefs: UserPreferences):
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded. Ensure data ingestion has run.")
        
    try:
        # Phase 2: Hard Filtering
        filtered_df = filter_restaurants(df, prefs, top_n=15)
        
        if filtered_df.empty:
            return {
                "summary": "No restaurants matched your exact criteria. Try broadening your search!",
                "recommendations": []
            }
            
        # Phase 3: LLM Recommender
        prefs_dict = prefs.model_dump()
        result = generate_recommendations(filtered_df, prefs_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {e}")
