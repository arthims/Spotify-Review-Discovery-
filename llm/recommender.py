import os
import json
import pandas as pd
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Initializes the LLM. Expects GROQ_API_KEY in environment variables."""
    # Using Llama 3.3 on Groq for blazingly fast inference
    return ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

def format_restaurants_for_prompt(df: pd.DataFrame) -> str:
    """Converts the filtered DataFrame into a compact JSON string to save tokens."""
    if df.empty:
        return "[]"
    
    # Extract only the essential columns needed for reasoning
    essential_cols = [col for col in df.columns if col.lower() in [
        'name', 'restaurant name', 'city', 'location', 'cuisines', 'cuisine', 
        'cost', 'approx cost(for two people)', 'rate', 'rating', 'votes', 
        'listed_in(type)', 'rest_type', 'highlights'
    ]]
    
    compact_df = df[essential_cols] if essential_cols else df
    return compact_df.to_json(orient='records')

def generate_recommendations(filtered_df: pd.DataFrame, user_prefs: dict) -> Dict[str, Any]:
    """
    Takes the hard-filtered top restaurants and uses the Groq LLM to rank and explain them
    based on nuanced user preferences.
    """
    if filtered_df.empty:
        return {
            "summary": "No restaurants matched your exact criteria. Try broadening your search!",
            "recommendations": []
        }

    llm = get_llm()
    
    system_prompt = """
    You are an expert food critic and personalized restaurant concierge.
    You will be provided with a JSON list of top-rated restaurants that already match the user's basic budget and location filters.
    You will also be given the user's explicit preferences.
    
    Your task:
    1. Analyze the provided list of restaurants carefully.
    2. Select the top 3 to 5 absolute best options that perfectly match the user's preferences, especially paying attention to 'additional_prefs' and 'cuisines'.
    3. Rank them from 1 to N.
    4. Provide a compelling, human-like explanation for *why* each restaurant is a perfect fit based on the data.
    
    Output STRICTLY in valid JSON format with the following structure and NO markdown formatting wrappers (like ```json):
    {{
        "summary": "A short, engaging introductory sentence for the user.",
        "recommendations": [
            {{
                "rank": 1,
                "name": "Exact Restaurant Name from JSON",
                "explanation": "Why this is recommended based on user preferences."
            }}
        ]
    }}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "User Preferences:\n{preferences}\n\nAvailable Restaurants:\n{restaurants_json}")
    ])
    
    # JsonOutputParser ensures we get a nice dict out of the LLM
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    restaurants_json = format_restaurants_for_prompt(filtered_df)
    
    try:
        response = chain.invoke({
            "preferences": json.dumps(user_prefs),
            "restaurants_json": restaurants_json
        })
        return response
    except Exception as e:
        print(f"Error during Groq LLM invocation: {e}")
        # Graceful fallback to heuristics if the LLM fails or API key is missing
        fallback_recs = []
        for i, row in enumerate(filtered_df.head(3).to_dict('records')):
            name_col = next((c for c in row.keys() if 'name' in c.lower()), "Unknown")
            fallback_recs.append({
                "rank": i + 1,
                "name": row.get(name_col, "Unknown"),
                "explanation": "This is a top-rated match based on our local dataset filtering."
            })
        return {
            "summary": "Here are the top matches based on your filters (AI personalized explanations are currently unavailable).",
            "recommendations": fallback_recs
        }
