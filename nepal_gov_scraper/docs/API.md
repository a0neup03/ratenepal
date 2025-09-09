# Nepal Government Scraper API Documentation

## Core Classes

### NepalGovScraper

Main scraper class for collecting data from Nepal government websites.

```python
from src.scrapers.nepal_gov_scraper import NepalGovScraper

# Initialize scraper
scraper = NepalGovScraper(headless=True, delay_range=(2, 5))

# Run full scrape
results = scraper.run_full_scrape()

# Save results
scraper.save_results("my_results.json")
```

#### Constructor Parameters

- `headless` (bool): Run browser in headless mode (default: True)
- `delay_range` (tuple): Min and max delay between requests in seconds (default: (2, 5))

#### Methods

##### `run_full_scrape() -> ScrapingResult`
Executes the complete scraping process including:
1. Scraping MOHA offices list
2. Individual DAO details
3. Passport department information

##### `scrape_moha_offices() -> List[Dict[str, str]]`
Scrapes the Ministry of Home Affairs office directory.

##### `scrape_dao_details(office_info: Dict[str, str]) -> Optional[Office]`
Scrapes detailed information from a specific DAO website.

##### `scrape_passport_department() -> Optional[Office]`
Scrapes Department of Passports information.

##### `save_results(filename: str = None) -> str`
Saves scraping results to JSON file.

## Data Models

### Office
Represents a government office with comprehensive information.

```python
from src.models.data_models import Office, OfficeType

office = Office(
    office_id="dao_kathmandu",
    name_english="District Administration Office, Kathmandu",
    office_type=OfficeType.DAO
)
```

#### Properties
- `office_id`: Unique identifier
- `name_english`: English name
- `name_nepali`: Nepali name (optional)
- `office_type`: Type of office (DAO, CENTRAL_DEPT, etc.)
- `location`: Location information
- `contact`: Contact details
- `services`: List of services offered
- `staff`: Staff information
- `operating_hours`: Operating schedule
- `metadata`: Scraping metadata

#### Methods
- `calculate_completeness() -> float`: Calculate data completeness percentage
- `to_dict() -> Dict[str, Any]`: Convert to dictionary for JSON serialization

### Service
Represents a government service (passport, citizenship, etc.).

```python
from src.models.data_models import Service, ServiceType, UrgencyLevel, Fee

service = Service(
    service_type=ServiceType.PASSPORT,
    name_english="Passport Application"
)

# Add fees
service.fees[UrgencyLevel.NORMAL] = Fee(amount_npr=5000.0)
service.fees[UrgencyLevel.URGENT] = Fee(amount_npr=12000.0)
```

### Contact
Contact information for an office.

```python
from src.models.data_models import Contact

contact = Contact(
    phone_primary="01-5362828",
    email="info@daokathmandu.gov.np",
    website="https://daokathmandu.moha.gov.np"
)
```

### Location
Physical location information.

```python
from src.models.data_models import Location

location = Location(
    address_english="Babarmahal, Kathmandu",
    district="Kathmandu",
    province="Bagmati Province"
)
```

### Staff
Staff member information.

```python
from src.models.data_models import Staff

staff = Staff(
    name_english="Rabin Kumar Rai",
    position="Administrative Officer",
    section="Citizenship Section"
)
```

## Utility Functions

### Text Processing

```python
from src.utils.text_processing import (
    extract_phone_numbers,
    extract_email_addresses,
    normalize_nepal_address
)

# Extract phone numbers
phones = extract_phone_numbers("Contact: 01-5362828, 01-4444444")
# Returns: ['015362828', '014444444']

# Extract emails
emails = extract_email_addresses("Email: info@dao.gov.np")
# Returns: ['info@dao.gov.np']

# Normalize address
address, district, municipality = normalize_nepal_address(
    "Ward No. 5, Lalitpur Municipality, Lalitpur District"
)
```

### Web Utilities

```python
from src.utils.web_utils import (
    setup_chrome_driver,
    setup_requests_session,
    check_robots_txt
)

# Setup Chrome driver
driver = setup_chrome_driver(headless=True)

# Setup requests session with retry logic
session = setup_requests_session()

# Check robots.txt compliance
rules = check_robots_txt("https://example.com", session)
```

## Enums

### ServiceType
- `PASSPORT`: Passport services
- `CITIZENSHIP`: Citizenship certificate services
- `OTHER`: Other government services

### OfficeType
- `DAO`: District Administration Office
- `CENTRAL_DEPT`: Central government department
- `PASSPORT_DEPT`: Department of Passports
- `OTHER`: Other office types

### UrgencyLevel
- `NORMAL`: Normal processing
- `URGENT`: Urgent processing
- `SAME_DAY`: Same-day processing

## Error Handling

The scraper implements comprehensive error handling:

```python
try:
    results = scraper.run_full_scrape()
except Exception as e:
    print(f"Scraping failed: {e}")
    # Check results.errors for detailed error information
```

Common exceptions:
- `TimeoutException`: Page load timeout
- `WebDriverException`: Browser-related errors
- `requests.RequestException`: HTTP request errors
- `ValueError`: Data validation errors

## Data Quality

### Completeness Score
Each office has a completeness percentage based on filled fields:

```python
completeness = office.calculate_completeness()
print(f"Data completeness: {completeness:.1f}%")
```

### Data Quality Score
Overall data quality score (0.0 to 1.0):

```python
quality = office.metadata.data_quality_score
print(f"Data quality: {quality:.2f}")
```

## Output Format

Results are saved in JSON format with the following structure:

```json
{
  "offices": [
    {
      "office_id": "dao_kathmandu",
      "name_english": "District Administration Office, Kathmandu",
      "office_type": "district_administration_office",
      "location": {
        "address_english": "Babarmahal, Kathmandu",
        "district": "Kathmandu",
        "province": "Bagmati Province"
      },
      "contact": {
        "phone_primary": "01-5362828",
        "website": "https://daokathmandu.moha.gov.np"
      },
      "services": [...],
      "staff": [...],
      "metadata": {
        "scraped_at": "2024-01-01T10:00:00",
        "completeness_percentage": 75.0,
        "data_quality_score": 0.8
      }
    }
  ],
  "summary": {
    "total_scraped": 50,
    "successful_scrapes": 45,
    "failed_scrapes": 5,
    "success_rate": 90.0
  }
}
```