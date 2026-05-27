# Phase 1: Data Ingestion & Preprocessing - Edge Cases

## Overview
This document outlines the edge cases and mitigation strategies for Phase 1, dealing with scraping, parsing, and chunking the data from the 5 Groww URLs.

## Edge Cases

### 1. Dynamic Content / JavaScript Rendering Failure
*   **Scenario:** Crucial scheme data (like expense ratio or exit load) is loaded asynchronously via JavaScript and is not present in the initial HTML payload.
*   **Impact:** Important factual data is missing from the vector database.
*   **Mitigation:** Use a headless browser (Playwright/Puppeteer) that waits for network idle or specific DOM elements to render before extracting text.

### 2. Complex Table Parsing
*   **Scenario:** Information is presented in complex HTML tables (e.g., holding breakdowns) that lose their semantic meaning when flattened into raw text.
*   **Impact:** The LLM receives garbled text and hallucinates or fails to answer queries about that data.
*   **Mitigation:** Use Markdown conversion tools (like `html2text` or `markdownify`) to preserve table structures.

### 3. Missing Metadata (Last Updated Date)
*   **Scenario:** The Groww page does not explicitly state a "Last Updated" date, which is required for the response footer.
*   **Impact:** Violation of the transparency constraint.
*   **Mitigation:** Fallback to the `Date` header from the HTTP response or the timestamp of when the scraping job was executed, explicitly formatting it as: `Last updated from sources (Fetched on): <date>`.

### 4. Noise Ingestion
*   **Scenario:** The scraper picks up unrelated text (e.g., promotional banners, "Customers also bought", or footer disclaimers) that pollutes the semantic search space.
*   **Impact:** Retrieval accuracy drops.
*   **Mitigation:** Target specific CSS selectors (e.g., `<div class="scheme-details">`) rather than scraping the entire `<body>`.
