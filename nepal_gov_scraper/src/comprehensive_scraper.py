#!/usr/bin/env python3
"""
Comprehensive Nepal Government Office Scraper with 20+ Offices
Includes passport, license, land registration, and other government services
"""

import json
import time
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests

from models.office_factory import GovernmentOfficeFactory, create_comprehensive_office_list
from models.enhanced_models import Office, Metadata
from config_extended import ALL_EXTENDED_OFFICES, SCHEMA_VERSION
from utils.text_processing import extract_phone_numbers, extract_email_addresses
from complete_dao_list import generate_complete_dao_list

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComprehensiveNepalGovScraper:
    """Comprehensive scraper for 20+ Nepal government offices"""
    
    def __init__(self):
        self.factory = GovernmentOfficeFactory()
        self.offices: List[Office] = []
        self.session = self._setup_requests_session()
        
        # Create necessary directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        logger.info("Comprehensive Nepal Government Scraper initialized")
    
    def _setup_requests_session(self) -> requests.Session:
        """Setup requests session with proper headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        return session
    
    def create_all_offices(self, include_all_77_daos: bool = False):
        """Create comprehensive government offices, optionally including all 77 DAOs"""
        if include_all_77_daos:
            logger.info("Creating COMPLETE list including all 77 Nepal DAOs...")
            self.offices = self._create_complete_office_list()
        else:
            logger.info("Creating comprehensive list of Nepal government offices...")
            self.offices = create_comprehensive_office_list()
        
        logger.info(f"✅ Created {len(self.offices)} comprehensive offices")
        
        # Group offices by type for summary
        office_types = {}
        provinces = {}
        for office in self.offices:
            office_type = office.type
            office_types[office_type] = office_types.get(office_type, 0) + 1
            
            if hasattr(office, 'location') and hasattr(office.location, 'province'):
                province = office.location.province
                if province:
                    provinces[province] = provinces.get(province, 0) + 1
        
        logger.info("📊 Office distribution:")
        for office_type, count in office_types.items():
            logger.info(f"   {office_type}: {count} offices")
            
        if provinces:
            logger.info("🌍 Provincial distribution:")
            for province, count in provinces.items():
                logger.info(f"   {province}: {count} offices")
        
        return self.offices
    
    def _create_complete_office_list(self) -> List[Office]:
        """Create complete office list: existing 21+ offices + all 77 DAOs"""
        offices = []
        
        # First, add existing comprehensive offices (non-DAO)
        logger.info("Adding existing comprehensive offices...")
        existing_offices = create_comprehensive_office_list()
        
        # Filter out DAOs from existing offices to avoid duplicates
        non_dao_offices = [
            office for office in existing_offices 
            if not (office.type == "district_administration_office" and 
                   "District Administration Office" in office.name)
        ]
        offices.extend(non_dao_offices)
        logger.info(f"Added {len(non_dao_offices)} existing non-DAO offices")
        
        # Then, add all 77 DAOs from complete list
        logger.info("Adding all 77 Nepal DAOs...")
        dao_data_list = generate_complete_dao_list()
        
        for dao_data in dao_data_list:
            dao_office = self._create_office_from_dao_data(dao_data)
            if dao_office:
                offices.append(dao_office)
        
        logger.info(f"Added {len(dao_data_list)} DAO offices")
        logger.info(f"Total offices: {len(offices)}")
        
        return offices
    
    def _create_office_from_dao_data(self, dao_data: Dict[str, Any]) -> Optional[Office]:
        """Convert DAO data from complete list to Office object"""
        try:
            from models.enhanced_models import Contact, Location, Service, Section, ServiceFees, Fee, ProcessingTimes, OperatingHours, Metadata
            
            # Create contact information
            contact = None
            if dao_data.get('phones') or dao_data.get('url'):
                contact = Contact(
                    phone_general=dao_data.get('phones', [None])[0],
                    website=dao_data['url'],
                    email=None
                )
            
            # Create location
            location = Location(
                address=dao_data.get('address', f"{dao_data['district']}, Nepal"),
                district=dao_data['district'],
                province=dao_data['province'],
                coordinates=None
            )
            
            # Create basic citizenship service for all DAOs
            citizenship_service = Service(
                service_id="citizenship_certificate",
                service_name="Citizenship Certificate",
                service_name_nepali="नागरिकता प्रमाणपत्र",
                sections=[Section(section_name="Citizenship Section", staff=[])],
                fees=ServiceFees(
                    normal_processing=Fee(
                        amount=100.0,
                        currency="NPR",
                        processing_days="15-20 days",
                        description="Normal citizenship certificate processing"
                    ),
                    urgent_processing=Fee(
                        amount=500.0,
                        currency="NPR", 
                        processing_days="3-5 days",
                        description="Urgent citizenship certificate processing"
                    )
                ),
                processing_times=ProcessingTimes(
                    document_submission="30 minutes",
                    verification_process="5-7 days",
                    total_normal="15-20 days",
                    total_urgent="3-5 days"
                ),
                required_documents=[
                    "Birth certificate",
                    "Parents' citizenship certificates", 
                    "Recommendation letter from ward office",
                    "Passport size photos (2 copies)"
                ]
            )
            
            # Create office with standard operating hours
            operating_hours = OperatingHours(
                monday_friday="10:00 AM - 5:00 PM",
                saturday="10:00 AM - 3:00 PM", 
                sunday="closed",
                lunch_break="1:00 PM - 2:00 PM",
                notes="Hours may vary during festivals"
            )
            
            # Create metadata
            metadata = Metadata(
                data_source=dao_data['url'],
                last_scraped=datetime.now().isoformat(),
                data_quality="generated_from_complete_dao_list",
                verification_status="unverified",
                schema_version=SCHEMA_VERSION,
                completeness_score=70.0,  # Base score for generated data
                scraper_version="comprehensive_1.0.0",
                extraction_method="dao_list_generation"
            )
            
            # Convert staff data to Staff objects
            staff_list = []
            if 'staff' in dao_data:
                from models.enhanced_models import Staff
                for staff_dict in dao_data['staff']:
                    staff_obj = Staff(
                        name=staff_dict['name'],
                        position=staff_dict['position'],
                        section=staff_dict.get('section')
                    )
                    staff_list.append(staff_obj)

            # Create office
            office = Office(
                id=f"dao_{dao_data['district'].lower().replace(' ', '_')}",
                type="district_administration_office",
                name=dao_data['name'],
                name_nepali=dao_data['name_nepali'],
                location=location,
                contact=contact,
                services=[citizenship_service],
                staff=staff_list,
                operating_hours=operating_hours,
                metadata=metadata
            )
            
            return office
            
        except Exception as e:
            logger.error(f"Error creating office from DAO data {dao_data.get('district', 'unknown')}: {e}")
            return None
    
    def enhance_with_live_data(self, max_attempts: int = 5):
        """Attempt to enhance offices with live data where possible"""
        logger.info("🌐 Attempting to enhance offices with live data...")
        
        enhanced_count = 0
        
        for i, office in enumerate(self.offices[:max_attempts]):
            if office.contact and office.contact.website:
                logger.info(f"Enhancing {office.name} ({i+1}/{max_attempts})...")
                
                try:
                    enhanced = self._enhance_office_with_live_data(office)
                    if enhanced:
                        enhanced_count += 1
                        logger.info(f"✅ Enhanced {office.name}")
                    else:
                        logger.info(f"ℹ️  No additional data found for {office.name}")
                
                except Exception as e:
                    logger.warning(f"⚠️  Could not enhance {office.name}: {e}")
                
                # Rate limiting
                time.sleep(2)
        
        logger.info(f"🎯 Enhanced {enhanced_count}/{max_attempts} offices with live data")
    
    def _enhance_office_with_live_data(self, office: Office) -> bool:
        """Attempt to enhance a single office with live data"""
        enhanced = False
        
        try:
            # Try to fetch live data with SSL verification enabled
            response = self.session.get(office.contact.website, timeout=10)
            
            if response.status_code == 200:
                text_content = response.text
                
                # Extract additional phone numbers
                live_phones = extract_phone_numbers(text_content)
                if live_phones:
                    # Add new phones if found
                    existing_phones = [
                        office.contact.phone_general,
                        office.contact.phone_citizenship
                    ]
                    
                    for phone in live_phones[:2]:  # Max 2 additional phones
                        if phone not in existing_phones:
                            if not office.contact.phone_general:
                                office.contact.phone_general = phone
                                enhanced = True
                            elif not office.contact.phone_citizenship:
                                office.contact.phone_citizenship = phone
                                enhanced = True
                
                # Extract email addresses
                live_emails = extract_email_addresses(text_content)
                if live_emails and not office.contact.email:
                    office.contact.email = live_emails[0]
                    enhanced = True

                # Extract operating hours
                operating_hours = self._extract_operating_hours(text_content)
                if operating_hours:
                    office.operating_hours = operating_hours
                    enhanced = True

                # Extract services
                services = self._extract_services(text_content)
                if services:
                    office.services.extend(services)
                    enhanced = True
                
                # Update metadata if enhanced
                if enhanced:
                    office.metadata.data_quality = "factory_generated_enhanced_with_live"
                    office.metadata.last_scraped = datetime.now().isoformat()
                    office.update_completeness_score()

        except requests.exceptions.SSLError as e:
            logger.warning(f"SSL Error for {office.contact.website}: {e}. Trying without verification.")
            try:
                # If SSL fails, try without verification and log it
                response = self.session.get(office.contact.website, timeout=10, verify=False)
                if response.status_code == 200:
                    text_content = response.text
                
                    # Extract additional phone numbers
                    live_phones = extract_phone_numbers(text_content)
                    if live_phones:
                        # Add new phones if found
                        existing_phones = [
                            office.contact.phone_general,
                            office.contact.phone_citizenship
                        ]
                        
                        for phone in live_phones[:2]:  # Max 2 additional phones
                            if phone not in existing_phones:
                                if not office.contact.phone_general:
                                    office.contact.phone_general = phone
                                    enhanced = True
                                elif not office.contact.phone_citizenship:
                                    office.contact.phone_citizenship = phone
                                    enhanced = True
                    
                    # Extract email addresses
                    live_emails = extract_email_addresses(text_content)
                    if live_emails and not office.contact.email:
                        office.contact.email = live_emails[0]
                        enhanced = True

                    # Extract operating hours
                    operating_hours = self._extract_operating_hours(text_content)
                    if operating_hours:
                        office.operating_hours = operating_hours
                        enhanced = True

                    # Extract services
                    services = self._extract_services(text_content)
                    if services:
                        office.services.extend(services)
                        enhanced = True
                    
                    # Update metadata if enhanced
                    if enhanced:
                        office.metadata.data_quality = "factory_generated_enhanced_with_live"
                        office.metadata.last_scraped = datetime.now().isoformat()
                        office.update_completeness_score()

            except Exception as e:
                logger.error(f"Could not fetch {office.contact.website} even without SSL verification: {e}")
                return False
        
        except Exception:
            # Silently continue if live enhancement fails
            pass
        
        return enhanced

    def _extract_operating_hours(self, text_content: str) -> Optional[OperatingHours]:
        # Simple keyword-based extraction for operating hours
        # This is a placeholder and can be improved with more sophisticated parsing
        if "10:00 AM" in text_content and "5:00 PM" in text_content:
            return OperatingHours(
                monday_friday="10:00 AM - 5:00 PM",
                saturday="10:00 AM - 3:00 PM",
                sunday="closed",
                lunch_break="1:00 PM - 2:00 PM",
                notes="Hours may vary during festivals"
            )
        return None

    def _extract_services(self, text_content: str) -> List[Service]:
        # Simple keyword-based extraction for services
        # This is a placeholder and can be improved with more sophisticated parsing
        services = []
        if "citizenship" in text_content.lower():
            services.append(Service(service_id="citizenship_certificate", service_name="Citizenship Certificate", service_name_nepali="नागरिकता प्रमाणपत्र"))
        if "passport" in text_content.lower():
            services.append(Service(service_id="passport_app", service_name="E-Passport Application", service_name_nepali="राहदानी आवेदन"))
        if "driving license" in text_content.lower():
            services.append(Service(service_id="driving_license", service_name="Driving License", service_name_nepali="सवारी चालक अनुमतिपत्र"))
        return services
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        if not self.offices:
            return {}
        
        # Basic statistics
        total_offices = len(self.offices)
        avg_completeness = sum(office.metadata.completeness_score for office in self.offices) / total_offices
        
        # Contact information statistics
        offices_with_phone = len([o for o in self.offices if o.contact and o.contact.phone_general])
        offices_with_email = len([o for o in self.offices if o.contact and o.contact.email])
        offices_with_website = len([o for o in self.offices if o.contact and o.contact.website])
        
        # Service statistics
        total_services = sum(len(office.services) for office in self.offices)
        unique_service_types = set()
        for office in self.offices:
            for service in office.services:
                unique_service_types.add(service.service_id)
        
        # Staff statistics
        total_staff = sum(len(office.staff) for office in self.offices)
        
        # Province distribution
        province_distribution = {}
        for office in self.offices:
            if office.location and office.location.province:
                province = office.location.province
                province_distribution[province] = province_distribution.get(province, 0) + 1
        
        # Office type distribution
        office_type_distribution = {}
        for office in self.offices:
            office_type = office.type
            office_type_distribution[office_type] = office_type_distribution.get(office_type, 0) + 1
        
        # Service availability matrix
        service_matrix = {}
        for service_type in unique_service_types:
            offices_offering = len([
                o for o in self.offices 
                if any(s.service_id == service_type for s in o.services)
            ])
            service_matrix[service_type] = {
                'offices_count': offices_offering,
                'coverage_percentage': (offices_offering / total_offices) * 100
            }
        
        return {
            'overview': {
                'total_offices': total_offices,
                'total_services': total_services,
                'unique_service_types': len(unique_service_types),
                'total_staff_members': total_staff,
                'average_completeness': round(avg_completeness, 1)
            },
            'contact_coverage': {
                'offices_with_phone': offices_with_phone,
                'phone_coverage_percentage': round((offices_with_phone / total_offices) * 100, 1),
                'offices_with_email': offices_with_email,
                'email_coverage_percentage': round((offices_with_email / total_offices) * 100, 1),
                'offices_with_website': offices_with_website,
                'website_coverage_percentage': round((offices_with_website / total_offices) * 100, 1)
            },
            'geographic_distribution': province_distribution,
            'office_type_distribution': office_type_distribution,
            'service_availability_matrix': service_matrix,
            'top_offices_by_completeness': [
                {
                    'name': office.name,
                    'type': office.type,
                    'completeness': office.metadata.completeness_score,
                    'services_count': len(office.services),
                    'staff_count': len(office.staff)
                }
                for office in sorted(self.offices, key=lambda x: x.metadata.completeness_score, reverse=True)[:10]
            ]
        }
    
    def save_comprehensive_data(self, filename: str = None) -> str:
        """Save comprehensive data with detailed analysis"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/comprehensive_nepal_offices_{timestamp}.json"
        
        # Generate comprehensive report
        analysis_report = self.generate_comprehensive_report()
        
        output_data = {
            "metadata": {
                "version": SCHEMA_VERSION,
                "scraper_type": "comprehensive_factory_generated",
                "generation_date": datetime.now().isoformat(),
                "total_offices": len(self.offices),
                "data_quality": "comprehensive_with_live_enhancement",
                "coverage_scope": "national_government_offices"
            },
            "data_sources": [
                "Ministry of Home Affairs (MOHA)",
                "Department of Passport", 
                "Department of Transport Management",
                "Survey Department",
                "Land Revenue Offices",
                "Transport Management Offices",
                "Company Registrar Office"
            ],
            "analysis_report": analysis_report,
            "offices": [office.to_dict() for office in self.offices]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved comprehensive data to {filename}")
        return filename
    
    def run_comprehensive_scrape(self, enhance_with_live: bool = True, include_all_77_daos: bool = False, max_enhancement_attempts: int = 5):
        """Run the complete comprehensive scraping process"""
        mode_text = "ALL 77 DAOs + Other Offices" if include_all_77_daos else "Standard Comprehensive"
        logger.info(f"🚀 Starting {mode_text} Nepal Government Office Scraping")
        print("🇳🇵 Nepal Government Office Scraper")
        print(f"Mode: {mode_text}")
        print("=" * 70)
        
        try:
            # Step 1: Create all offices using factory
            if include_all_77_daos:
                print("📋 Step 1: Creating COMPLETE office database (all 77 DAOs + others)...")
            else:
                print("📋 Step 1: Creating comprehensive office database...")
                
            self.create_all_offices(include_all_77_daos=include_all_77_daos)
            print(f"✅ Created {len(self.offices)} government offices")
            
            # Step 2: Enhance with live data (optional)
            if enhance_with_live and len(self.offices) > 0:
                print("\n🌐 Step 2: Enhancing with live data...")
                self.enhance_with_live_data(max_attempts=min(max_enhancement_attempts, len(self.offices)))
                
                # Recalculate completeness after enhancement
                for office in self.offices:
                    office.update_completeness_score()
            
            # Step 3: Generate analysis
            print("\n📊 Step 3: Generating comprehensive analysis...")
            analysis = self.generate_comprehensive_report()
            
            # Step 4: Save results
            print("\n💾 Step 4: Saving comprehensive results...")
            output_file = self.save_comprehensive_data()
            
            # Display summary
            print(f"\n🎊 COMPREHENSIVE SCRAPING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"📄 Results saved to: {output_file}")
            print(f"🏢 Total offices: {analysis['overview']['total_offices']}")
            print(f"🛎️  Total services: {analysis['overview']['total_services']}")
            print(f"👥 Total staff: {analysis['overview']['total_staff_members']}")
            print(f"📈 Average completeness: {analysis['overview']['average_completeness']}%")
            print(f"📞 Phone coverage: {analysis['contact_coverage']['phone_coverage_percentage']}%")
            print(f"📧 Email coverage: {analysis['contact_coverage']['email_coverage_percentage']}%")
            
            print(f"\n🏆 Top 5 Offices by Completeness:")
            for i, office_info in enumerate(analysis['top_offices_by_completeness'][:5], 1):
                print(f"  {i}. {office_info['name']} - {office_info['completeness']:.1f}%")
            
            print(f"\n📍 Provincial Coverage:")
            for province, count in analysis['geographic_distribution'].items():
                print(f"  {province}: {count} offices")
            
            print(f"\n🎯 Service Coverage:")
            service_matrix = analysis['service_availability_matrix']
            for service_type, info in list(service_matrix.items())[:7]:  # Show top 7 services
                coverage = info['coverage_percentage']
                print(f"  {service_type.replace('_', ' ').title()}: {info['offices_count']} offices ({coverage:.1f}%)")
            
            print("=" * 60)
            
            return output_file
            
        except Exception as e:
            logger.error(f"Critical error in comprehensive scrape: {e}")
            print(f"❌ Comprehensive scraping failed: {e}")
            raise
    
    def get_offices_by_service(self, service_type: str) -> List[Office]:
        """Get all offices that provide a specific service"""
        matching_offices = []
        for office in self.offices:
            if any(service.service_id == service_type for service in office.services):
                matching_offices.append(office)
        return matching_offices
    
    def get_offices_by_province(self, province: str) -> List[Office]:
        """Get all offices in a specific province"""
        matching_offices = []
        for office in self.offices:
            if office.location and office.location.province == province:
                matching_offices.append(office)
        return matching_offices
    
    def get_offices_by_type(self, office_type: str) -> List[Office]:
        """Get all offices of a specific type"""
        matching_offices = []
        for office in self.offices:
            if office.type == office_type:
                matching_offices.append(office)
        return matching_offices


def main():
    """Main function to run the comprehensive scraper"""
    scraper = ComprehensiveNepalGovScraper()
    
    try:
        output_file = scraper.run_comprehensive_scrape(enhance_with_live=True)
        
        # Additional analysis examples
        print(f"\n🔍 Additional Analysis Examples:")
        
        # Passport service offices
        passport_offices = scraper.get_offices_by_service('passport')
        print(f"📘 Offices offering passport services: {len(passport_offices)}")
        
        # Driving license offices
        license_offices = scraper.get_offices_by_service('driving_license')
        print(f"🚗 Offices offering driving license services: {len(license_offices)}")
        
        # Land registration offices
        land_offices = scraper.get_offices_by_service('land_registration')
        print(f"🏡 Offices offering land registration services: {len(land_offices)}")
        
        # Bagmati Province offices
        bagmati_offices = scraper.get_offices_by_province('Bagmati Province')
        print(f"🏔️  Offices in Bagmati Province: {len(bagmati_offices)}")
        
        print(f"\n✅ Comprehensive analysis completed!")
        
    except Exception as e:
        print(f"❌ Comprehensive scraping failed: {e}")
        logger.error(f"Main execution failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()