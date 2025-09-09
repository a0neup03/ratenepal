#!/usr/bin/env python3
"""
Test script for text processing utilities
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.text_processing import (
    clean_text, extract_phone_numbers, extract_email_addresses,
    normalize_nepal_address, extract_staff_info, extract_operating_hours,
    separate_english_nepali, is_nepal_text
)


def test_phone_extraction():
    """Test phone number extraction"""
    print("=== Testing Phone Number Extraction ===")
    
    test_cases = [
        "Contact: 01-5362828",
        "Phone: +977-1-1234567",
        "Call us at 977-14-123456",
        "Mobile: 9841234567",
        "Office: 01-5367691, 01-4444444"
    ]
    
    for text in test_cases:
        phones = extract_phone_numbers(text)
        print(f"Text: {text}")
        print(f"Phones: {phones}")
        print()


def test_email_extraction():
    """Test email extraction"""
    print("=== Testing Email Extraction ===")
    
    test_cases = [
        "Email: info@daokathmandu.gov.np",
        "Contact us: admin@moha.gov.np or support@nepal.gov",
        "Send to: test@example.com, another@domain.org"
    ]
    
    for text in test_cases:
        emails = extract_email_addresses(text)
        print(f"Text: {text}")
        print(f"Emails: {emails}")
        print()


def test_address_normalization():
    """Test Nepal address normalization"""
    print("=== Testing Address Normalization ===")
    
    test_cases = [
        "Babarmahal, Kathmandu District, Nepal",
        "Ward No. 5, Lalitpur Municipality, Lalitpur",
        "Bhaktapur District, Bagmati Province"
    ]
    
    for address in test_cases:
        clean_addr, district, municipality = normalize_nepal_address(address)
        print(f"Original: {address}")
        print(f"Cleaned: {clean_addr}")
        print(f"District: {district}")
        print(f"Municipality: {municipality}")
        print()


def test_staff_extraction():
    """Test staff information extraction"""
    print("=== Testing Staff Information Extraction ===")
    
    test_cases = [
        "Rabin Kumar Rai - Administrative Officer, Citizenship Section",
        "Mr. John Doe, Chief Administrative Officer",
        "Sita Maya Sharma - Assistant Director"
    ]
    
    for text in test_cases:
        staff = extract_staff_info(text)
        print(f"Text: {text}")
        print(f"Staff: {staff}")
        print()


def test_operating_hours():
    """Test operating hours extraction"""
    print("=== Testing Operating Hours Extraction ===")
    
    test_cases = [
        "Office Hours: 10:00 AM - 5:00 PM",
        "Open 10:00 to 17:00",
        "Working time: 10AM-5PM"
    ]
    
    for text in test_cases:
        opening, closing = extract_operating_hours(text)
        print(f"Text: {text}")
        print(f"Hours: {opening} - {closing}")
        print()


def test_language_separation():
    """Test English/Nepali text separation"""
    print("=== Testing Language Separation ===")
    
    test_cases = [
        "District Administration Office / जिल्ला प्रशासन कार्यालय",
        "Kathmandu (काठमाडौं)",
        "राहदानी विभाग | Department of Passports"
    ]
    
    for text in test_cases:
        english, nepali = separate_english_nepali(text)
        print(f"Original: {text}")
        print(f"English: {english}")
        print(f"Nepali: {nepali}")
        print(f"Contains Nepali: {is_nepal_text(text)}")
        print()


def main():
    """Run all tests"""
    print("🧪 Testing Text Processing Utilities")
    print("=" * 50)
    print()
    
    test_phone_extraction()
    test_email_extraction()
    test_address_normalization()
    test_staff_extraction()
    test_operating_hours()
    test_language_separation()
    
    print("=" * 50)
    print("✅ All text processing tests completed!")


if __name__ == "__main__":
    main()