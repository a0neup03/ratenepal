import time
import random
import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def setup_chrome_driver(headless: bool = True, user_agent: Optional[str] = None) -> webdriver.Chrome:
    """Setup Chrome WebDriver with appropriate options"""
    
    options = Options()
    
    if headless:
        options.add_argument("--headless")
    
    # Standard options for stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Set user agent
    if not user_agent:
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/120.0.0.0 Safari/537.36")
    
    options.add_argument(f"--user-agent={user_agent}")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        logging.error(f"Failed to setup Chrome driver: {e}")
        raise


def setup_requests_session() -> requests.Session:
    """Setup requests session with retry strategy"""
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set headers
    session.headers.update({
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    return session


def safe_get_text(element, default: str = "") -> str:
    """Safely extract text from a web element"""
    try:
        if element:
            text = element.get_attribute('textContent') or element.text
            return text.strip() if text else default
        return default
    except Exception:
        return default


def safe_get_attribute(element, attribute: str, default: str = "") -> str:
    """Safely extract attribute from a web element"""
    try:
        if element:
            attr = element.get_attribute(attribute)
            return attr.strip() if attr else default
        return default
    except Exception:
        return default


def wait_for_element(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10):
    """Wait for element to be present and return it"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logging.warning(f"Element not found: {by}={value} within {timeout} seconds")
        return None


def wait_for_elements(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10):
    """Wait for elements to be present and return them"""
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )
        return elements
    except TimeoutException:
        logging.warning(f"Elements not found: {by}={value} within {timeout} seconds")
        return []


def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
    """Add a random delay to avoid being detected as a bot"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def safe_click(driver: webdriver.Chrome, element):
    """Safely click an element with error handling"""
    try:
        # Scroll to element first
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        
        # Try regular click first
        element.click()
        return True
    except Exception as e:
        try:
            # Try JavaScript click as fallback
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e2:
            logging.warning(f"Failed to click element: {e}, {e2}")
            return False


def check_robots_txt(base_url: str, session: requests.Session) -> Dict[str, Any]:
    """Check robots.txt for crawling rules"""
    robots_url = f"{base_url.rstrip('/')}/robots.txt"
    
    try:
        response = session.get(robots_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Simple robots.txt parsing
            rules = {
                'allowed': True,
                'crawl_delay': 1,
                'disallowed_paths': []
            }
            
            lines = content.split('\n')
            user_agent_section = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('User-agent:'):
                    agent = line.split(':', 1)[1].strip()
                    user_agent_section = agent == '*' or 'python' in agent.lower()
                elif user_agent_section:
                    if line.startswith('Disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            rules['disallowed_paths'].append(path)
                        else:
                            rules['allowed'] = False
                    elif line.startswith('Crawl-delay:'):
                        try:
                            delay = int(line.split(':', 1)[1].strip())
                            rules['crawl_delay'] = max(delay, 1)
                        except ValueError:
                            pass
            
            return rules
        else:
            # No robots.txt found, assume crawling is allowed
            return {'allowed': True, 'crawl_delay': 1, 'disallowed_paths': []}
            
    except Exception as e:
        logging.warning(f"Could not fetch robots.txt from {robots_url}: {e}")
        return {'allowed': True, 'crawl_delay': 2, 'disallowed_paths': []}


def is_path_allowed(path: str, disallowed_paths: list) -> bool:
    """Check if a path is allowed based on robots.txt rules"""
    for disallowed in disallowed_paths:
        if path.startswith(disallowed):
            return False
    return True


def handle_consent_banner(driver: webdriver.Chrome):
    """Handle common consent/cookie banners"""
    consent_selectors = [
        "button[id*='accept']",
        "button[class*='accept']",
        "a[id*='accept']",
        "a[class*='accept']",
        ".cookie-accept",
        ".consent-accept",
        "#cookieAccept"
    ]
    
    for selector in consent_selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            if element and element.is_displayed():
                safe_click(driver, element)
                time.sleep(1)
                break
        except:
            continue


def scroll_to_load_content(driver: webdriver.Chrome, max_scrolls: int = 3):
    """Scroll down to load dynamic content"""
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Check if new content loaded by comparing page height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if i > 0 and new_height == previous_height:
            break
        previous_height = new_height