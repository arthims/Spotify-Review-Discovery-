import time
import logging
import os
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pii_filter import redact_pii

# Set up logging directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "backend.log")

# Configure logger
logger = logging.getLogger("MF_FAQ_Backend")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Lightweight in-memory rate limiting middleware.
    Limits clients to 20 requests per minute by default.
    """
    def __init__(self, app, limit: int = 20, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = {} # ip -> list of timestamps

    async def dispatch(self, request: Request, call_next):
        # We only rate limit API endpoints
        if not request.url.path.startswith("/api/"):
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean up old timestamps
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < self.window]
        else:
            self.requests[client_ip] = []
            
        # Check limit
        if len(self.requests[client_ip]) >= self.limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please wait a moment before trying again."}
            )
            
        # Record request
        self.requests[client_ip].append(now)
        return await call_next(request)

class StrictLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests while ensuring PII is redacted.
    """
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        
        # Process request
        start_time = time.time()
        
        # If it is the chat API, we will log the query (redacted)
        # Note: reading body inside middleware can be tricky, so we do query logging in the route handler instead
        # but we still log request info here.
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        logger.info(f"IP: {client_ip} | {method} {path} | Status: {response.status_code} | Time: {process_time:.2f}ms")
        
        return response
