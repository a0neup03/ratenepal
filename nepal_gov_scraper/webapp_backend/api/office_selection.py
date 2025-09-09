#!/usr/bin/env python3
"""
API endpoints for office selection workflow
District -> Office Type -> Specific Office -> Service Selection
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from collections import defaultdict

from database.connection import get_database
from models.database_models import Office, OfficeService
from models.pydantic_models import (
    DistrictResponse, OfficeType, ServiceOption, 
    OfficeListResponse, OfficeSearchRequest
)

from api.dependencies import get_api_key

router = APIRouter(
    prefix="/api/selection",
    tags=["Office Selection"],
    dependencies=[Depends(get_api_key)]
)


@router.get("/districts", response_model=DistrictResponse)
async def get_districts(db: Session = Depends(get_database)):
    """Get all districts and provinces for selection"""
    
    # Query all offices for districts and provinces
    offices = db.query(Office.district, Office.province).distinct().all()
    
    if not offices:
        raise HTTPException(status_code=404, detail="No offices found in database")
    
    # Group districts by province
    provinces = defaultdict(list)
    all_districts = []
    
    for district, province in offices:
        provinces[province].append(district)
        all_districts.append(district)
    
    # Sort everything
    all_districts = sorted(set(all_districts))
    provinces_sorted = {
        province: sorted(districts) 
        for province, districts in provinces.items()
    }
    
    return DistrictResponse(
        districts=all_districts,
        provinces=provinces_sorted
    )


@router.get("/office-types/{district}")
async def get_office_types(district: str, db: Session = Depends(get_database)):
    """Get available office types in selected district"""
    
    # Query office types in the district
    office_types = db.query(
        Office.office_type, 
        db.func.count(Office.id).label('count')
    ).filter(
        Office.district == district
    ).group_by(Office.office_type).all()
    
    if not office_types:
        raise HTTPException(
            status_code=404, 
            detail=f"No offices found in district: {district}"
        )
    
    # Map office types to display names
    type_display_map = {
        "district_administration_office": {
            "display_name": "District Administration Office (DAO)",
            "display_name_nepali": "जिल्ला प्रशासन कार्यालय"
        },
        "passport_department": {
            "display_name": "Passport Department",
            "display_name_nepali": "राहदानी विभाग"
        },
        "transport_office": {
            "display_name": "Transport Management Office",
            "display_name_nepali": "यातायात व्यवस्थापन कार्यालय"
        },
        "land_revenue_office": {
            "display_name": "Land Revenue Office", 
            "display_name_nepali": "मालपोत कार्यालय"
        },
        "survey_department": {
            "display_name": "Survey Department",
            "display_name_nepali": "नापी विभाग"
        },
        "company_registrar": {
            "display_name": "Company Registrar Office",
            "display_name_nepali": "कम्पनी रजिस्ट्रार कार्यालय"
        }
    }
    
    result = []
    for office_type, count in office_types:
        display_info = type_display_map.get(office_type, {
            "display_name": office_type.replace("_", " ").title(),
            "display_name_nepali": office_type
        })
        
        result.append(OfficeType(
            office_type=office_type,
            display_name=display_info["display_name"],
            display_name_nepali=display_info["display_name_nepali"],
            count=count
        ))
    
    return result


@router.get("/offices/{district}/{office_type}")
async def get_offices_in_district(
    district: str, 
    office_type: str, 
    db: Session = Depends(get_database)
):
    """Get specific offices in district of given type"""
    
    offices = db.query(Office).filter(
        Office.district == district,
        Office.office_type == office_type
    ).all()
    
    if not offices:
        raise HTTPException(
            status_code=404, 
            detail=f"No {office_type} found in {district}"
        )
    
    office_list = []
    for office in offices:
        office_list.append({
            "id": office.id,
            "office_id": office.office_id,
            "name": office.name,
            "name_nepali": office.name_nepali,
            "address": office.address,
            "phone": office.phone,
            "website": office.website
        })
    
    return OfficeListResponse(
        district=district,
        office_type=office_type,
        offices=office_list
    )


@router.get("/services/{office_id}")
async def get_office_services(office_id: int, db: Session = Depends(get_database)):
    """Get services available at specific office"""
    
    # Verify office exists
    office = db.query(Office).filter(Office.id == office_id).first()
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    
    # Get services
    services = db.query(OfficeService).filter(
        OfficeService.office_id == office_id
    ).all()
    
    if not services:
        raise HTTPException(
            status_code=404, 
            detail="No services found for this office"
        )
    
    service_list = []
    for service in services:
        # Extract estimated time from fees or processing_time
        estimated_time = service.processing_time
        if not estimated_time and service.fees:
            # Try to get from fees data
            fees_data = service.fees if isinstance(service.fees, dict) else {}
            normal_processing = fees_data.get('normal_processing', {})
            if isinstance(normal_processing, dict):
                estimated_time = normal_processing.get('processing_days')
        
        service_list.append(ServiceOption(
            service_id=service.service_id,
            service_name=service.service_name,
            service_name_nepali=service.service_name_nepali,
            estimated_time=estimated_time,
            fees=service.fees
        ))
    
    return {
        "office_name": office.name,
        "office_name_nepali": office.name_nepali,
        "services": service_list
    }


@router.post("/search")
async def search_offices(
    search_request: OfficeSearchRequest,
    db: Session = Depends(get_database)
):
    """Advanced office search and filtering"""
    
    query = db.query(Office)
    
    # Apply filters
    if search_request.district:
        query = query.filter(Office.district == search_request.district)
    
    if search_request.province:
        query = query.filter(Office.province == search_request.province)
    
    if search_request.office_type:
        query = query.filter(Office.office_type == search_request.office_type)
    
    # For now, return basic results (can add analytics filtering later)
    offices = query.limit(search_request.limit or 20).all()
    
    return {
        "total_found": len(offices),
        "offices": [
            {
                "id": office.id,
                "name": office.name,
                "name_nepali": office.name_nepali,
                "district": office.district,
                "province": office.province,
                "office_type": office.office_type,
                "address": office.address,
                "phone": office.phone
            }
            for office in offices
        ]
    }