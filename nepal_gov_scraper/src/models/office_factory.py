#!/usr/bin/env python3
"""
Office Factory for creating comprehensive government office data
Generates 20+ offices with complete service information
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.enhanced_models import (
    Office, Contact, Location, Staff, Service, Section,
    ServiceFees, Fee, ProcessingTimes, OperatingHours, Metadata
)
from config_extended import (
    ALL_EXTENDED_OFFICES, EXTENDED_SERVICE_DEFINITIONS,
    OFFICE_SERVICE_MAPPING, SCHEMA_VERSION
)


class GovernmentOfficeFactory:
    """Factory for creating comprehensive government office data"""
    
    def __init__(self):
        self.service_definitions = EXTENDED_SERVICE_DEFINITIONS
        self.office_service_mapping = OFFICE_SERVICE_MAPPING
    
    def create_all_offices(self) -> List[Office]:
        """Create all 20+ government offices with comprehensive data"""
        offices = []
        
        for office_data in ALL_EXTENDED_OFFICES:
            office = self.create_office_from_data(office_data)
            if office:
                offices.append(office)
        
        print(f"✅ Created {len(offices)} comprehensive government offices")
        return offices
    
    def create_office_from_data(self, office_data: Dict[str, Any]) -> Optional[Office]:
        """Create a complete office object from configuration data"""
        try:
            # Generate office ID
            office_id = self._generate_office_id(office_data['name'])
            
            # Create location
            location = Location(
                address=office_data.get('address', 'Address not specified'),
                district=office_data['district'],
                province=office_data['province'],
                coordinates={"latitude": None, "longitude": None}
            )
            
            # Create contact
            phones = office_data.get('phones', [])
            contact = Contact(
                phone_general=phones[0] if len(phones) > 0 else None,
                phone_citizenship=phones[1] if len(phones) > 1 else None,
                email=office_data.get('email'),
                website=office_data.get('url', 'https://moha.gov.np')
            )
            
            # Create staff
            staff_list = []
            staff_data = office_data.get('staff', [])
            for staff_info in staff_data:
                staff_member = Staff(
                    name=staff_info['name'],
                    position=staff_info['position'],
                    section=staff_info.get('section')
                )
                staff_list.append(staff_member)
            
            # Create services based on office type
            services = self._create_services_for_office(office_data)
            
            # Create operating hours
            operating_hours = OperatingHours(
                monday_friday="10:00 AM - 5:00 PM",
                saturday="10:00 AM - 3:00 PM", 
                sunday="closed",
                lunch_break="1:00 PM - 2:00 PM",
                notes="Hours may vary during festivals and public holidays"
            )
            
            # Create metadata
            metadata = Metadata(
                data_source=office_data.get('url', 'config_data'),
                last_scraped=datetime.now().isoformat(),
                data_quality="comprehensive_factory_generated",
                verification_status="verified",
                schema_version=SCHEMA_VERSION,
                scraper_version="office_factory_1.0.0",
                extraction_method="factory_generated"
            )
            
            # Create the office
            office = Office(
                id=office_id,
                type=office_data.get('office_type', 'district_administration_office'),
                name=office_data['name'],
                name_nepali=office_data.get('name_nepali'),
                services=services,
                location=location,
                contact=contact,
                staff=staff_list,
                operating_hours=operating_hours,
                metadata=metadata
            )
            
            # Calculate completeness score
            office.update_completeness_score()
            
            return office
            
        except Exception as e:
            print(f"❌ Error creating office {office_data.get('name', 'Unknown')}: {e}")
            return None
    
    def _create_services_for_office(self, office_data: Dict[str, Any]) -> List[Service]:
        """Create services based on office type and specified services"""
        services = []
        
        # Get office type and specified services
        office_type = office_data.get('office_type', 'district_administration_office')
        specified_services = office_data.get('services', [])
        
        # Get default services for office type
        default_services = self.office_service_mapping.get(office_type, [])
        
        # Combine specified and default services
        all_service_types = list(set(specified_services + default_services))
        
        for service_type in all_service_types:
            if service_type in self.service_definitions:
                service = self._create_service(service_type, office_data)
                if service:
                    services.append(service)
        
        return services
    
    def _create_service(self, service_type: str, office_data: Dict[str, Any]) -> Optional[Service]:
        """Create a comprehensive service object"""
        try:
            service_def = self.service_definitions[service_type]
            
            # Create service fees
            fees_data = service_def.get('fees', {})
            fees = ServiceFees()
            
            if 'normal' in fees_data:
                fees.normal_processing = Fee(
                    amount=float(fees_data['normal']),
                    processing_days=service_def['processing_days'].get('normal', '7-15 days'),
                    description=f"Normal {service_def['name_en'].lower()} processing"
                )
            
            if 'urgent' in fees_data:
                fees.urgent_processing = Fee(
                    amount=float(fees_data['urgent']),
                    processing_days=service_def['processing_days'].get('urgent', '3-5 days'),
                    description=f"Urgent {service_def['name_en'].lower()} processing"
                )
            
            if 'same_day' in fees_data:
                fees.same_day = Fee(
                    amount=float(fees_data['same_day']),
                    processing_days=service_def['processing_days'].get('same_day', 'same day'),
                    description=f"Same-day {service_def['name_en'].lower()} processing"
                )
            
            # Handle special fee cases
            if service_type in ['driving_license', 'vehicle_registration', 'business_license', 'company_registration']:
                fees = self._create_special_fees(service_type, fees_data, service_def)
            
            # Create processing times
            processing_times = ProcessingTimes(
                document_submission="30 minutes",
                verification_process=service_def['processing_days'].get('normal', '7-15 days'),
                total_normal=service_def['processing_days'].get('normal', '7-15 days'),
                total_urgent=service_def['processing_days'].get('urgent', '3-5 days') if 'urgent' in service_def['processing_days'] else None
            )
            
            # Create sections with staff
            sections = self._create_service_sections(service_type, office_data)
            
            # Create the service
            service = Service(
                service_id=service_type,
                service_name=service_def['name_en'],
                service_name_nepali=service_def.get('name_np'),
                sections=sections,
                fees=fees,
                processing_times=processing_times,
                required_documents=service_def.get('required_docs', []),
                service_procedures=self._get_service_procedures(service_type)
            )
            
            return service
            
        except Exception as e:
            print(f"❌ Error creating service {service_type}: {e}")
            return None
    
    def _create_special_fees(self, service_type: str, fees_data: Dict[str, Any], service_def: Dict[str, Any]) -> ServiceFees:
        """Create special fee structures for complex services"""
        fees = ServiceFees()
        
        if service_type == 'driving_license':
            fees.normal_processing = Fee(
                amount=float(fees_data.get('smart_license', 1500)),
                processing_days=service_def['processing_days'].get('normal', '7-15 days'),
                description="Smart driving license"
            )
            if 'urgent' in service_def['processing_days']:
                fees.urgent_processing = Fee(
                    amount=float(fees_data.get('smart_license', 1500)) * 1.5,
                    processing_days=service_def['processing_days']['urgent'],
                    description="Urgent smart driving license"
                )
        
        elif service_type == 'vehicle_registration':
            # Use car registration as default
            fees.normal_processing = Fee(
                amount=float(fees_data.get('car', 15000)),
                processing_days=service_def['processing_days'].get('normal', '3-7 days'),
                description="Vehicle registration (car)"
            )
        
        elif service_type == 'business_license':
            fees.normal_processing = Fee(
                amount=float(fees_data.get('medium', 2000)),
                processing_days=service_def['processing_days'].get('normal', '7-15 days'),
                description="Medium business license"
            )
        
        elif service_type == 'company_registration':
            fees.normal_processing = Fee(
                amount=float(fees_data.get('pvt_limited', 5000)),
                processing_days=service_def['processing_days'].get('normal', '15-21 days'),
                description="Private limited company registration"
            )
        
        return fees
    
    def _create_service_sections(self, service_type: str, office_data: Dict[str, Any]) -> List[Section]:
        """Create appropriate sections for each service type"""
        sections = []
        
        # Map service types to section names
        section_mapping = {
            'citizenship': 'Citizenship Section',
            'passport': 'Passport Section',
            'driving_license': 'License Section',
            'vehicle_registration': 'Registration Section',
            'land_registration': 'Registration Section',
            'company_registration': 'Company Registration Section',
            'business_license': 'Licensing Section'
        }
        
        section_name = section_mapping.get(service_type, f"{service_type.replace('_', ' ').title()} Section")
        
        # Find relevant staff for this section
        relevant_staff = []
        office_staff = office_data.get('staff', [])
        
        for staff_info in office_staff:
            staff_section = staff_info.get('section', '')
            if (service_type in staff_section.lower() or 
                any(word in staff_section.lower() for word in service_type.split('_'))):
                staff_member = Staff(
                    name=staff_info['name'],
                    position=staff_info['position'],
                    section=staff_section or section_name
                )
                relevant_staff.append(staff_member)
        
        # If no specific staff found, create section without staff
        section = Section(
            section_name=section_name,
            staff=relevant_staff
        )
        sections.append(section)
        
        return sections
    
    def _get_service_procedures(self, service_type: str) -> List[str]:
        """Get standard procedures for each service type"""
        procedures = {
            'citizenship': [
                "Submit application with required documents",
                "Document verification by officer", 
                "Field verification (if required)",
                "Approval and certificate printing",
                "Certificate collection"
            ],
            'passport': [
                "Online application submission",
                "Document verification",
                "Biometric data collection", 
                "Application processing",
                "Passport printing and dispatch"
            ],
            'driving_license': [
                "Trial license application",
                "Written examination",
                "Practical driving test",
                "Medical examination",
                "Smart license issuance"
            ],
            'vehicle_registration': [
                "Document submission", 
                "Vehicle inspection",
                "Tax payment",
                "Registration processing",
                "Number plate issuance"
            ],
            'land_registration': [
                "Document verification",
                "Survey report review",
                "Tax calculation and payment",
                "Registration in government records",
                "Certificate issuance"
            ],
            'company_registration': [
                "Name reservation",
                "Document submission",
                "Legal compliance check",
                "Registration approval",
                "Certificate issuance"
            ]
        }
        
        return procedures.get(service_type, [
            "Application submission",
            "Document verification", 
            "Processing and approval",
            "Certificate/License issuance"
        ])
    
    def _generate_office_id(self, office_name: str) -> str:
        """Generate a clean office ID from name"""
        # Remove common prefixes and clean up
        clean_name = office_name.lower()
        clean_name = clean_name.replace('district administration office,', 'dao')
        clean_name = clean_name.replace('district administration office', 'dao')
        clean_name = clean_name.replace('department of', 'dept')
        clean_name = clean_name.replace('office of', '')
        clean_name = clean_name.replace('transport management office,', 'tmo')
        clean_name = clean_name.replace('land revenue office,', 'lro')
        
        # Replace spaces and punctuation with underscores
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', clean_name)
        clean_name = re.sub(r'_+', '_', clean_name)  # Remove multiple underscores
        clean_name = clean_name.strip('_')  # Remove leading/trailing underscores
        
        return clean_name
    
    def create_dao_offices(self) -> List[Office]:
        """Create only DAO offices"""
        from config_extended import EXTENDED_DAO_OFFICES
        offices = []
        for office_data in EXTENDED_DAO_OFFICES:
            office = self.create_office_from_data(office_data)
            if office:
                offices.append(office)
        return offices
    
    def create_central_departments(self) -> List[Office]:
        """Create only central departments"""
        from config_extended import CENTRAL_DEPARTMENTS
        offices = []
        for office_data in CENTRAL_DEPARTMENTS:
            office = self.create_office_from_data(office_data)
            if office:
                offices.append(office)
        return offices
    
    def create_specialized_offices(self) -> List[Office]:
        """Create transport, land, and other specialized offices"""
        from config_extended import LAND_REVENUE_OFFICES, TRANSPORT_OFFICES, COMPANY_REGISTRAR_OFFICES
        offices = []
        
        all_specialized = LAND_REVENUE_OFFICES + TRANSPORT_OFFICES + COMPANY_REGISTRAR_OFFICES
        
        for office_data in all_specialized:
            office = self.create_office_from_data(office_data)
            if office:
                offices.append(office)
        
        return offices


def create_comprehensive_office_list() -> List[Office]:
    """Create comprehensive list of 20+ Nepal government offices"""
    factory = GovernmentOfficeFactory()
    return factory.create_all_offices()


def main():
    """Test the office factory"""
    print("🏭 Government Office Factory Test")
    print("=" * 50)
    
    factory = GovernmentOfficeFactory()
    offices = factory.create_all_offices()
    
    print(f"\n📊 Factory Results:")
    print(f"Total offices created: {len(offices)}")
    
    # Group by office type
    office_types = {}
    for office in offices:
        office_type = office.type
        if office_type not in office_types:
            office_types[office_type] = 0
        office_types[office_type] += 1
    
    print(f"\n🏢 Office Types:")
    for office_type, count in office_types.items():
        print(f"  {office_type}: {count} offices")
    
    # Calculate average completeness
    if offices:
        avg_completeness = sum(office.metadata.completeness_score for office in offices) / len(offices)
        print(f"\n📈 Average completeness: {avg_completeness:.1f}%")
    
    # Show sample offices
    print(f"\n🏆 Sample Offices:")
    for i, office in enumerate(offices[:5], 1):
        print(f"  {i}. {office.name}")
        print(f"     Services: {len(office.services)}, Staff: {len(office.staff)}")
        print(f"     Completeness: {office.metadata.completeness_score:.1f}%")
    
    print(f"\n✅ Office factory test completed!")


if __name__ == "__main__":
    main()