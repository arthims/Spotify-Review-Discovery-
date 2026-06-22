# Phase-Wise Architecture: AI-Powered Review Discovery & MVP
This document outlines the end-to-end architecture for addressing the Spotify music discovery challenge, breaking it down into four distinct phases as outlined in the problem statement.
## Phase 1: AI-Powered Review Discovery Engine
**Goal:** Ingest user feedback at scale from diverse sources and extract actionable insights using LLMs.
---
### 1. Data Ingestion Layer
*   **Sources:**
    *   **Reddit:** Subreddits like `r/spotify`, `r/truespotify`, `r/Music` using the `praw` API.
    *   **App Stores:** Apple App Store and Google Play Store reviews using `google-play-scraper` and `app-store-scraper`.
    *   **Community Forums/Social Media:** Twitter/X mentions or Spotify Community forums.
*   **Ingestion Tooling:** 
    *   Python scripts scheduled via a lightweight orchestrator (e.g., cron, or an n8n workflow).
### 2. Data Processing & Storage Layer
*   **Preprocessing:** Clean HTML, remove PII, and filter for reviews that mention keywords related to "recommendations," "discovery," "algorithm," "repetitive," "bored," etc.
*   **Storage:** 
    *   **Raw Data:** Stored in a SQLite/PostgreSQL database or simple JSON lines.
### 3. AI Analysis Layer
*   **LLM Pipeline (e.g., using OpenAI GPT-4o or Claude 3.5 Sonnet):**
    *   Pass batches of reviews into the LLM with a structured prompt.
    *   **Task:** Perform Topic Modeling, Sentiment Analysis, and Intent Classification.
    *   **Outputs:** JSON structures answering the core questions:
        *   *Frustrations* (e.g., "Algorithm gets stuck in a loop").
        *   *Behaviors* (e.g., "Users create new playlists just to force new recommendations").
*   **Workflow Engine:** Optional use of **n8n** or **Zapier** to route new reviews directly to the LLM and append the structured JSON to a Google Sheet or database.
### 4. Dashboard (Insight Consumption)
*   **UI:** A lightweight **Streamlit** or **Gradio** app displaying:
    *   Aggregated themes of unmet needs.
    *   Semantic search bar over historical complaints.
## Phase 2: Validate the Opportunity Through User Research
**Goal:** Take LLM-generated hypotheses and validate them with primary human research.
### 1. Research Preparation
*   **AI-Assisted Guide Creation:** Use the insights from Phase 1 to automatically generate an interview script using an LLM.
*   **Screener:** Target users who have high engagement but low discovery diversity.
### 2. Interview & Transcription
*   **Transcription:** Record interviews and pass the audio through **OpenAI Whisper** for high-accuracy text transcription.
### 3. Synthesis
*   **LLM Summarization:** Feed the 5-6 transcripts into an LLM context window to extract patterns, validate/invalidate Phase 1 assumptions, and identify the exact user segment to focus on (e.g., "The Active Curation Seeker").
---
## Phase 3: Define the Problem
**Goal:** Frame a clear, business-driven problem statement.
### Deliverable: The PRD (Product Requirements Document)
*   **Root Cause Analysis:** Based on Phase 1 & 2. (Example Hypothesis: *Traditional collaborative filtering over-indexes on historical watch-time, locking users into 'safe' echo chambers. Users lack a deterministic way to steer the algorithm out of its local minima.*)
*   **Target Segment:** e.g., Power users who listen 20+ hours a week but feel high fatigue with their current library.
*   **Business Case:** Improving discovery diversity directly correlates with long-term retention (LTV) and reduces churn to competitors like Apple Music or YouTube Music.
## Phase 4: Build an AI-Native MVP
**Goal:** Build a functional prototype demonstrating how AI solves this problem uniquely.
### Concept: "Spotify Vibe Steer" / AI Discovery Co-Pilot
Instead of passive scrolling, users converse with an AI agent to explicitly steer their discovery session in real-time.
---
### MVP Architecture Stack
#### 1. Frontend (User Interface)
*   **Tech:** React (Next.js) or Streamlit for rapid prototyping.
*   **UX:** A chat-like interface or smart search bar integrated into a mocked Spotify UI.
*   **Input:** Natural language (e.g., *"I want something like Arctic Monkeys but darker, instrumental, and high energy."*)
#### 2. Backend & Integration (API Layer)
*   **Tech:** FastAPI (Python).
*   **Spotify Web API Integration:** Connect to the real Spotify API to fetch tracks, audio features (valence, energy, acousticness), and seed genres.
#### 3. AI Agent Layer (The Core)
*   **LLM Router:** Takes the user's natural language prompt.
*   **Function Calling / Tool Use:** 
    *   The LLM translates the user's vague prompt into concrete Spotify API parameters.
    *   *Example:* User says "darker and high energy" -> LLM calls `get_recommendations(seed_genres=["indie"], target_valence=0.2, target_energy=0.8)`.
*   **Explainability:** The LLM receives the Spotify API results and generates a human-readable explanation for *why* these tracks match the prompt.
#### 4. The "Why AI?" Factor
*   **Why traditional systems fail here:** Collaborative filtering requires historical data and clicks. It cannot understand zero-shot, abstract concepts like "darker."
*   **What AI unlocks:** The ability to map semantic human intent directly to complex metadata vectors (audio features).
*   **User Experience:** Shifts discovery from **Passive/Algorithmic** to **Active/Conversational**, restoring user agency.
---
