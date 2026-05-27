# Phase 3: Generation & Formatting - Edge Cases

## Overview
This document outlines the edge cases and mitigation strategies for Phase 3, dealing with LLM generation, constraints, and citations.

## Edge Cases

### 1. Hallucination Despite Strict Prompts
*   **Scenario:** The LLM generates a plausible-sounding fact (e.g., "The minimum SIP is ₹500") that is *not* present in the retrieved context.
*   **Impact:** Severe loss of trust and accuracy violation.
*   **Mitigation:** Use a low temperature setting (`temperature=0.0`). Implement a secondary "Fact-Checker" prompt or LLM call that verifies if the generated answer is strictly entailed by the retrieved chunks.

### 2. Sentence Limit Violation
*   **Scenario:** The answer requires a complex explanation, and the LLM outputs 4 or 5 sentences, violating the strict 3-sentence constraint.
*   **Impact:** Fails constraint checks.
*   **Mitigation:** Post-process the LLM output using regex or an NLP sentence tokenizer (like `nltk` or `spaCy`). If it exceeds 3 sentences, aggressively truncate it or force the LLM to regenerate with a stronger penalty.

### 3. Conflicting Information in Context
*   **Scenario:** The retrieved chunks contain conflicting data (e.g., a promotional header says "0% Exit Load", but the terms section says "1% within 1 year").
*   **Impact:** The LLM might pick the wrong one or get confused.
*   **Mitigation:** Instruct the LLM in the system prompt: "If the context contains conflicting information, state all conditions clearly (e.g., 'The exit load is 1% if redeemed within 1 year, and 0% thereafter')."

### 4. No Answer Found in Context
*   **Scenario:** The user asks a factual query about one of the 5 schemes, but that specific fact is not on the Groww page (e.g., the name of the fund manager's assistant).
*   **Impact:** The LLM might try to guess or hallucinate.
*   **Mitigation:** The system prompt must aggressively enforce: "If the provided context does not contain the answer, you must reply EXACTLY with: 'I cannot find this information in the official sources.'"
