#!/usr/bin/env python3
"""
Extended configuration with 20+ Nepal government offices
Covers passport, license, land registration, and other services
"""

# Import base configuration
from config import *

# --- Extended Office Data (20+ Offices) ---

# District Administration Offices (DAOs) - Major Districts
EXTENDED_DAO_OFFICES = [
    {
        "name": "District Administration Office, Kathmandu",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, काठमाडौं",
        "url": "https://daokathmandu.moha.gov.np",
        "district": "Kathmandu",
        "province": "Bagmati Province",
        "address": "Babarmahal, Kathmandu",
        "phones": ["01-5362828", "01-5367691"],
        "services": ["citizenship", "passport", "licenses"],
        "staff": [{"name": "Rabin Kumar Rai", "position": "Administrative Officer", "section": "Citizenship Section"}]
    },
    {
        "name": "District Administration Office, Lalitpur",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, ललितपुर",
        "url": "https://daolalitpur.moha.gov.np",
        "district": "Lalitpur",
        "province": "Bagmati Province",
        "address": "Pulchowk, Lalitpur",
        "phones": ["01-5521821", "01-5521822"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Bhaktapur",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, भक्तपुर",
        "url": "https://daobhaktapur.moha.gov.np",
        "district": "Bhaktapur",
        "province": "Bagmati Province",
        "address": "Bhaktapur Durbar Square, Bhaktapur",
        "phones": ["01-6610477", "01-6610478"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Chitwan",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, चितवन",
        "url": "https://daochitwan.moha.gov.np",
        "district": "Chitwan",
        "province": "Bagmati Province",
        "address": "Bharatpur-10, Chitwan",
        "phones": ["056-527020", "056-527021"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Pokhara",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, कास्की",
        "url": "https://daokaski.moha.gov.np", 
        "district": "Kaski",
        "province": "Gandaki Province",
        "address": "Pokhara-8, Kaski",
        "phones": ["061-521045", "061-521046"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Biratnagar",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, मोरङ",
        "url": "https://daomorang.moha.gov.np",
        "district": "Morang",
        "province": "Koshi Province",
        "address": "Biratnagar-8, Morang",
        "phones": ["021-522045", "021-522046"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Birgunj",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, पर्सा",
        "url": "https://daoparsa.moha.gov.np",
        "district": "Parsa",
        "province": "Madhesh Province",
        "address": "Birgunj-14, Parsa",
        "phones": ["051-522789", "051-522790"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Butwal",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, रुपन्देही",
        "url": "https://daorupandehi.moha.gov.np",
        "district": "Rupandehi",
        "province": "Lumbini Province",
        "address": "Butwal-11, Rupandehi",
        "phones": ["071-540205", "071-540206"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Nepalgunj",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, बाँके",
        "url": "https://daobanke.moha.gov.np",
        "district": "Banke",
        "province": "Lumbini Province", 
        "address": "Nepalgunj-7, Banke",
        "phones": ["081-520145", "081-520146"],
        "services": ["citizenship", "passport", "licenses"]
    },
    {
        "name": "District Administration Office, Dharan",
        "name_nepali": "जिल्ला प्रशासन कार्यालय, सुनसरी",
        "url": "https://daosunsari.moha.gov.np",
        "district": "Sunsari",
        "province": "Koshi Province",
        "address": "Dharan-8, Sunsari",
        "phones": ["025-520789", "025-520790"],
        "services": ["citizenship", "passport", "licenses"]
    }
]

# Central Departments and Specialized Offices
CENTRAL_DEPARTMENTS = [
    {
        "name": "Department of Passport",
        "name_nepali": "राहदानी विभाग",
        "url": "https://nepalpassport.gov.np",
        "office_type": "passport_department",
        "address": "Tripureshwor, Kathmandu",
        "district": "Kathmandu",
        "province": "Bagmati Province",
        "phones": ["+977-1-5970330", "+977-1-5970329"],
        "email": "communication@nepalpassport.gov.np",
        "services": ["passport"],
        "staff": [{"name": "Prakash Mani Paudel", "position": "Director General"}]
    },
    {
        "name": "Department of Transport Management",
        "name_nepali": "यातायात व्यवस्थापन विभाग",
        "url": "https://dotm.gov.np",
        "office_type": "transport_department",
        "address": "Minbhawan, Kathmandu",
        "district": "Kathmandu", 
        "province": "Bagmati Province",
        "phones": ["01-4211081", "01-4211082"],
        "email": "info@dotm.gov.np",
        "services": ["driving_license", "vehicle_registration", "route_permit"],
        "staff": [{"name": "Mahindra Raj Silwal", "position": "Director General"}]
    },
    {
        "name": "Survey Department",
        "name_nepali": "नापी विभाग",
        "url": "https://dos.gov.np",
        "office_type": "survey_department",
        "address": "Minbhawan, Kathmandu",
        "district": "Kathmandu",
        "province": "Bagmati Province", 
        "phones": ["01-4211025", "01-4211026"],
        "email": "info@dos.gov.np",
        "services": ["land_survey", "mapping", "geodetic_survey"],
        "staff": [{"name": "Susheel Dangol", "position": "Director General"}]
    },
    {
        "name": "Department of Land Management and Archive",
        "name_nepali": "भूमि व्यवस्थापन तथा अभिलेख विभाग",
        "url": "https://dolma.gov.np",
        "office_type": "land_department",
        "address": "Dillibazar, Kathmandu",
        "district": "Kathmandu",
        "province": "Bagmati Province",
        "phones": ["01-4478231", "01-4478232"],
        "email": "info@dolma.gov.np",
        "services": ["land_registration", "land_records", "property_valuation"],
        "staff": [{"name": "Kedar Prasad Khanal", "position": "Director General"}]
    }
]

# Land Revenue Offices (Major Districts)
LAND_REVENUE_OFFICES = [
    {
        "name": "Land Revenue Office, Kathmandu",
        "name_nepali": "मालपोत कार्यालय, काठमाडौं",
        "url": "https://lrokathmandu.gov.np",
        "office_type": "land_revenue_office",
        "address": "Dillibazar, Kathmandu",
        "district": "Kathmandu",
        "province": "Bagmati Province",
        "phones": ["01-4412345", "01-4412346"],
        "services": ["land_registration", "property_transfer", "tax_collection"],
        "staff": [{"name": "Ram Prasad Sharma", "position": "Registrar"}]
    },
    {
        "name": "Land Revenue Office, Lalitpur", 
        "name_nepali": "मालपोत कार्यालय, ललितपुर",
        "url": "https://lrolalitpur.gov.np",
        "office_type": "land_revenue_office", 
        "address": "Pulchowk, Lalitpur",
        "district": "Lalitpur",
        "province": "Bagmati Province",
        "phones": ["01-5521900", "01-5521901"],
        "services": ["land_registration", "property_transfer", "tax_collection"]
    },
    {
        "name": "Land Revenue Office, Pokhara",
        "name_nepali": "मालपोत कार्यालय, कास्की",
        "url": "https://lrokaski.gov.np",
        "office_type": "land_revenue_office",
        "address": "Pokhara-9, Kaski", 
        "district": "Kaski",
        "province": "Gandaki Province",
        "phones": ["061-521900", "061-521901"],
        "services": ["land_registration", "property_transfer", "tax_collection"]
    }
]

# Transport Management Offices (Major Cities)
TRANSPORT_OFFICES = [
    {
        "name": "Transport Management Office, Kathmandu",
        "name_nepali": "यातायात व्यवस्थापन कार्यालय, काठमाडौं",
        "url": "https://tmokathamndu.gov.np",
        "office_type": "transport_office",
        "address": "Ekantakuna, Lalitpur",
        "district": "Lalitpur",
        "province": "Bagmati Province",
        "phones": ["01-5970525", "01-5970526"],
        "services": ["driving_license", "vehicle_registration", "license_renewal"],
        "staff": [{"name": "Bijay Kumar Yadav", "position": "Chief"}]
    },
    {
        "name": "Transport Management Office, Pokhara", 
        "name_nepali": "यातायात व्यवस्थापन कार्यालय, कास्की",
        "url": "https://tmokaski.gov.np",
        "office_type": "transport_office",
        "address": "Pokhara-10, Kaski",
        "district": "Kaski", 
        "province": "Gandaki Province",
        "phones": ["061-521525", "061-521526"],
        "services": ["driving_license", "vehicle_registration", "license_renewal"]
    },
    {
        "name": "Transport Management Office, Biratnagar",
        "name_nepali": "यातायात व्यवस्थापन कार्यालय, मोरङ",
        "url": "https://tmomorang.gov.np", 
        "office_type": "transport_office",
        "address": "Biratnagar-10, Morang",
        "district": "Morang",
        "province": "Koshi Province",
        "phones": ["021-522525", "021-522526"],
        "services": ["driving_license", "vehicle_registration", "license_renewal"]
    }
]

# Company Registrar Offices
COMPANY_REGISTRAR_OFFICES = [
    {
        "name": "Office of Company Registrar",
        "name_nepali": "कम्पनी रजिष्ट्रार कार्यालय", 
        "url": "https://ocr.gov.np",
        "office_type": "company_registrar",
        "address": "Tripureshwor, Kathmandu",
        "district": "Kathmandu",
        "province": "Bagmati Province",
        "phones": ["01-4259109", "01-4259110"],
        "email": "info@ocr.gov.np",
        "services": ["company_registration", "business_license", "trademark_registration"],
        "staff": [{"name": "Rajesh Kumar Jha", "position": "Registrar"}]
    }
]

# All Extended Offices Combined
ALL_EXTENDED_OFFICES = (
    EXTENDED_DAO_OFFICES + 
    CENTRAL_DEPARTMENTS + 
    LAND_REVENUE_OFFICES + 
    TRANSPORT_OFFICES + 
    COMPANY_REGISTRAR_OFFICES
)

# Service Type Definitions
EXTENDED_SERVICE_DEFINITIONS = {
    "citizenship": {
        "name_en": "Citizenship Certificate",
        "name_np": "नागरिकता प्रमाणपत्र",
        "fees": {"normal": 100, "urgent": 500},
        "processing_days": {"normal": "15-20", "urgent": "3-5"},
        "required_docs": [
            "Birth certificate",
            "Parents' citizenship certificates",
            "Recommendation letter from ward office",
            "Passport size photos (2 copies)"
        ]
    },
    "passport": {
        "name_en": "E-Passport Application", 
        "name_np": "राहदानी आवेदन",
        "fees": {"normal": 5000, "urgent": 12000, "same_day": 15000},
        "processing_days": {"normal": "15-30", "urgent": "3-4", "same_day": "1"},
        "required_docs": [
            "Citizenship certificate",
            "Passport size photos (2 copies)", 
            "Application form",
            "Birth certificate (for first time)"
        ]
    },
    "driving_license": {
        "name_en": "Driving License",
        "name_np": "सवारी चालक अनुमतिपत्र",
        "fees": {"trial": 1000, "smart_license": 1500, "renewal": 700},
        "processing_days": {"normal": "7-15", "urgent": "3-5"},
        "required_docs": [
            "Citizenship certificate",
            "Medical certificate", 
            "Passport size photos (4 copies)",
            "Trial form (for new license)"
        ]
    },
    "vehicle_registration": {
        "name_en": "Vehicle Registration",
        "name_np": "सवारी दर्ता",
        "fees": {"car": 15000, "motorcycle": 3000, "truck": 25000},
        "processing_days": {"normal": "3-7"},
        "required_docs": [
            "Ownership certificate",
            "Insurance papers",
            "Citizenship certificate",
            "Tax clearance"
        ]
    },
    "land_registration": {
        "name_en": "Land Registration",
        "name_np": "जग्गा दर्ता",
        "fees": {"registration": "2% of value", "mutation": 1000},
        "processing_days": {"normal": "15-30", "urgent": "7-10"},
        "required_docs": [
            "Previous ownership documents",
            "Citizenship certificate",
            "Tax clearance certificate", 
            "Survey report"
        ]
    },
    "business_license": {
        "name_en": "Business License",
        "name_np": "व्यापार अनुमतिपत्र", 
        "fees": {"small": 500, "medium": 2000, "large": 10000},
        "processing_days": {"normal": "7-15"},
        "required_docs": [
            "PAN certificate",
            "Citizenship certificate",
            "Office premises proof",
            "Environmental clearance (if required)"
        ]
    },
    "company_registration": {
        "name_en": "Company Registration",
        "name_np": "कम्पनी दर्ता",
        "fees": {"pvt_limited": 5000, "public_limited": 25000},
        "processing_days": {"normal": "15-21"},
        "required_docs": [
            "Memorandum of Association",
            "Articles of Association", 
            "Name reservation certificate",
            "Directors' details"
        ]
    }
}

# Office Type Service Mapping
OFFICE_SERVICE_MAPPING = {
    "district_administration_office": ["citizenship", "passport", "licenses"],
    "passport_department": ["passport"],
    "transport_department": ["driving_license", "vehicle_registration", "route_permit"],
    "transport_office": ["driving_license", "vehicle_registration", "license_renewal"],
    "land_revenue_office": ["land_registration", "property_transfer", "tax_collection"],
    "land_department": ["land_registration", "land_records", "property_valuation"],
    "survey_department": ["land_survey", "mapping", "geodetic_survey"],
    "company_registrar": ["company_registration", "business_license", "trademark_registration"]
}