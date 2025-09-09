import re
from typing import Optional, List, Tuple


def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace and special characters"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common unwanted characters
    text = re.sub(r'[^\w\s\-\+\(\)\.\,\:\;\/\@\#]', '', text)
    
    return text


def extract_phone_numbers(text: str) -> List[str]:
    """Extract Nepal phone numbers from text"""
    if not text:
        return []
    
    phones = []
    
    # Nepal phone number patterns
    patterns = [
        r'\+977[-\s]?[0-9][-\s]?[0-9]{7}',  # +977-1-1234567
        r'977[-\s]?[0-9][-\s]?[0-9]{7}',    # 977-1-1234567
        r'0[0-9][-\s]?[0-9]{7}',            # 01-1234567
        r'[0-9]{2}[-\s]?[0-9]{7}',          # 14-1234567
        r'[0-9]{8,10}'                       # 11234567 or 9841234567
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Clean the phone number
            phone = re.sub(r'[-\s]', '', match)
            if len(phone) >= 7:
                phones.append(phone)
    
    return list(set(phones))  # Remove duplicates


def extract_email_addresses(text: str) -> List[str]:
    """Extract email addresses from text"""
    if not text:
        return []
    
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    
    return list(set(emails))  # Remove duplicates


def normalize_nepal_address(address: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Normalize Nepal address and extract district/municipality info
    Returns: (cleaned_address, district, municipality)
    """
    if not address:
        return None, None, None
    
    address = clean_text(address)
    
    # Common district patterns
    district_patterns = [
        r'([A-Za-z\s]+)\s+District',
        r'District\s+([A-Za-z\s]+)',
        r'([A-Za-z]+)\s*,\s*Nepal'
    ]
    
    district = None
    for pattern in district_patterns:
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            district = match.group(1).strip()
            break
    
    # Common municipality/VDC patterns
    municipality_patterns = [
        r'([A-Za-z\s]+)\s+Municipality',
        r'([A-Za-z\s]+)\s+VDC',
        r'Ward\s*No\.?\s*\d+,\s*([A-Za-z\s]+)'
    ]
    
    municipality = None
    for pattern in municipality_patterns:
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            municipality = match.group(1).strip()
            break
    
    return address, district, municipality


def extract_ward_number(text: str) -> Optional[int]:
    """Extract ward number from address text"""
    if not text:
        return None
    
    patterns = [
        r'Ward\s*No\.?\s*(\d+)',
        r'वडा\s*नं\.?\s*(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue
    
    return None


def extract_staff_info(text: str) -> List[Tuple[str, str]]:
    """
    Extract staff names and positions from text
    Returns: List of (name, position) tuples
    """
    if not text:
        return []
    
    staff_info = []
    
    # Common patterns for staff information
    patterns = [
        r'([A-Za-z\s]+)\s*[-–]\s*([A-Za-z\s,]+(?:Officer|Chief|Director|Manager|Supervisor|Assistant))',
        r'([A-Za-z\s]+)\s*,\s*([A-Za-z\s,]+(?:Officer|Chief|Director|Manager|Supervisor|Assistant))',
        r'(Mr\.?\s*|Ms\.?\s*|Mrs\.?\s*)?([A-Za-z\s]+)\s*[-–]\s*([A-Za-z\s,]+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 3:  # Pattern with title
                name = clean_text(f"{match[0]} {match[1]}".strip())
                position = clean_text(match[2])
            else:  # Pattern without title
                name = clean_text(match[0])
                position = clean_text(match[1])
            
            if name and position and len(name) > 2:
                staff_info.append((name, position))
    
    return staff_info


def extract_operating_hours(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract operating hours from text
    Returns: (opening_time, closing_time)
    """
    if not text:
        return None, None
    
    # Common patterns for operating hours
    patterns = [
        r'(\d{1,2}):?(\d{2})?\s*(AM|PM)?\s*[-–to]\s*(\d{1,2}):?(\d{2})?\s*(AM|PM)?',
        r'(\d{1,2}):(\d{2})\s*[-–to]\s*(\d{1,2}):(\d{2})',
        r'Open\s*:?\s*(\d{1,2}):?(\d{2})?\s*(AM|PM)?.*Close\s*:?\s*(\d{1,2}):?(\d{2})?\s*(AM|PM)?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            
            # Extract opening time
            if groups[0] and groups[1]:
                opening = f"{groups[0]}:{groups[1]}"
            elif groups[0]:
                opening = f"{groups[0]}:00"
            else:
                continue
                
            # Extract closing time (depends on pattern)
            closing = None
            if len(groups) >= 5 and groups[3] and groups[4]:
                closing = f"{groups[3]}:{groups[4]}"
            elif len(groups) >= 4 and groups[3]:
                closing = f"{groups[3]}:00"
            
            return opening, closing
    
    return None, None


def is_nepal_text(text: str) -> bool:
    """Check if text contains Nepali/Devanagari characters"""
    if not text:
        return False
    
    # Devanagari Unicode range
    devanagari_pattern = r'[\u0900-\u097F]'
    return bool(re.search(devanagari_pattern, text))


def separate_english_nepali(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Separate English and Nepali text from mixed content
    Returns: (english_text, nepali_text)
    """
    if not text:
        return None, None
    
    # Split by common separators and analyze each part
    parts = re.split(r'[/\|\(\)]', text)
    
    english_parts = []
    nepali_parts = []
    
    for part in parts:
        part = part.strip()
        if part:
            if is_nepal_text(part):
                nepali_parts.append(part)
            else:
                # Check if it's meaningful English (not just numbers/symbols)
                if re.search(r'[A-Za-z]', part) and len(part) > 2:
                    english_parts.append(part)
    
    english_text = ' '.join(english_parts) if english_parts else None
    nepali_text = ' '.join(nepali_parts) if nepali_parts else None
    
    return english_text, nepali_text