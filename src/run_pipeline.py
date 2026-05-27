"""
Phase 1.7 - Local Pipeline Orchestrator

Runs the full Phase 1 ingestion pipeline locally in sequence.
This is the same pipeline that GitHub Actions runs on schedule,
but can be triggered manually for local development and testing.

Usage:
    python run_pipeline.py
"""

import subprocess
import sys
import os

PHASES = [
    {
        "name": "Phase 0 - Health Check",
        "dir": "phase0_config",
        "script": "health_check.py",
        "critical": True
    },
    {
        "name": "Phase 1.1 - Scrape URLs",
        "dir": os.path.join("phase1_ingestion", "phase1_1_scraping"),
        "script": "scraper.py",
        "critical": True
    },
    {
        "name": "Phase 1.2 - Parse & Clean HTML",
        "dir": os.path.join("phase1_ingestion", "phase1_2_parsing"),
        "script": "parser.py",
        "critical": True
    },
    {
        "name": "Phase 1.3 - Chunk Text",
        "dir": os.path.join("phase1_ingestion", "phase1_3_chunking"),
        "script": "chunker.py",
        "critical": True
    },
    {
        "name": "Phase 1.5 - BGE Embedding",
        "dir": os.path.join("phase1_ingestion", "phase1_5_embedding_bge"),
        "script": "embedder_bge.py",
        "critical": True
    },
    {
        "name": "Phase 1.6 - ChromaDB Ingest",
        "dir": os.path.join("phase1_ingestion", "phase1_6_chromadb"),
        "script": "chroma_ingest.py",
        "critical": True
    }
]

def run_phase(phase, src_dir):
    phase_dir = os.path.join(src_dir, phase["dir"])
    script_path = os.path.join(phase_dir, phase["script"])
    
    print(f"\n{'='*60}")
    print(f"  RUNNING: {phase['name']}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(script_path):
        print(f"[ERROR] Script not found: {script_path}")
        return False
        
    result = subprocess.run(
        [sys.executable, phase["script"]],
        cwd=phase_dir,
        capture_output=False
    )
    
    if result.returncode != 0:
        print(f"\n[FAILED] {phase['name']} exited with code {result.returncode}")
        return False
    
    print(f"\n[SUCCESS] {phase['name']} completed.")
    return True

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir)
    
    print("="*60)
    print("  MUTUAL FUND FAQ - FULL INGESTION PIPELINE")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for phase in PHASES:
        success = run_phase(phase, src_dir)
        if success:
            passed += 1
        else:
            failed += 1
            if phase["critical"]:
                print(f"\n[ABORT] Critical phase '{phase['name']}' failed. Stopping pipeline.")
                break
    
    print(f"\n{'='*60}")
    print(f"  PIPELINE SUMMARY: {passed} passed, {failed} failed out of {len(PHASES)} phases")
    print(f"{'='*60}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
