# Phase 2: Query Processing & Retrieval - Edge Cases

## Overview
This document outlines the edge cases and mitigation strategies for Phase 2, which handles user intent classification and vector retrieval.

## Edge Cases

### 1. Subtle Advisory Queries
*   **Scenario:** The user asks a question that seems factual but implies advice, e.g., "Is an exit load of 1% too high for this fund?" or "Which of these 5 funds has the best expense ratio?"
*   **Impact:** The system might accidentally provide comparative or advisory responses, violating strict constraints.
*   **Mitigation:** Strengthen the Intent Classifier prompt to explicitly catch comparative adjectives ("best", "highest", "better") and subjective qualifiers ("too high", "good"). Route these to the Refusal Handler.

### 2. Ambiguous or Incomplete Queries
*   **Scenario:** The user types something extremely short or ambiguous like "minimum" or "returns".
*   **Impact:** The retrieval system pulls random contexts, leading to confusing or irrelevant answers.
*   **Mitigation:** If the retrieval confidence score is below a certain threshold, prompt the user for clarification: "Could you please specify which scheme or detail (e.g., minimum SIP amount) you are asking about?"

### 3. Out-of-Scope Scheme Queries
*   **Scenario:** The user asks for facts about a mutual fund *not* in the list of 5 URLs (e.g., "What is the expense ratio for Axis Bluechip?").
*   **Impact:** The system searches the existing 5 schemes and might hallucinate an answer based on HDFC data, or fail silently.
*   **Mitigation:** Implement a pre-retrieval entity extraction step. If a scheme name is detected that does not match the 5 authorized HDFC schemes, immediately return a refusal: "I can only provide information on the 5 supported HDFC schemes."

### 4. Multi-Intent Queries
*   **Scenario:** User asks a combined question: "What is the exit load and should I invest?"
*   **Impact:** Partial factual answer combined with a potential compliance violation.
*   **Mitigation:** The Intent Classifier must treat the entire query as Advisory if *any* part of it seeks advice, triggering the Refusal Handler for the whole prompt.
