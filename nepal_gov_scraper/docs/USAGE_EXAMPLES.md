# Usage Examples

## Quick Start

### Basic Scraping

```bash
# Install dependencies
pip install -r requirements.txt

# Run basic test on DAO Kathmandu
python -m tests.test_dao_kathmandu

# Run full scraper
python -m src.main
```

### Command Line Options

```bash
# Run with visible browser (for debugging)
python -m src.main --no-headless

# Custom delay settings (be respectful to servers)
python -m src.main --delay-min 3 --delay-max 6

# Save to specific file
python -m src.main --output my_nepal_offices.json

# Enable debug logging
python -m src.main --log-level DEBUG

# Test mode (limited offices)
python -m src.main --test-mode
```

## Python API Examples

### Basic Usage

```python
from src.scrapers.nepal_gov_scraper import NepalGovScraper

# Create scraper instance
scraper = NepalGovScraper(headless=True, delay_range=(2, 5))

# Run complete scraping
results = scraper.run_full_scrape()

# Display summary
print(f"Scraped {results.successful_scrapes} offices successfully")
print(f"Success rate: {results.successful_scrapes/results.total_scraped*100:.1f}%")

# Save results
output_file = scraper.save_results("nepal_offices.json")
print(f"Results saved to {output_file}")
```

### Individual Office Scraping

```python
from src.scrapers.nepal_gov_scraper import NepalGovScraper

scraper = NepalGovScraper()

# Get list of offices
office_list = scraper.scrape_moha_offices()

# Scrape specific office
for office_info in office_list[:3]:  # First 3 offices
    office = scraper.scrape_dao_details(office_info)
    if office:
        print(f"✅ {office.name_english}")
        print(f"   Completeness: {office.metadata.completeness_percentage:.1f}%")
        print(f"   Services: {len(office.services)}")
        print(f"   Staff: {len(office.staff)}")
    else:
        print(f"❌ Failed: {office_info['name_english']}")
```

### Working with Results

```python
import json
from datetime import datetime

# Load saved results
with open('nepal_offices.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Analyze results
offices = data['offices']
print(f"Total offices: {len(offices)}")

# Find offices with complete data
complete_offices = [
    office for office in offices 
    if office['metadata']['completeness_percentage'] > 80
]
print(f"Complete offices: {len(complete_offices)}")

# Find offices with phone numbers
offices_with_phones = [
    office for office in offices
    if office.get('contact', {}).get('phone_primary')
]
print(f"Offices with phones: {len(offices_with_phones)}")

# Display top offices by data quality
sorted_offices = sorted(
    offices, 
    key=lambda x: x['metadata']['data_quality_score'], 
    reverse=True
)

print("\nTop 5 offices by data quality:")
for i, office in enumerate(sorted_offices[:5], 1):
    score = office['metadata']['data_quality_score']
    completeness = office['metadata']['completeness_percentage']
    print(f"{i}. {office['name_english']} - Quality: {score:.2f}, Complete: {completeness:.1f}%")
```

## Customization Examples

### Custom Delay Strategy

```python
from src.scrapers.nepal_gov_scraper import NepalGovScraper
import random

class CustomScraper(NepalGovScraper):
    def respect_rate_limit(self, base_url):
        """Custom rate limiting with exponential backoff"""
        delay = random.uniform(2, 4)
        
        # Longer delay for government sites
        if 'gov.np' in base_url:
            delay *= 2
        
        time.sleep(delay)

# Use custom scraper
scraper = CustomScraper()
results = scraper.run_full_scrape()
```

### Adding Custom Services

```python
from src.models.data_models import Service, ServiceType, Fee, UrgencyLevel

# Create custom service
custom_service = Service(
    service_type=ServiceType.OTHER,
    name_english="Vehicle Registration",
    name_nepali="सवारी दर्ता"
)

# Add fees
custom_service.fees[UrgencyLevel.NORMAL] = Fee(
    amount_npr=2000.0,
    description="Normal vehicle registration"
)

# Add to office
office.services.append(custom_service)
```

### Filtering Results

```python
def filter_kathmandu_offices(results):
    """Filter offices in Kathmandu district"""
    kathmandu_offices = []
    
    for office in results.offices:
        if office.location and office.location.district == "Kathmandu":
            kathmandu_offices.append(office)
    
    return kathmandu_offices

# Usage
results = scraper.run_full_scrape()
ktm_offices = filter_kathmandu_offices(results)
print(f"Found {len(ktm_offices)} offices in Kathmandu")
```

## Data Processing Examples

### Export to CSV

