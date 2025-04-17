import re
from typing import Dict, Pattern

# Comprehensive PII patterns
PII_PATTERNS: Dict[str, Pattern] = {
    'name': re.compile(r'\b(?:[A-Z][a-z]+(?: [A-Z][a-z]+)+)\b'),  # First Last names
    'phone': re.compile(r'\b(?:\+\d{1,3}\s?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b'),  # International phones
    'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),  # Emails
    'ssn': re.compile(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'),  # Social Security Numbers
    'credit_card': re.compile(r'\b(?:\d[ -]*?){13,16}\b'),  # Credit cards
    'date': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),  # Dates
    'medical_record': re.compile(r'\b[A-Z]{2,}\d{5,}\b'),  # Medical record numbers
}

def anonymize_text(text: str) -> str:
    """
    Anonymizes PII in medical text with type-specific redaction tags.
    Returns the anonymized text and a log of redactions made.
    """
    redaction_log = []
    
    for pii_type, pattern in PII_PATTERNS.items():
        def replacer(match):
            redaction_log.append({
                'type': pii_type,
                'value': match.group(),
                'position': (match.start(), match.end())
            })
            return f'[REDACTED {pii_type.upper()}]'
        
        text = pattern.sub(replacer, text)
    
    return text