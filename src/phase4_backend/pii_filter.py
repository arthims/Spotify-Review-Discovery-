import re

# Regular expression patterns for common Indian PII
AADHAAR_PATTERN = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b')
PAN_PATTERN = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b(?:\+91[\s-]?)?[6-9]\d{9}\b|\b\d{10}\b')

def contains_pii(text: str) -> bool:
    """
    Checks if a given string contains common PII (Aadhaar, PAN, email, phone number).
    """
    if not text:
        return False
        
    if AADHAAR_PATTERN.search(text):
        return True
    if PAN_PATTERN.search(text):
        return True
    if EMAIL_PATTERN.search(text):
        return True
    if PHONE_PATTERN.search(text):
        return True
        
    return False

def redact_pii(text: str) -> str:
    """
    Redacts any detected PII in the given string with standardized labels.
    """
    if not text:
        return ""
        
    redacted = text
    redacted = AADHAAR_PATTERN.sub("[REDACTED_AADHAAR]", redacted)
    redacted = PAN_PATTERN.sub("[REDACTED_PAN]", redacted)
    redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", redacted)
    redacted = PHONE_PATTERN.sub("[REDACTED_PHONE]", redacted)
    
    return redacted
