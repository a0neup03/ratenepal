#!/usr/bin/env python3
"""
Configuration file for Nepal Government Office Scraper
Centralizes URLs, default values, and settings for easier maintenance
"""

# --- Target URLs ---
DAO_KATHMANDU_URL = "https://daokathmandu.moha.gov.np"
MOHA_OFFICES_URL = "https://moha.gov.np/en/offices"
PASSPORT_DEPT_URL = "https://nepalpassport.gov.np"

# Test URLs for DAO Kathmandu
DAO_KATHMANDU_TEST_URLS = [
    "https://daokathmandu.moha.gov.np/en",
    "https://daokathmandu.moha.gov.np/en/services", 
    "https://daokathmandu.moha.gov.np/en/members"
]

# --- Scraping Settings ---
HEADLESS_BROWSER = True
REQUEST_DELAY_SECONDS = 3  # Delay between HTTP requests to be polite
SELENIUM_TIMEOUT_SECONDS = 20
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# --- Default Data Points (Known Values) ---
# Used for validation and as fallbacks
DEFAULT_PASSPORT_FEES = {
    "normal_34pg": 5000,
    "fast_track_34pg": 12000,
    "same_day_34pg": 15000,
    "normal_66pg": 10000,
    "fast_track_66pg": 20000,
}

DEFAULT_CITIZENSHIP_FEES = {
    "normal": 100,
    "urgent": 500,
}

DEFAULT_PROCESSING_TIMES = {
    "passport": {
        "normal": "15-30 days",
        "urgent": "3-4 days", 
        "same_day": "1 day"
    },
    "citizenship": {
        "normal": "15-20 days",
        "urgent": "3-5 days"
    }
}

DEFAULT_OPERATING_HOURS = "10:00 AM - 5:00 PM, Sunday to Thursday; 10:00 AM - 3:00 PM, Friday"

# --- Known Office Data ---
KNOWN_DAO_KATHMANDU = {
    "name": "District Administration Office, Kathmandu",
    "name_nepali": "जिल्ला प्रशासन कार्यालय, काठमाडौं",
    "address": "Babarmahal, Kathmandu, Nepal",
    "phones": ["01-5362828", "01-5367691"],
    "district": "Kathmandu",
    "province": "Bagmati Province",
    "staff": [
        {
            "name": "Rabin Kumar Rai",
            "position": "Administrative Officer",
            "section": "Citizenship Section"
        }
    ]
}

KNOWN_PASSPORT_DEPT = {
    "name": "Department of Passport, Tripureshwor",
    "address": "Tripureshwor, Kathmandu, Nepal", 
    "phone": "+977-1-5970330",
    "email": "communication@nepalpassport.gov.np",
    "director": "Prakash Mani Paudel"
}

# --- Output Settings ---
OUTPUT_FILENAME = "data/scraped_data.json"
SCHEMA_VERSION = "1.0.0"
DATA_DIRECTORY = "data"
LOGS_DIRECTORY = "logs"

# --- Nepal-Specific Patterns ---
NEPAL_PHONE_PATTERNS = [
    r'\+?977[-\s]?1[-\s]?\d{7}',  # International format
    r'0?1[-\s]?\d{7}',            # Local format  
    r'\d{2}-\d{7}',               # Hyphenated format
    r'०[०-९][-\s]?[०-९]{7}'        # Nepali numerals
]

NEPAL_EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:gov\.np|org\.np|com\.np|np)\b'

# Nepal district to province mapping
DISTRICT_PROVINCE_MAPPING = {
    "Kathmandu": "Bagmati Province",
    "Lalitpur": "Bagmati Province", 
    "Bhaktapur": "Bagmati Province",
    "Chitwan": "Bagmati Province",
    "Pokhara": "Gandaki Province",
    "Biratnagar": "Province No. 1",
    "Birgunj": "Madhesh Province",
    "Dharan": "Province No. 1",
    "Butwal": "Lumbini Province",
    "Nepalgunj": "Lumbini Province"
}

# Common Nepali terms for text processing
NEPALI_TERMS = {
    "office": ["कार्यालय", "अफिस"],
    "district": ["जिल्ला"],
    "administration": ["प्रशासन"],
    "passport": ["राहदानी"],
    "citizenship": ["नागरिकता"],
    "certificate": ["प्रमाणपत्र"],
    "section": ["शाखा", "सेक्शन"],
    "officer": ["अधिकारी", "अफिसर"]
}