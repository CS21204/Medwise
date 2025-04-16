import re

def anonymize_text(text: str):
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[REDACTED NAME]', text)
    text = re.sub(r'\b\d{10}\b', '[REDACTED PHONE]', text)
    return text
