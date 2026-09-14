from __future__ import annotations
import re

def validate_org_number(org_number: str) -> bool:
    """Validate a 9-digit Norwegian organization number with MOD-11 checksum."""
    if not isinstance(org_number, str):
        return False
        
    cleaned = re.sub(r'\s+', '', org_number).replace('-', '')
    
    if not re.match(r'^\d{9}$', cleaned):
        return False
        
    weights = [3, 2, 7, 6, 5, 4, 3, 2]
    digits = [int(d) for d in cleaned]
    
    checksum_sum = sum(digits[i] * weights[i] for i in range(8))
    remainder = checksum_sum % 11
    
    checksum = 11 - remainder if remainder != 0 else 0
    
    if checksum == 10:
        return False
        
    if checksum == 11:
        checksum = 0
        
    return checksum == digits[8]

def normalize_org_number(org_number: str) -> str:
    """Strip whitespace/dashes and validate. Raises ValueError if invalid."""
    if not isinstance(org_number, str):
        raise ValueError("Organization number must be a string")
        
    cleaned = re.sub(r'\s+', '', org_number).replace('-', '')
    
    if not validate_org_number(cleaned):
        raise ValueError(f"Invalid organization number: {org_number}")
        
    return cleaned
