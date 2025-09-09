#!/usr/bin/env python3
"""
Enhanced data models incorporating best practices from the reference code
Uses both dataclasses and Pydantic for validation
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, time
from enum import Enum
import json
import re

# Import from our config
try:
    from ..config import (
        DEFAULT_PASSPORT_FEES, DEFAULT_CITIZENSHIP_FEES,
        DEFAULT_PROCESSING_TIMES, KNOWN_DAO_KATHMANDU
    )
except ImportError:
    # Fallback values if config not available
    DEFAULT_PASSPORT_FEES = {"normal_34pg": 5000, "fast_track_34pg": 12000}
    DEFAULT_CITIZENSHIP_FEES = {"normal": 100, "urgent": 500}
    DEFAULT_PROCESSING_TIMES = {"passport": {"normal": "15-30 days"}}


class ServiceType(Enum):
    PASSPORT = "passport"
    CITIZENSHIP = "citizenship_certificate"
    OTHER = "other"


class OfficeType(Enum):
    DAO = "district_administration_office"
    CENTRAL_DEPT = "central_department"
    PASSPORT_DEPT = "passport_department"
    OTHER = "other"


class UrgencyLevel(Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    SAME_DAY = "same_day"


class DataQuality(Enum):
    VERIFIED = "verified"
    PARTIAL = "partial"
    ENHANCED_TEST = "enhanced_test"
    UNVERIFIED = "unverified"


@dataclass
class Contact:
    """Enhanced contact information with validation"""
    phone_general: Optional[str] = None
    phone_citizenship: Optional[str] = None
    phone_passport: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    fax: Optional[str] = None
    
    def __post_init__(self):
        """Validate and clean contact information"""
        # Clean phone numbers
        for field_name in ['phone_general', 'phone_citizenship', 'phone_passport']:
            phone = getattr(self, field_name)
            if phone:
                setattr(self, field_name, self._clean_phone_number(phone))
        
        # Validate email
        if self.email and not self._is_valid_email(self.email):
            self.email = None
    
    def _clean_phone_number(self, phone: str) -> str:
        """Clean and standardize phone numbers"""
        # Remove common separators and whitespace
        cleaned = re.sub(r'[-\s\(\)]', '', phone)
        
        # Handle Nepal country code
        if cleaned.startswith('+977'):
            cleaned = cleaned[4:]
        elif cleaned.startswith('977'):
            cleaned = cleaned[3:]
        
        # Ensure it starts with area code
        if not cleaned.startswith('0') and len(cleaned) == 7:
            cleaned = '01' + cleaned
            
        return cleaned
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def get_phones_list(self) -> List[str]:
        """Get all phone numbers as a list"""
        phones = []
        for phone in [self.phone_general, self.phone_citizenship, self.phone_passport]:
            if phone:
                phones.append(phone)
        return phones
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Location:
    """Enhanced location with coordinate support"""
    address: str
    district: str
    province: str
    address_nepali: Optional[str] = None
    ward_no: Optional[int] = None
    municipality: Optional[str] = None
    postal_code: Optional[str] = None
    coordinates: Dict[str, Optional[float]] = field(default_factory=lambda: {"latitude": None, "longitude": None})
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Staff:
    """Enhanced staff information"""
    name: str
    position: str
    section: Optional[str] = None
    contact: Optional[str] = None
    name_nepali: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Fee:
    """Fee structure for services"""
    amount: float
    currency: str = "NPR"
    processing_days: str = ""
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProcessingTimes:
    """Detailed processing time breakdown"""
    document_submission: Optional[str] = None
    biometric_capture: Optional[str] = None
    verification_process: Optional[str] = None
    total_normal: Optional[str] = None
    total_urgent: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ServiceFees:
    """Comprehensive fee structure"""
    normal_processing: Optional[Fee] = None
    urgent_processing: Optional[Fee] = None
    same_day: Optional[Fee] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.normal_processing:
            result['normal_processing'] = self.normal_processing.to_dict()
        if self.urgent_processing:
            result['urgent_processing'] = self.urgent_processing.to_dict()
        if self.same_day:
            result['same_day'] = self.same_day.to_dict()
        return result


@dataclass
class Section:
    """Office section information"""
    section_name: str
    staff: List[Staff] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'section_name': self.section_name,
            'staff': [staff_member.to_dict() for staff_member in self.staff]
        }


@dataclass
class Service:
    """Enhanced service information"""
    service_id: str
    service_name: str
    service_name_nepali: Optional[str] = None
    sections: List[Section] = field(default_factory=list)
    fees: Optional[ServiceFees] = None
    processing_times: Optional[ProcessingTimes] = None
    required_documents: List[str] = field(default_factory=list)
    service_procedures: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'service_id': self.service_id,
            'service_name': self.service_name
        }
        
        if self.service_name_nepali:
            result['service_name_nepali'] = self.service_name_nepali
        if self.sections:
            result['sections'] = [section.to_dict() for section in self.sections]
        if self.fees:
            result['fees'] = self.fees.to_dict()
        if self.processing_times:
            result['processing_times'] = self.processing_times.to_dict()
        if self.required_documents:
            result['required_documents'] = self.required_documents
        if self.service_procedures:
            result['service_procedures'] = self.service_procedures
            
        return result


@dataclass
class OperatingHours:
    """Enhanced operating hours"""
    monday_friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: str = "closed"
    lunch_break: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Metadata:
    """Enhanced metadata with quality tracking"""
    data_source: str
    last_scraped: str
    data_quality: str
    verification_status: str = "unverified"
    schema_version: str = "1.0.0"
    completeness_score: float = 0.0
    scraper_version: str = "enhanced_1.0.0"
    extraction_method: str = "mixed"  # "requests", "selenium", "mixed"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Office:
    """Enhanced office model with comprehensive information"""
    id: str
    type: str
    name: str
    name_nepali: Optional[str] = None
    services: List[Service] = field(default_factory=list)
    location: Optional[Location] = None
    contact: Optional[Contact] = None
    staff: List[Staff] = field(default_factory=list)
    operating_hours: Optional[OperatingHours] = None
    metadata: Optional[Metadata] = None
    
    def calculate_completeness_score(self) -> float:
        """Calculate data completeness as a percentage"""
        total_fields = 10  # Base important fields
        filled_fields = 0
        
        # Check essential fields
        if self.name: filled_fields += 1
        if self.location and self.location.address: filled_fields += 1
        if self.location and self.location.district: filled_fields += 1
        if self.contact and self.contact.phone_general: filled_fields += 1
        if self.contact and self.contact.email: filled_fields += 1
        if self.services: filled_fields += 1
        if self.staff: filled_fields += 1
        if self.operating_hours: filled_fields += 1
        if self.contact and self.contact.website: filled_fields += 1
        if self.name_nepali: filled_fields += 1
        
        return (filled_fields / total_fields) * 100
    
    def update_completeness_score(self):
        """Update the completeness score in metadata"""
        if self.metadata:
            self.metadata.completeness_score = self.calculate_completeness_score()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            'id': self.id,
            'type': self.type,
            'name': self.name
        }
        
        if self.name_nepali:
            result['name_nepali'] = self.name_nepali
        if self.location:
            result['location'] = self.location.to_dict()
        if self.contact:
            result['contact'] = self.contact.to_dict()
        if self.services:
            result['services'] = [service.to_dict() for service in self.services]
        if self.staff:
            result['staff'] = [staff_member.to_dict() for staff_member in self.staff]
        if self.operating_hours:
            result['operating_hours'] = self.operating_hours.to_dict()
        if self.metadata:
            result['metadata'] = self.metadata.to_dict()
            
        return result


def create_enhanced_dao_kathmandu() -> Office:
    """Create an enhanced DAO Kathmandu office with known data"""
    
    # Create contact information
    contact = Contact(
        phone_general="01-5362828",
        phone_citizenship="01-5367691",
        website="https://daokathmandu.moha.gov.np"
    )
    
    # Create location
    location = Location(
        address="Babarmahal, Kathmandu, Nepal",
        district="Kathmandu",
        province="Bagmati Province"
    )
    
    # Create staff
    staff_list = [
        Staff(
            name="Rabin Kumar Rai",
            position="Administrative Officer", 
            section="Citizenship Section"
        )
    ]
    
    # Create citizenship service with fees
    citizenship_fees = ServiceFees(
        normal_processing=Fee(
            amount=100.0,
            processing_days="15-20 days",
            description="Normal citizenship certificate processing"
        ),
        urgent_processing=Fee(
            amount=500.0,
            processing_days="3-5 days",
            description="Urgent citizenship certificate processing"
        )
    )
    
    citizenship_times = ProcessingTimes(
        document_submission="30 minutes",
        verification_process="5-7 days",
        total_normal="15-20 days",
        total_urgent="3-5 days"
    )
    
    citizenship_service = Service(
        service_id="citizenship_certificate",
        service_name="Citizenship Certificate",
        service_name_nepali="नागरिकता प्रमाणपत्र",
        sections=[Section(
            section_name="Citizenship Section",
            staff=[staff_list[0]]
        )],
        fees=citizenship_fees,
        processing_times=citizenship_times,
        required_documents=[
            "Birth certificate",
            "Parents' citizenship certificates", 
            "Recommendation letter from ward office",
            "Passport size photos (2 copies)"
        ]
    )
    
    # Create passport service with fees
    passport_fees = ServiceFees(
        normal_processing=Fee(
            amount=5000.0,
            processing_days="15-30 days",
            description="Normal 34-page passport"
        ),
        urgent_processing=Fee(
            amount=12000.0,
            processing_days="3-4 days", 
            description="Fast-track 34-page passport"
        ),
        same_day=Fee(
            amount=15000.0,
            processing_days="same day",
            description="Same-day 34-page passport"
        )
    )
    
    passport_times = ProcessingTimes(
        document_submission="30 minutes",
        biometric_capture="15 minutes",
        verification_process="7-10 days",
        total_normal="15-30 days",
        total_urgent="3-4 days"
    )
    
    passport_service = Service(
        service_id="passport_application",
        service_name="E-Passport Application",
        service_name_nepali="राहदानी आवेदन",
        sections=[Section(section_name="Passport Section", staff=[])],
        fees=passport_fees,
        processing_times=passport_times,
        required_documents=[
            "Citizenship certificate",
            "Passport size photos (2 copies)",
            "Application form",
            "Birth certificate (if applying for first time)"
        ]
    )
    
    # Create operating hours
    operating_hours = OperatingHours(
        monday_friday="10:00 AM - 5:00 PM",
        saturday="10:00 AM - 3:00 PM",
        lunch_break="1:00 PM - 2:00 PM",
        notes="Hours may vary during festivals"
    )
    
    # Create metadata
    metadata = Metadata(
        data_source="daokathmandu.moha.gov.np",
        last_scraped=datetime.now().isoformat(),
        data_quality="enhanced_test",
        verification_status="partially_verified",
        extraction_method="enhanced_mixed"
    )
    
    # Create the office
    office = Office(
        id="dao_kathmandu_enhanced",
        type="district_administration_office",
        name="District Administration Office, Kathmandu",
        name_nepali="जिल्ला प्रशासन कार्यालय, काठमाडौं",
        services=[citizenship_service, passport_service],
        location=location,
        contact=contact,
        staff=staff_list,
        operating_hours=operating_hours,
        metadata=metadata
    )
    
    # Update completeness score
    office.update_completeness_score()
    
    return office


def create_passport_department() -> Office:
    """Create the central passport department office"""
    
    contact = Contact(
        phone_general="+977-1-5970330",
        phone_passport="+977-1-5970329",
        email="communication@nepalpassport.gov.np",
        website="https://nepalpassport.gov.np"
    )
    
    location = Location(
        address="Tripureshwor, Kathmandu, Nepal",
        district="Kathmandu",
        province="Bagmati Province"
    )
    
    staff_list = [
        Staff(
            name="Prakash Mani Paudel",
            position="Director General",
            contact="dg@nepalpassport.gov.np"
        )
    ]
    
    # Create comprehensive passport service
    passport_fees = ServiceFees(
        normal_processing=Fee(amount=5000.0, processing_days="15-30 days"),
        urgent_processing=Fee(amount=12000.0, processing_days="3-4 days"),
        same_day=Fee(amount=15000.0, processing_days="same day")
    )
    
    passport_service = Service(
        service_id="passport_application",
        service_name="E-Passport Application",
        sections=[Section(
            section_name="Central Passport Office",
            staff=staff_list
        )],
        fees=passport_fees
    )
    
    metadata = Metadata(
        data_source="nepalpassport.gov.np",
        last_scraped=datetime.now().isoformat(),
        data_quality="enhanced_test",
        verification_status="verified"
    )
    
    office = Office(
        id="passport_dept_main",
        type="central_department",
        name="Department of Passport, Tripureshwor",
        name_nepali="राहदानी विभाग, त्रिपुरेश्वर",
        services=[passport_service],
        location=location,
        contact=contact,
        staff=staff_list,
        metadata=metadata
    )
    
    office.update_completeness_score()
    return office