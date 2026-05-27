# Phase 0: Target Schemes & Knowledge Base - Edge Cases

## Overview
This document outlines the edge cases and mitigation strategies for Phase 0, which strictly defines the 5 Groww URLs used for the knowledge base.

## Edge Cases

### 1. URL Inaccessibility or Slug Change
*   **Scenario:** One of the 5 exact Groww URLs is taken down, renamed, or returns a 404 Not Found error.
*   **Impact:** The scraper fails to fetch the data for that scheme, leaving a gap in the knowledge base.
*   **Mitigation:** Implement a health-check script that pings the 5 URLs daily. If a 404 is detected, trigger an alert to manually update the URL in the system configuration.

### 2. Anti-Scraping Defenses (CAPTCHA / Cloudflare)
*   **Scenario:** Groww enables strict anti-bot protection (like Cloudflare Turnstile) on these specific scheme pages, blocking automated HTTP requests.
*   **Impact:** Complete failure of data ingestion.
*   **Mitigation:** 
    *   Rotate User-Agent strings.
    *   Use a headless browser (e.g., Playwright or Selenium) rather than simple `requests`.
    *   Implement exponential backoff and retry logic.

### 3. Page Redirection
*   **Scenario:** The URL redirects to a general mutual funds page or a login prompt.
*   **Impact:** The scraper ingests irrelevant content or fails entirely.
*   **Mitigation:** Disable auto-redirects in the scraping client or strictly validate the `<title>` tag of the fetched page to ensure it matches the expected scheme name.
