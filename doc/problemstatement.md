# 🍽️ AI-Powered Restaurant Recommendation System

**Domain:** AI & Data Science (Zomato Use Case)

---

## 🎯 Objective
You are tasked with building an AI-powered restaurant recommendation service inspired by Zomato. The system should intelligently suggest restaurants based on user preferences by combining structured data with a Large Language Model (LLM).

Design and implement an application that:
- **Collects** user preferences (such as location, budget, cuisine, and ratings).
- **Ingests** a real-world dataset of restaurants.
- **Leverages** an LLM to generate personalized, human-like recommendations.
- **Displays** clear, useful, and explained results to the user.

---

## ⚙️ System Workflow

### 1. 📊 Data Ingestion
- **Source:** Load and preprocess the Zomato dataset from Hugging Face: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation).
- **Extraction:** Extract relevant fields such as restaurant name, location, cuisine, cost, rating, and other key metadata.

### 2. 👤 User Input
Collect and structure user preferences:
- **Location:** (e.g., Delhi, Bangalore)
- **Budget:** (Low, Medium, High)
- **Cuisine:** (e.g., Italian, Chinese, North Indian)
- **Minimum Rating:** (e.g., 4.0+)
- **Additional Preferences:** (e.g., Family-friendly, Quick service, Outdoor seating)

### 3. 🧠 Integration Layer
- **Data Filtering:** Filter and prepare relevant restaurant data based on user input to narrow down the context before feeding it to the LLM.
- **Prompt Engineering:** Pass the structured results into an LLM prompt. Design a prompt that helps the LLM reason, analyze, and rank the options effectively.

### 4. 🤖 Recommendation Engine
Use the LLM to:
- **Rank** the filtered restaurants based on how well they match the exact nuances of the user's prompt.
- **Explain** the recommendations (provide a human-like explanation for why each recommendation is a great fit).
- **Summarize** the final choices in a concise and engaging tone.

### 5. 💻 Output Display
- Present the final recommendations to the user in a clean, readable, and structured interface.
