"""
Mutual Fund FAQ Assistant - Backend Runner
Loads environment variables and spins up the FastAPI application with Uvicorn.
"""
import sys
import os
import uvicorn
from dotenv import load_dotenv

# Load env variables from root directory .env file
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

if __name__ == "__main__":
    # Ensure src directory is in path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("  STARTING MUTUAL FUND FAQ ASSISTANT API SERVER")
    print("=" * 60)
    print("Server Address: http://localhost:8000")
    print("API docs:        http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)
    
    # Run the Uvicorn server referencing the phase4_backend package
    uvicorn.run("phase4_backend.api:app", host="localhost", port=8000, reload=True)