```python
import csv
import json

# Load JSON results
with open('nepal_offices.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Export basic office info to CSV
with open('offices_summary.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Header
    writer.writerow([
        'Office Name', 'District', 'Phone', 'Email', 
        'Services Count', 'Staff Count', 'Completeness %'
    ])
    
    # Data rows
    for office in data['offices']:
        contact = office.get('contact', {})
        location = office.get('location', {})
        metadata = office.get('metadata', {})
        
        writer.writerow([
            office.get('name_english', ''),
            location.get('district', ''),
            contact.get('phone_primary', ''),
            contact.get('email', ''),
            len(office.get('services', [])),
            len(office.get('staff', [])),
            metadata.get('completeness_percentage', 0)
        ])

print("Exported to offices_summary.csv")
```

### Generate Statistics Report

```python
def generate_stats_report(results):
    """Generate comprehensive statistics"""
    offices = results.offices
    
    stats = {
        'total_offices': len(offices),
        'avg_completeness': sum(o.metadata.completeness_percentage for o in offices) / len(offices),
        'avg_quality_score': sum(o.metadata.data_quality_score for o in offices) / len(offices),
        'offices_with_phones': sum(1 for o in offices if o.contact and o.contact.phone_primary),
        'offices_with_emails': sum(1 for o in offices if o.contact and o.contact.email),
        'total_services': sum(len(o.services) for o in offices),
        'total_staff': sum(len(o.staff) for o in offices),
    }
    
    # District distribution
    districts = {}
    for office in offices:
        if office.location and office.location.district:
            district = office.location.district
            districts[district] = districts.get(district, 0) + 1
    
    stats['district_distribution'] = districts
    
    return stats

# Usage
results = scraper.run_full_scrape()
stats = generate_stats_report(results)

print(f"📊 Scraping Statistics Report")
print(f"Total offices: {stats['total_offices']}")
print(f"Average completeness: {stats['avg_completeness']:.1f}%")
print(f"Average quality: {stats['avg_quality_score']:.2f}")
print(f"Offices with phones: {stats['offices_with_phones']}")
print(f"Total services found: {stats['total_services']}")
print(f"Total staff records: {stats['total_staff']}")

print("\nTop 5 districts by office count:")
top_districts = sorted(stats['district_distribution'].items(), key=lambda x: x[1], reverse=True)
for district, count in top_districts[:5]:
    print(f"  {district}: {count} offices")
```

## Monitoring and Scheduling

### Automated Monthly Scraping

```python
import schedule
import time
from datetime import datetime

def monthly_scrape():
    """Run monthly scraping job"""
    print(f"Starting monthly scrape at {datetime.now()}")
    
    try:
        scraper = NepalGovScraper(headless=True)
        results = scraper.run_full_scrape()
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m")
        filename = f"data/nepal_offices_{timestamp}.json"
        scraper.save_results(filename)
        
        print(f"Monthly scrape completed: {filename}")
        
        # Send notification (implement as needed)
        send_notification(f"Scraped {results.successful_scrapes} offices")
        
    except Exception as e:
        print(f"Monthly scrape failed: {e}")
        send_error_notification(str(e))

# Schedule monthly scraping
schedule.every().month.do(monthly_scrape)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

### Progress Monitoring

```python
class ProgressMonitor:
    def __init__(self):
        self.start_time = None
        self.completed = 0
        self.total = 0
    
    def start(self, total_offices):
        self.start_time = datetime.now()
        self.total = total_offices
        self.completed = 0
        print(f"🚀 Starting scrape of {total_offices} offices")
    
    def update(self, office_name, success=True):
        self.completed += 1
        elapsed = datetime.now() - self.start_time
        
        if success:
            print(f"✅ [{self.completed}/{self.total}] {office_name}")
        else:
            print(f"❌ [{self.completed}/{self.total}] Failed: {office_name}")
        
        # Estimate remaining time
        if self.completed > 0:
            avg_time_per_office = elapsed.total_seconds() / self.completed
            remaining_offices = self.total - self.completed
            estimated_remaining = remaining_offices * avg_time_per_office
            
            if self.completed % 10 == 0:  # Every 10 offices
                print(f"📊 Progress: {self.completed/self.total*100:.1f}% - ETA: {estimated_remaining/60:.1f} minutes")

# Usage with custom scraper
monitor = ProgressMonitor()

# Customize scraper to use monitor
class MonitoredScraper(NepalGovScraper):
    def __init__(self, monitor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitor = monitor
    
    def run_full_scrape(self):
        office_list = self.scrape_moha_offices()
        self.monitor.start(len(office_list))
        
        for office_info in office_list:
            office = self.scrape_dao_details(office_info)
            self.monitor.update(office_info['name_english'], office is not None)
        
        return super().run_full_scrape()
```

These examples show the flexibility and power of the Nepal Government Office Scraper for various use cases from simple data collection to comprehensive monitoring and analysis.