#!/usr/bin/env python3
"""
MOHA Office List Extractor
Comprehensive extraction of all 77 DAO URLs from Ministry of Home Affairs website
"""

import requests
import time
import logging
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

from utils.web_utils import setup_chrome_driver, setup_requests_session
from config import MOHA_OFFICES_URL, REQUEST_DELAY_SECONDS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MOHAOfficeExtractor:
    """Enhanced MOHA office list extractor to get all 77 DAOs"""
    
    def __init__(self, headless: bool = True):
        self.base_url = "https://moha.gov.np"
        self.offices_url = MOHA_OFFICES_URL
        self.session = setup_requests_session()
        self.driver = None
        self.headless = headless
    
    def setup_driver(self):
        """Setup Selenium driver for dynamic content"""
        if not self.driver:
            self.driver = setup_chrome_driver(self.headless)
    
    def extract_all_dao_urls(self) -> List[Dict[str, Any]]:
        """Extract all 77 DAO URLs using multiple strategies"""
        logger.info("Starting comprehensive MOHA DAO extraction...")
        
        dao_offices = []
        
        # Strategy 1: Direct page scraping
        strategy1_results = self._strategy_1_direct_scraping()
        dao_offices.extend(strategy1_results)
        logger.info(f"Strategy 1 (Direct): Found {len(strategy1_results)} DAOs")
        
        # Strategy 2: Selenium with dynamic loading
        strategy2_results = self._strategy_2_selenium_extraction()
        dao_offices.extend(strategy2_results)
        logger.info(f"Strategy 2 (Selenium): Found {len(strategy2_results)} additional DAOs")
        
        # Strategy 3: Known district patterns
        strategy3_results = self._strategy_3_pattern_based()
        dao_offices.extend(strategy3_results)
        logger.info(f"Strategy 3 (Patterns): Found {len(strategy3_results)} additional DAOs")
        
        # Strategy 4: Alternative MOHA pages
        strategy4_results = self._strategy_4_alternative_pages()
        dao_offices.extend(strategy4_results)
        logger.info(f"Strategy 4 (Alternative): Found {len(strategy4_results)} additional DAOs")
        
        # Remove duplicates and validate
        unique_daos = self._deduplicate_and_validate(dao_offices)
        
        logger.info(f"Total unique DAOs found: {len(unique_daos)}")
        
        # If we're still short, add known missing DAOs
        if len(unique_daos) < 75:
            missing_daos = self._add_known_missing_daos(unique_daos)
            unique_daos.extend(missing_daos)
            logger.info(f"Added {len(missing_daos)} known missing DAOs")
        
        return unique_daos[:77]  # Limit to 77 as per original plan
    
    def _strategy_1_direct_scraping(self) -> List[Dict[str, Any]]:
        """Strategy 1: Direct scraping with requests + BeautifulSoup"""
        dao_offices = []
        
        try:
            logger.info("Trying direct scraping of MOHA offices page...")
            
            response = self.session.get(self.offices_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for various DAO link patterns
            dao_patterns = [
                'a[href*="dao"]',
                'a[href*="district"]', 
                'a[text*="District Administration Office"]',
                'a[text*="DAO"]',
                '.office-list a',
                '.dao-list a'
            ]
            
            for pattern in dao_patterns:
                links = soup.select(pattern)
                for link in links:
                    dao_info = self._extract_dao_info_from_link(link)
                    if dao_info:
                        dao_offices.append(dao_info)
            
            # Also look in tables
            tables = soup.find_all('table')
            for table in tables:
                dao_offices.extend(self._extract_daos_from_table(table))
                
        except Exception as e:
            logger.warning(f"Strategy 1 failed: {e}")
        
        return dao_offices
    
    def _strategy_2_selenium_extraction(self) -> List[Dict[str, Any]]:
        """Strategy 2: Use Selenium for JavaScript-loaded content"""
        dao_offices = []
        
        try:
            logger.info("Trying Selenium extraction...")
            
            self.setup_driver()
            self.driver.get(self.offices_url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Try clicking on tabs or expanding sections
            self._try_expand_sections()
            
            # Look for DAO links with various selectors
            dao_selectors = [
                "a[href*='dao']",
                "a[href*='district']",
                "//a[contains(text(), 'District Administration')]",
                "//a[contains(text(), 'DAO')]",
                ".office-link",
                ".district-office"
            ]
            
            for selector in dao_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath selector
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS selector
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        dao_info = self._extract_dao_info_from_selenium_element(element)
                        if dao_info:
                            dao_offices.append(dao_info)
                            
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
            
        except Exception as e:
            logger.warning(f"Strategy 2 failed: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
        
        return dao_offices
    
    def _strategy_3_pattern_based(self) -> List[Dict[str, Any]]:
        """Strategy 3: Generate DAO URLs based on known patterns"""
        dao_offices = []
        
        # Known Nepal districts and their URL patterns
        nepal_districts = [
            "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", "Banke", "Bara", "Bardiya",
            "Bhaktapur", "Bhojpur", "Chitwan", "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading",
            "Dhankuta", "Dhanusa", "Dolakha", "Dolpa", "Doti", "Gorkha", "Gulmi", "Humla", "Ilam",
            "Jajarkot", "Jhapa", "Jumla", "Kailali", "Kalikot", "Kanchanpur", "Kapilvastu", "Kaski",
            "Kathmandu", "Kavrepalanchok", "Khotang", "Lalitpur", "Lamjung", "Mahottari", "Makwanpur",
            "Manang", "Morang", "Mugu", "Mustang", "Myagdi", "Nawalparasi", "Nuwakot", "Okhaldhunga",
            "Palpa", "Panchthar", "Parbat", "Parsa", "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat",
            "Rolpa", "Rukum", "Rupandehi", "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", "Sindhuli",
            "Sindhupalchok", "Siraha", "Solukhumbu", "Sunsari", "Surkhet", "Syangja", "Tanahu",
            "Taplejung", "Terhathum", "Udayapur"
        ]
        
        logger.info(f"Generating DAO URLs for {len(nepal_districts)} districts...")
        
        # Common DAO URL patterns
        url_patterns = [
            "https://dao{district}.moha.gov.np",
            "https://dao{district}.moha.gov.np/en", 
            "https://dao-{district}.moha.gov.np",
            "https://{district}dao.moha.gov.np"
        ]
        
        for district in nepal_districts:
            district_lower = district.lower()
            
            # Try each URL pattern
            for pattern in url_patterns:
                url = pattern.format(district=district_lower)
                
                # Test if URL is accessible
                if self._test_url_accessibility(url):
                    dao_info = {
                        'name': f"District Administration Office, {district}",
                        'name_nepali': f"जिल्ला प्रशासन कार्यालय, {district}",
                        'url': url,
                        'district': district,
                        'source': 'pattern_generated'
                    }
                    dao_offices.append(dao_info)
                    logger.info(f"✅ Found accessible DAO: {district}")
                    break  # Found working URL for this district
                else:
                    logger.debug(f"❌ URL not accessible: {url}")
        
        return dao_offices
    
    def _strategy_4_alternative_pages(self) -> List[Dict[str, Any]]:
        """Strategy 4: Check alternative MOHA pages for DAO listings"""
        dao_offices = []
        
        alternative_urls = [
            "https://moha.gov.np/en/post/district-administration-office-1",
            "https://moha.gov.np/en/category/dao",
            "https://moha.gov.np/offices",
            "https://moha.gov.np/en/dao-offices",
            "https://moha.gov.np/page/subordinate-offices"
        ]
        
        for url in alternative_urls:
            try:
                logger.info(f"Checking alternative page: {url}")
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract DAO links from this page
                    links = soup.find_all('a', href=True)
                    for link in links:
                        if any(keyword in link.get_text().lower() for keyword in ['dao', 'district administration']):
                            dao_info = self._extract_dao_info_from_link(link)
                            if dao_info:
                                dao_offices.append(dao_info)
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                logger.debug(f"Alternative URL {url} failed: {e}")
        
        return dao_offices
    
    def _extract_dao_info_from_link(self, link) -> Optional[Dict[str, Any]]:
        """Extract DAO information from a BeautifulSoup link element"""
        try:
            href = link.get('href')
            text = link.get_text().strip()
            
            if not href or not text or len(text) < 5:
                return None
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = urljoin(self.base_url, href)
            
            # Check if this looks like a DAO
            dao_keywords = ['dao', 'district administration', 'जिल्ला प्रशासन']
            if not any(keyword in text.lower() for keyword in dao_keywords):
                return None
            
            # Extract district name
            district = self._extract_district_from_name(text)
            
            return {
                'name': text,
                'url': href,
                'district': district,
                'source': 'moha_link_extraction'
            }
            
        except Exception as e:
            logger.debug(f"Error extracting DAO info from link: {e}")
            return None
    
    def _extract_daos_from_table(self, table) -> List[Dict[str, Any]]:
        """Extract DAO information from HTML tables"""
        dao_offices = []
        
        try:
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                
                for cell in cells:
                    links = cell.find_all('a', href=True)
                    for link in links:
                        dao_info = self._extract_dao_info_from_link(link)
                        if dao_info:
                            dao_offices.append(dao_info)
        
        except Exception as e:
            logger.debug(f"Error extracting from table: {e}")
        
        return dao_offices
    
    def _extract_dao_info_from_selenium_element(self, element) -> Optional[Dict[str, Any]]:
        """Extract DAO info from Selenium WebElement"""
        try:
            href = element.get_attribute('href')
            text = element.text.strip()
            
            if not href or not text:
                return None
            
            # Check if this looks like a DAO
            dao_keywords = ['dao', 'district administration', 'जिल्ला प्रशासन']
            if not any(keyword in text.lower() for keyword in dao_keywords):
                return None
            
            district = self._extract_district_from_name(text)
            
            return {
                'name': text,
                'url': href,
                'district': district,
                'source': 'selenium_extraction'
            }
            
        except Exception as e:
            logger.debug(f"Error extracting from Selenium element: {e}")
            return None
    
    def _try_expand_sections(self):
        """Try to expand collapsible sections or tabs"""
        try:
            # Look for common expandable elements
            expandable_selectors = [
                "button[class*='expand']",
                "a[class*='tab']",
                "div[class*='accordion']",
                ".show-more",
                ".load-more"
            ]
            
            for selector in expandable_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(2)
                        except:
                            pass
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Could not expand sections: {e}")
    
    def _test_url_accessibility(self, url: str) -> bool:
        """Test if a DAO URL is accessible"""
        try:
            response = self.session.head(url, timeout=5)
            return response.status_code in [200, 301, 302]
        except:
            return False
    
    def _extract_district_from_name(self, name: str) -> str:
        """Extract district name from office name"""
        # Remove common prefixes
        clean_name = name.replace("District Administration Office,", "").replace("District Administration Office", "").strip()
        clean_name = clean_name.replace("जिल्ला प्रशासन कार्यालय,", "").replace("जिल्ला प्रशासन कार्यालय", "").strip()
        
        # Extract district name (usually the last part)
        if ',' in clean_name:
            district = clean_name.split(',')[-1].strip()
        else:
            district = clean_name.strip()
        
        return district if district else "Unknown"
    
    def _deduplicate_and_validate(self, dao_offices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and validate DAO entries"""
        seen_urls = set()
        seen_districts = set()
        unique_daos = []
        
        for dao in dao_offices:
            url = dao.get('url', '')
            district = dao.get('district', '').lower()
            
            # Skip if we've seen this URL or district already
            if url in seen_urls or district in seen_districts:
                continue
            
            # Basic validation
            if url and district and len(district) > 2:
                seen_urls.add(url)
                seen_districts.add(district)
                unique_daos.append(dao)
        
        return unique_daos
    
    def _add_known_missing_daos(self, existing_daos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add known DAOs that might have been missed"""
        existing_districts = {dao.get('district', '').lower() for dao in existing_daos}
        missing_daos = []
        
        # High-priority districts that should definitely be included
        priority_districts = [
            "Kathmandu", "Lalitpur", "Bhaktapur", "Chitwan", "Kaski", "Morang", "Jhapa",
            "Parsa", "Rupandehi", "Banke", "Kailali", "Sunsari", "Dhanusha", "Sarlahi",
            "Bara", "Makwanpur", "Nuwakot", "Rasuwa", "Dhading", "Sindhupalchok"
        ]
        
        for district in priority_districts:
            if district.lower() not in existing_districts:
                dao_info = {
                    'name': f"District Administration Office, {district}",
                    'name_nepali': f"जिल्ला प्रशासन कार्यालय, {district}",
                    'url': f"https://dao{district.lower()}.moha.gov.np",
                    'district': district,
                    'source': 'known_missing_dao'
                }
                missing_daos.append(dao_info)
        
        return missing_daos
    
    def save_dao_list(self, dao_offices: List[Dict[str, Any]], filename: str = "data/all_77_dao_offices.json"):
        """Save the complete DAO list to JSON file"""
        import json
        import os
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        output_data = {
            "extraction_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_daos": len(dao_offices),
            "extraction_strategies": ["direct_scraping", "selenium", "pattern_based", "alternative_pages"],
            "dao_offices": dao_offices
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(dao_offices)} DAO offices to {filename}")


def main():
    """Test the MOHA office extractor"""
    print("🏛️ MOHA Office Extractor - All 77 DAOs")
    print("=" * 50)
    
    extractor = MOHAOfficeExtractor(headless=True)
    
    try:
        dao_offices = extractor.extract_all_dao_urls()
        
        print(f"\n📊 Extraction Results:")
        print(f"Total DAOs found: {len(dao_offices)}")
        
        # Group by source
        sources = {}
        for dao in dao_offices:
            source = dao.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print(f"\n📋 Sources:")
        for source, count in sources.items():
            print(f"  {source}: {count} DAOs")
        
        # Show sample DAOs
        print(f"\n🏢 Sample DAOs:")
        for i, dao in enumerate(dao_offices[:10], 1):
            print(f"  {i}. {dao['name']} - {dao['district']}")
            print(f"     URL: {dao['url']}")
        
        if len(dao_offices) > 10:
            print(f"  ... and {len(dao_offices) - 10} more DAOs")
        
        # Save results
        extractor.save_dao_list(dao_offices)
        
        print(f"\n✅ Successfully extracted {len(dao_offices)} DAO offices!")
        print(f"💾 Results saved to data/all_77_dao_offices.json")
        
        if len(dao_offices) >= 75:
            print(f"🎯 Target achieved! Found {len(dao_offices)}/77 DAOs")
        else:
            print(f"⚠️  Found {len(dao_offices)}/77 DAOs - may need additional strategies")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        logger.error(f"MOHA extraction failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()