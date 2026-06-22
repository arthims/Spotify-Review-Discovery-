# Capstone / Grad Project Architecture: AI-Native Solution for Spotify Music Discovery

**Project Title:** Addressing the "Echo Chamber" Effect in Recommendation Systems using AI-Driven Intent Mapping
**Domain:** Product Management, AI Engineering, and UX Research

This document details the comprehensive phase-wise architecture and methodology for the Spotify Graduation Project, aligned with the requirements of `problemstatement1.md`. It is designed to demonstrate rigorous academic methodology, scalable system design, and product-driven AI implementation.

---

## Phase 1: AI-Powered Review Discovery Engine
**Objective:** Systematically ingest, process, and analyze qualitative user feedback at scale to identify core failures in current discovery mechanisms, focusing strictly on music discovery and repetitive listening habits.

### 1.1 Data Ingestion (ETL Pipeline)
*   **Sources:**
    *   **Primary Consolidated Dataset:** [Reviews_Spotify.csv](file:///C:/Users/SDS01493/.gemini/antigravity/scratch/Reviews_Spotify.csv) (and `.xlsx`) containing 2,412 de-duplicated multi-platform reviews (Google Play, App Store, Reddit, Forums, Social Media).
*   **Orchestration:** A scheduled script that reads new reviews, adds them to the master sheet, and prepares them for the discovery analysis engine.

### 1.2 Processing & Relevance Filtering
*   **Cleaning:** Remove PII, emojis, and boilerplate text using standard NLP sanitization.
*   **Relevance Filtering:** 
    *   Apply heuristic keyword matching (e.g. matching *discover*, *shuffle*, *repeat*, *same*, *algorithm*, *recommend*, *loop*, *weekly*, *radio*, *mix*, *heart*) and semantic relevance score thresholding.
    *   Strictly filter out irrelevant reviews (e.g., pure app crashes, billing errors, account recovery disputes, general subscription/price complaints that do not touch on recommendations or curation limits).
*   **Vectorization & Storage:** Convert filtered qualitative data into dense vector representations (e.g., via Hugging Face/OpenAI embeddings) and index them in a Vector Database (e.g. ChromaDB) to enable semantic clustering and RAG-based thematic querying.

### 1.3 LLM-Driven Analysis (The "Agent")
*   **Model:** Groq Llama-3.3-70b-versatile or equivalent.
*   **Pipeline:** 
    *   **RAG Querying:** Query the vector index using intent prompts corresponding to the project's six core discovery questions.
    *   **Thematic Synthesis:** Cluster qualitative insights to map out exactly *why* users struggle to discover music, the workarounds they use, and their unmet curation needs.


---

## Phase 2: Opportunity Validation (Primary User Research)
**Objective:** Ground the AI-generated hypotheses in primary, qualitative user research.

### 2.1 Methodology
*   **Screener:** Identify 5-6 participants who fit the "High-Engagement, Low-Discovery" profile identified in Phase 1.
*   **AI-Assisted Protocol:** Use the LLM to draft a semi-structured interview guide targeting the blind spots found in Phase 1.

### 2.2 Data Synthesis
*   **Transcription:** Process interview audio using **OpenAI Whisper**.
*   **Analysis:** Feed transcripts into an LLM context window to cross-reference primary insights against Phase 1 data, ensuring the identified "Root Cause" is statistically and qualitatively valid.

---

## Phase 3: Problem Definition & System Framing
**Objective:** Consolidate research into a structured Product Requirements Document (PRD).

### 3.1 Problem Framing
*   **Root Cause Hypothesis:** *Traditional collaborative filtering models over-optimize for engagement (watch/listen time), which traps users in "safe" local minima. Users lack semantic control to steer the algorithm.*
*   **Target Persona:** The "Active Curation Seeker" — users who want to discover music but are exhausted by passive, unpredictable algorithmic radio.

### 3.2 Business Case
*   **Metric Impact:** Demonstrate how solving this increases long-term retention (LTV), reduces churn, and boosts engagement diversity.

---

## Phase 4: AI-Native MVP Implementation ("Spotify Vibe Steer")
**Objective:** Deploy a functional, production-ready AI feature that translates natural human intent into complex API filter parameters.

### 4.1 System Components
*   **Frontend (User Interface):** 
    *   **Framework:** Next.js (React) or Streamlit.
    *   **Interaction:** A conversational chat interface (e.g., "Give me songs like Tame Impala but darker, faster, and instrumental").
*   **Backend (API & Orchestration Layer):**
    *   **Framework:** FastAPI (Python).
    *   **Spotify Web API:** Handles authentication (OAuth), fetches user top artists, and queries the `/recommendations` endpoint.
*   **AI Engine (The "Intent Router"):**
    *   **Function Calling:** The LLM receives the natural language prompt and executes a strict JSON function call: 
        `get_spotify_recs(seed_genres=["psychedelic rock"], target_valence=0.3, target_energy=0.8, target_instrumentalness=0.9)`
    *   **Explainable AI (XAI):** The system returns the playlist alongside an LLM-generated explanation of *why* these tracks match the prompt (e.g., "I selected tracks with low valence (darker) and high energy to match your request").

### 4.2 Sequence Diagram Flow
1. **User** types a mood/vibe prompt into the **Frontend**.
2. **Frontend** sends the query to the **FastAPI Backend**.
3. **Backend** passes the query to the **LLM**.
4. **LLM** interprets the intent and responds with structured JSON containing Spotify audio parameters (Valence, Energy, Acousticness, etc.).
5. **Backend** calls the **Spotify API** with these exact parameters.
6. **Backend** sends the track list back to the **LLM** to generate a human-readable justification.
7. **Frontend** displays the AI-curated playlist and the explanation to the **User**.

---

## Phase 5: Quantitative Thematic Analytics & Insight Synthesizer
**Objective:** Programmatically process the filtered reviews to auto-generate a comprehensive UX research report addressing the six core product discovery challenges.

### 5.1 Thematic Clustering Engine
*   **Heuristic / Semantic Search:** Query the filtered `Reviews_Spotify.csv` using specialized semantic profiles representing the six core discovery questions (e.g. *smart shuffle loop frustrations*, *desire for manual mood steering*, *echo chamber root causes*).
*   **Insight Compiler:** Feed the retrieved relevant review records into an LLM context window to synthesize summaries, user quotes, and actionable recommendations.
*   **Output:** Auto-generate a structured product discovery report (`thematic_research_report.md`) detailing evidence-backed answers.

---

## Phase 6: Interactive Analytical Dashboard
**Objective:** Build a qualitative and quantitative visual analytics dashboard to help product developers inspect user feedback trends.

### 6.1 Streamlit Visualization Module
*   **Data Source:** Read filtered data from `Reviews_Spotify.csv` dynamically.
*   **Key Visuals:**
    *   *Topic Sentiment Distribution:* Compare ratings and sentiment across Google Play, App Store, Reddit, Forums, and Social Media.
    *   *Interactive Keyword Explorer:* A search panel allowing developers to input keywords (e.g. "DJ", "shuffle", "heart") to instantly filter and read user quotes.
    *   *Problem Statement Q&A Panels:* Expandable UI cards displaying the synthesized answers to the six discovery questions backed by raw user quotes.

---

## Deployment & Evaluation
### Infrastructure
*   **Backend & LLM Proxy:** Deployed on **Render** or **Railway** as a Dockerized FastAPI service.
*   **Frontend:** Deployed on **Vercel**.
*   **Database:** SQLite (local/prototyping) or Supabase (PostgreSQL) for storing session logs.

### Evaluation Metrics (For the Grad Project Defense)
1. **Accuracy of Intent Translation:** How well the LLM maps text to correct audio parameters (Manual Evaluation / Human-in-the-loop).
2. **Discovery Rate:** Percentage of generated tracks the user has *never* listened to before.
3. **User Satisfaction:** Measured via a simple thumbs-up/thumbs-down mechanism in the MVP UI.
