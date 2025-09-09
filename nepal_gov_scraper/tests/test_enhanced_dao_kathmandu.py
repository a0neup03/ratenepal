#!/usr/bin/env python3
"""
Enhanced test scraper for DAO Kathmandu incorporating pattern-based extraction
Based on the reference implementation provided
"""

import sys
import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup
from src.models.enhanced_models import (
    Office, Contact, Location, Staff, Service, Section,
    ServiceFees, Fee, ProcessingTimes, OperatingHours, Metadata,
    create_enhanced_dao_kathmandu
)
from src.config import (
    DAO_KATHMANDU_URL, DAO_KATHMANDU_TEST_URLS, 
    NEPAL_PHONE_PATTERNS, USER_AGENT
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EnhancedDAOKathmanduScraper:
    """Enhanced scraper for DAO Kathmandu using pattern-based extraction"""
    
    def __init__(self):
        self.base_url = DAO_KATHMANDU_URL
        self.test_urls = DAO_KATHMANDU_TEST_URLS
        self.scraped_data = {}
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with proper headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        return session
    
    def test_dao_kathmandu(self) -> Office:
        """Enhanced test scraping of DAO Kathmandu with pattern extraction"""
        
        print("🧪 Testing Enhanced DAO Kathmandu scraper...")
        print("=" * 60)
        
        scraped_data = {}
        
        # Test multiple URLs
        for url in self.test_urls:
            try:
                print(f"\n🌐 Testing URL: {url}")
                
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text_content = soup.get_text()
                    
                    # Extract information using pattern matching
                    contact_info = self.extract_contact_patterns(text_content)
                    staff_info = self.extract_staff_patterns(soup)
                    hours_info = self.extract_hours_patterns(text_content)
                    services_info = self.extract_services_patterns(text_content)
                    
                    scraped_data[url] = {
                        'contact': contact_info,
                        'staff': staff_info,
                        'hours': hours_info,
                        'services': services_info,
                        'page_title': soup.title.string if soup.title else None,
                        'text_preview': text_content[:500],
                        'status': 'success'
                    }
                    
                    print(f"✅ Successfully scraped {url}")
                    print(f"   📞 Contact items: {len(contact_info)}")
                    print(f"   👥 Staff items: {len(staff_info)}")
                    print(f"   🕐 Hours info: {'Yes' if hours_info else 'No'}")
                    
                else:
                    print(f"❌ Failed to access {url} (Status: {response.status_code})")
                    scraped_data[url] = {'status': 'failed', 'status_code': response.status_code}
                    
            except Exception as e:
                print(f"💥 Error scraping {url}: {e}")
                scraped_data[url] = {'status': 'error', 'error': str(e)}
        
        # Create enhanced office data
        enhanced_office = self.create_enhanced_office_data(scraped_data)
        
        # Save detailed results
        self.save_test_results(scraped_data, enhanced_office)
        
        print(f"\n📊 Enhanced Test Results:")
        print(f"   Office: {enhanced_office.name}")
        print(f"   Services: {len(enhanced_office.services)}")
        print(f"   Staff: {len(enhanced_office.staff)}")
        print(f"   Completeness: {enhanced_office.metadata.completeness_score:.1f}%")
        print(f"   Data Quality: {enhanced_office.metadata.data_quality}")
        
        return enhanced_office
    
    def extract_contact_patterns(self, text: str) -> Dict[str, Any]:
        """Enhanced contact information extraction using multiple patterns"""
        contact_info = {}
        
        # Phone number extraction with Nepal-specific patterns
        phones = []
        for pattern in NEPAL_PHONE_PATTERNS:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        # Clean and deduplicate phone numbers
        cleaned_phones = list(set(self._clean_phone_number(phone) for phone in phones))
        if cleaned_phones:
            contact_info['phones'] = cleaned_phones
        
        # Enhanced email extraction (prioritize .gov.np)
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]*\.gov\.np\b',  # Government emails first
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Any emails
        ]
        
        emails = []
        for pattern in email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            emails.extend(matches)
        
        if emails:
            contact_info['emails'] = list(set(emails))
        
        # Enhanced address extraction
        address_keywords = [
            'Babarmahal', 'काठमाडौं', 'Kathmandu', 'Nepal', 
            'नेपाल', 'बाबरमहल', 'जिल्ला प्रशासन'
        ]
        
        for keyword in address_keywords:
            if keyword in text:
                # Extract surrounding context (broader range)
                start = max(0, text.find(keyword) - 100)
                end = min(len(text), text.find(keyword) + 150)
                context = text[start:end].strip()
                
                # Clean up the context
                context = ' '.join(context.split())
                contact_info['address_context'] = context
                break
        
        # Look for website/URL mentions
        url_pattern = r'https?://[^\s<>"\']*'
        urls = re.findall(url_pattern, text)
        if urls:
            contact_info['websites'] = list(set(urls))
        
        return contact_info
    
    def extract_staff_patterns(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Enhanced staff information extraction"""
        staff_info = []
        
        # Pattern 1: Table-based staff information
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    text_cells = [cell.get_text().strip() for cell in cells]
                    
                    # Look for staff-related keywords
                    combined_text = ' '.join(text_cells).lower()
                    staff_keywords = ['officer', 'subba', 'chief', 'director', 'administrator', 
                                    'अधिकारी', 'प्रमुख', 'निर्देशक']
                    
                    if any(keyword in combined_text for keyword in staff_keywords):
                        staff_info.append({
                            'raw_data': text_cells,
                            'source': 'table',
                            'type': 'structured'
                        })
        
        # Pattern 2: List-based staff information  
        lists = soup.find_all(['ul', 'ol'])
        for list_elem in lists:
            items = list_elem.find_all('li')
            for item in items:
                text = item.get_text().strip()
                if self._contains_staff_keywords(text):
                    staff_info.append({
                        'raw_data': text,
                        'source': 'list',
                        'type': 'unstructured'
                    })
        
        # Pattern 3: Paragraph-based staff mentions
        paragraphs = soup.find_all('p')
        for para in paragraphs:
            text = para.get_text().strip()
            if self._contains_staff_keywords(text) and len(text) < 200:
                staff_info.append({
                    'raw_data': text,
                    'source': 'paragraph',
                    'type': 'mention'
                })
        
        return staff_info
    
    def extract_hours_patterns(self, text: str) -> Dict[str, Any]:
        """Enhanced operating hours extraction"""
        hours_info = {}
        
        # Time pattern extraction (multiple formats)
        time_patterns = [
            r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)',  # 10:00 AM format
            r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}',  # 10:00-17:00 format
            r'\d{1,2}\s*(?:AM|PM|am|pm)\s*-\s*\d{1,2}\s*(?:AM|PM|am|pm)',  # 10 AM - 5 PM
            r'बजे',  # Nepali time indicator
            r'देखि.*सम्म'  # Nepali "from...to" 
        ]
        
        time_mentions = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            time_mentions.extend(matches)
        
        if time_mentions:
            hours_info['time_mentions'] = time_mentions
        
        # Day-related keywords (English and Nepali)
        day_keywords = {
            'english': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
            'nepali': ['सोमबार', 'मंगलबार', 'बुधबार', 'बिहिबार', 'शुक्रबार', 'शनिबार', 'आइतबार']
        }
        
        found_days = []
        for lang, days in day_keywords.items():
            for day in days:
                if day.lower() in text.lower():
                    found_days.append((lang, day))
        
        if found_days:
            hours_info['day_mentions'] = found_days
        
        # Look for break/lunch mentions
        break_patterns = [
            r'lunch\s*break', r'खाजा\s*समय', r'बिदा', 
            r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}.*(?:lunch|खाजा)'
        ]
        
        break_mentions = []
        for pattern in break_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            break_mentions.extend(matches)
        
        if break_mentions:
            hours_info['break_mentions'] = break_mentions
        
        return hours_info
    
    def extract_services_patterns(self, text: str) -> Dict[str, Any]:
        """Extract service-related information"""
        services_info = {}
        
        # Service keywords
        service_keywords = {
            'passport': ['passport', 'राहदानी', 'e-passport'],
            'citizenship': ['citizenship', 'नागरिकता', 'certificate', 'प्रमाणपत्र']
        }
        
        found_services = []
        for service_type, keywords in service_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    found_services.append(service_type)
                    break
        
        if found_services:
            services_info['services_mentioned'] = list(set(found_services))
        
        # Fee patterns
        fee_patterns = [
            r'(?:NPR|Rs\.?|रु)\s*\d+',
            r'\d+\s*(?:NPR|Rs\.?|रुपैयाँ)',
            r'fee[s]?\s*[:\-]\s*\d+',
            r'शुल्क.*\d+'
        ]
        
        fee_mentions = []
        for pattern in fee_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            fee_mentions.extend(matches)
        
        if fee_mentions:
            services_info['fee_mentions'] = fee_mentions
        
        return services_info
    
    def create_enhanced_office_data(self, scraped_data: Dict[str, Any]) -> Office:
        """Create enhanced office object from scraped data"""
        
        # Start with the default enhanced office
        office = create_enhanced_dao_kathmandu()
        
        # Enhance with scraped data
        all_contacts = {}
        all_staff = []
        
        for url, data in scraped_data.items():
            if data.get('status') != 'success':
                continue
                
            # Merge contact information
            contact = data.get('contact', {})
            if contact.get('phones'):
                all_contacts.setdefault('phones', []).extend(contact['phones'])
            if contact.get('emails'):
                all_contacts.setdefault('emails', []).extend(contact['emails'])
            if contact.get('address_context'):
                all_contacts['address'] = contact['address_context']
            
            # Extract staff from scraped data
            staff_data = data.get('staff', [])
            for staff_item in staff_data:
                parsed_staff = self._parse_staff_item(staff_item)
                if parsed_staff:
                    all_staff.extend(parsed_staff)
        
        # Update office with scraped contact info
        if all_contacts.get('phones'):
            unique_phones = list(set(all_contacts['phones']))
            if len(unique_phones) >= 1:
                office.contact.phone_general = unique_phones[0]
            if len(unique_phones) >= 2:
                office.contact.phone_citizenship = unique_phones[1]
        
        if all_contacts.get('emails'):
            office.contact.email = all_contacts['emails'][0]
        
        # Add any new staff found (avoid duplicates)
        existing_names = [staff.name.lower() for staff in office.staff]
        for new_staff in all_staff:
            if new_staff.name.lower() not in existing_names:
                office.staff.append(new_staff)
        
        # Update metadata
        office.metadata.last_scraped = datetime.now().isoformat()
        office.metadata.data_quality = "enhanced_test_with_live_data"
        office.metadata.extraction_method = "pattern_based_enhanced"
        
        # Recalculate completeness
        office.update_completeness_score()
        
        return office
    
    def _clean_phone_number(self, phone: str) -> str:
        """Clean phone number format"""
        # Remove common separators
        cleaned = re.sub(r'[-\s\(\)]', '', phone)
        
        # Handle Nepal country code
        if cleaned.startswith('+977'):
            cleaned = cleaned[4:]
        elif cleaned.startswith('977'):
            cleaned = cleaned[3:]
        
        # Ensure proper format
        if not cleaned.startswith('0') and len(cleaned) == 7:
            cleaned = '01' + cleaned
            
        return cleaned
    
    def _contains_staff_keywords(self, text: str) -> bool:
        """Check if text contains staff-related keywords"""
        staff_keywords = [
            'officer', 'subba', 'chief', 'director', 'administrator',
            'secretary', 'assistant', 'clerk', 'manager',
            'अधिकारी', 'प्रमुख', 'निर्देशक', 'सहायक', 'सचिव'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in staff_keywords)
    
    def _parse_staff_item(self, staff_item: Dict[str, Any]) -> List[Staff]:
        """Parse staff information from scraped item"""
        staff_list = []
        raw_data = staff_item.get('raw_data', '')
        
        if isinstance(raw_data, list):
            # Table format - try to extract name and position
            if len(raw_data) >= 2:
                name = raw_data[0].strip()
                position = raw_data[1].strip()
                section = raw_data[2].strip() if len(raw_data) >= 3 else None
                
                if name and position and self._is_valid_name(name):
                    staff_list.append(Staff(
                        name=name,
                        position=position,
                        section=section
                    ))
        
        elif isinstance(raw_data, str):
            # String format - try to parse name and position
            # Look for patterns like "Name - Position" or "Name, Position"
            patterns = [
                r'([A-Za-z\s]+?)\s*[-–]\s*([A-Za-z\s,]+)',
                r'([A-Za-z\s]+?)\s*,\s*([A-Za-z\s,]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, raw_data)
                if match:
                    name = match.group(1).strip()
                    position = match.group(2).strip()
                    
                    if self._is_valid_name(name) and self._contains_staff_keywords(position):
                        staff_list.append(Staff(name=name, position=position))
                        break
        
        return staff_list
    
    def _is_valid_name(self, name: str) -> bool:
        """Check if string looks like a valid person name"""
        if not name or len(name) < 3:
            return False
        
        # Should contain mostly letters and spaces
        if not re.match(r'^[A-Za-z\s.]+$', name):
            return False
        
        # Should have at least 2 words for full name
        words = name.split()
        if len(words) < 2:
            return False
        
        # Avoid common non-name words
        non_name_words = ['office', 'department', 'section', 'कार्यालय', 'विभाग']
        if any(word.lower() in name.lower() for word in non_name_words):
            return False
        
        return True
    
    def save_test_results(self, scraped_data: Dict[str, Any], office: Office):
        """Save test results to JSON file"""
        os.makedirs('data', exist_ok=True)
        
        results = {
            'test_metadata': {
                'test_name': 'Enhanced DAO Kathmandu Scraper Test',
                'test_date': datetime.now().isoformat(),
                'urls_tested': list(scraped_data.keys()),
                'scraper_version': 'enhanced_pattern_based_1.0'
            },
            'scraped_raw_data': scraped_data,
            'enhanced_office_data': office.to_dict(),
            'summary': {
                'urls_successful': len([d for d in scraped_data.values() if d.get('status') == 'success']),
                'urls_failed': len([d for d in scraped_data.values() if d.get('status') != 'success']),
                'completeness_score': office.metadata.completeness_score,
                'services_count': len(office.services),
                'staff_count': len(office.staff)
            }
        }
        
        filename = 'data/enhanced_dao_kathmandu_test_results.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Enhanced test results saved to {filename}")


def main():
    """Run the enhanced DAO Kathmandu test"""
    print("🇳🇵 Enhanced DAO Kathmandu Scraper Test")
    print("=" * 60)
    
    scraper = EnhancedDAOKathmanduScraper()
    enhanced_office = scraper.test_dao_kathmandu()
    
    print("\n" + "=" * 60)
    print("📋 ENHANCED TEST OFFICE DATA SUMMARY:")
    print("=" * 60)
    print(f"Office: {enhanced_office.name}")
    print(f"Services: {len(enhanced_office.services)}")
    print(f"Contact Phone: {enhanced_office.contact.phone_general}")
    print(f"Contact Email: {enhanced_office.contact.email or 'Not found'}")
    print(f"Address: {enhanced_office.location.address}")
    print(f"Staff Members: {len(enhanced_office.staff)}")
    print(f"Completeness: {enhanced_office.metadata.completeness_score:.1f}%")
    
    print("\n📋 Services Details:")
    for service in enhanced_office.services:
        print(f"\n🔷 {service.service_name}:")
        if service.fees and service.fees.normal_processing:
            print(f"   💰 Normal fee: NPR {service.fees.normal_processing.amount}")
            print(f"   ⏱️  Processing time: {service.fees.normal_processing.processing_days}")
        if service.fees and service.fees.urgent_processing:
            print(f"   💰 Urgent fee: NPR {service.fees.urgent_processing.amount}")
        if service.required_documents:
            print(f"   📄 Required docs: {len(service.required_documents)} items")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced test completed successfully!")
    return enhanced_office


if __name__ == "__main__":
    main()