# 🏗️ Phase-Wise Architecture: AI Restaurant Recommendation System

This document outlines the step-by-step phased architecture for building the AI-Powered Restaurant Recommendation System based on the Zomato use case.

---

## 🟢 Phase 1: Foundation & Data Engineering
**Goal:** Set up the environment, acquire the data, and prepare it for querying.

1. **Environment Setup:** Initialize the project using Python. Set up virtual environments and install core dependencies (`pandas`, `datasets`, `openai`/`langchain`, `streamlit`/`fastapi`).
2. **Data Acquisition:** Use the Hugging Face `datasets` library to pull the `ManikaSaini/zomato-restaurant-recommendation` dataset.
3. **Data Preprocessing:** 
   - Clean missing or malformed data.
   - Standardize text columns (e.g., lowercasing cuisines, normalizing location names).
   - Convert data types (e.g., ensuring ratings and costs are numeric).
4. **Storage:** Save the cleaned dataset into an efficient format (like Parquet or a local SQLite database) for rapid filtering in later phases.
5. **Basic Web UI (Input Source):** Initialize a basic web interface (e.g., Streamlit) to serve as the initial source for collecting user input.

---

## 🟡 Phase 2: Core Search & Filtering (Heuristics Layer)
**Goal:** Build the engine that filters the massive dataset down to a relevant subset based on user constraints.

1. **Input Handler:** Create data models (e.g., using Pydantic) to capture user preferences:
   - Location (Exact match or regional)
   - Budget Constraints (Range filtering)
   - Cuisine (List intersection)
   - Minimum Rating (Threshold filtering)
2. **Hard Filtering Engine:** Query the cleaned dataset using the user's hard constraints. This step is crucial to reduce the context window size before sending data to the LLM. It should narrow thousands of rows down to the **Top 10-20 candidates**.

---

## 🟠 Phase 3: AI & LLM Integration (Recommendation Engine)
**Goal:** Introduce the "brain" of the system to provide personalized, human-like recommendations.

1. **LLM Setup:** Integrate an LLM provider (e.g., OpenAI API, Anthropic, or a local open-source model).
2. **Prompt Engineering:**
   - **System Prompt:** Define the AI's persona (e.g., "You are an expert food critic and local guide...").
   - **Context Injection:** Format the Top 10-20 filtered restaurants into a structured format (JSON or Markdown tables) and inject it into the prompt.
   - **User Intent:** Pass the user's explicit and implicit preferences (e.g., "looking for a cozy vibe for an anniversary").
3. **Reasoning & Ranking:** Instruct the LLM to analyze the provided subset, rank the top 3-5 options, and write a brief, compelling explanation for *why* it fits the user's unique request.

---

## 🔴 Phase 4: User Interface & Experience
**Goal:** Build a user-friendly frontend to interact with the system.

1. **Frontend Development:** Use a rapid UI framework like **Streamlit** (Python-native) or **Next.js** for a more robust web app.
2. **Form Inputs:** Create intuitive UI controls for the user:
   - Dropdowns for City/Location
   - Multi-selects for Cuisines
   - Sliders for Budget and Rating
   - Text Area for "Additional Preferences" (e.g., "Must have vegan options and outdoor seating")
3. **Result Presentation:** Design a clean output display that showcases the LLM's recommended restaurants with beautiful cards, highlighting the restaurant name, key stats, and the AI's personalized reasoning.

---

## 🟣 Phase 5: Advanced Refinements (Future Scope)
**Goal:** Scale the system and improve recommendation quality.

1. **Semantic Search / RAG:** Instead of hard filtering, convert restaurant reviews/descriptions into vector embeddings and store them in a Vector DB (like Chroma or Pinecone). This allows for semantic matching (e.g., searching for "romantic sunset view" directly).
2. **Caching:** Implement caching (e.g., Redis or simple in-memory cache) for identical queries to save LLM costs and reduce latency.
3. **Conversational Agent:** Upgrade the UI from a static form to an interactive chatbot where the user can refine their choices dynamically (e.g., "These look great, but do any of them have live music?").

---

## 🏗️ Phase 6: Decoupled Production Architecture
**Goal:** Migrate the monolithic Streamlit application into a robust, decoupled, and highly scalable production system.

1. **Backend API (FastAPI):**
   - Wrap the core Python logic (Parquet data loading, `filter_engine`, and Groq LLM `recommender`) into a high-performance **FastAPI** application.
   - Expose RESTful endpoints (e.g., `POST /recommendations`) that accept JSON user preferences and return structured JSON recommendations.
   - Implement basic error handling, CORS middleware, and input validation using Pydantic.
2. **Rich Frontend (Next.js / React):**
   - Replace the basic Streamlit interface with a modern, dynamic web application built using **Next.js**.
   - Use **TailwindCSS** to design a stunning, premium aesthetic (dark mode, glassmorphism, micro-animations for loading states).
   - Implement state management to handle user inputs and cleanly render the JSON API response into highly engaging restaurant cards.
3. **Containerization:**
   - Write `Dockerfile`s for both the FastAPI backend and Next.js frontend to allow for easy cloud deployment (e.g., AWS, GCP, Vercel/Render).

---

## 🚀 Phase 7: Deployment (Streamlit Alternative)
**Goal:** Deploy the original monolithic Streamlit application quickly and for free using Streamlit Community Cloud.

1. **Repository Setup:**
   - Push the codebase (specifically `frontend/app.py`, `backend/`, and `llm/`) to a public or private GitHub repository.
   - Ensure `requirements.txt` is updated with all dependencies (e.g., `streamlit`, `pandas`, `langchain-groq`, `pydantic`).
2. **Streamlit Community Cloud:**
   - Connect the GitHub repository to [Streamlit Community Cloud](https://streamlit.io/cloud).
   - Set the main file path to `frontend/app.py`.
3. **Secrets Management & Data Handling:**
   - Add the `GROQ_API_KEY` to the Streamlit Cloud Secrets management dashboard to securely inject the API key without exposing it in the codebase.
   - Execute the `data_ingestion.py` script automatically during startup to generate the `cleaned_zomato.parquet` file locally in the cloud container, avoiding the need to upload the large ~150MB file to GitHub.
