import sys
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add directories to system path for modular imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "..", "phase3_generation"))
sys.path.append(os.path.join(current_dir, "..", "phase2_retrieval"))

from generator import generate_response
from pii_filter import contains_pii, redact_pii
from middleware import RateLimitingMiddleware, StrictLoggingMiddleware, logger

app = FastAPI(title="Mutual Fund FAQ Assistant API", version="1.0.0")

# Enable CORS for cross-origin local requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middlewares for Rate Limiting and PII-Safe Logging
app.add_middleware(RateLimitingMiddleware, limit=30, window=60)
app.add_middleware(StrictLoggingMiddleware)

class ChatRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "app": "Mutual Fund FAQ Assistant"}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Main chat Q&A endpoint.
    Checks for PII, classifies query, retrieves context, and generates answer.
    """
    query_text = request.query.strip()
    
    # 1. PII Security Check
    if contains_pii(query_text):
        redacted_query = redact_pii(query_text)
        logger.warning(f"PII Blocked | Query: {redacted_query}")
        return {
            "query": query_text,
            "status": "refused",
            "response": "Privacy Warning: Your query contains Personal Identifiable Information (PII) like phone numbers or emails. We do not process PII to ensure privacy. Please query again without sharing personal details.",
            "source_url": None,
            "footer": "Privacy & Security guardrails active."
        }
        
    # Log sanitized query
    logger.info(f"Query: {query_text}")
    
    try:
        # Run Phase 3 generation pipeline
        response_data = generate_response(query_text)
        return response_data
    except Exception as e:
        logger.exception("Error executing chat pipeline")
        raise HTTPException(status_code=500, detail=f"Internal Pipeline Error: {str(e)}")

# Mount frontend files
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phase4_frontend"))

if os.path.exists(FRONTEND_DIR):
    # Route for serving main SPA index.html
    @app.get("/")
    def read_root():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
        
    # Mount files under static
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
else:
    logger.error(f"Frontend directory not found at {FRONTEND_DIR}")
