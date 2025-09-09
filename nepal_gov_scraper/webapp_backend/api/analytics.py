#!/usr/bin/env python3
"""
API endpoints for analytics dashboard and office comparisons
Includes radar charts, rankings, and performance metrics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from typing import List, Dict, Any
from datetime import datetime, timedelta

from database.connection import get_database
from models.database_models import (
    Office, OfficeVisit, OfficeService, OfficeAnalytics, User, ServiceStatus
)
from models.pydantic_models import (
    OfficeAnalyticsResponse, ComparisonRequest, RadarChartData, 
    ComparisonResponse, AnalyticsDashboard
)

from api.dependencies import get_api_key

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics & Dashboard"],
    dependencies=[Depends(get_api_key)]
)


@router.get("/dashboard", response_model=AnalyticsDashboard)
async def get_dashboard_data(db: Session = Depends(get_database)):
    """Main analytics dashboard with key metrics"""
    
    # Overall statistics
    total_offices = db.query(Office).count()
    total_visits = db.query(OfficeVisit).count()
    
    # Success rate calculation
    successful_visits = db.query(OfficeVisit).filter(
        OfficeVisit.service_status == ServiceStatus.SUCCESS
    ).count()
    avg_success_rate = (successful_visits / total_visits * 100) if total_visits > 0 else 0
    
    # Average overall rating
    avg_rating_result = db.query(func.avg(OfficeVisit.overall_rating)).filter(
        OfficeVisit.overall_rating.isnot(None)
    ).scalar()
    avg_overall_rating = round(avg_rating_result, 2) if avg_rating_result else 0
    
    # Top rated offices (with at least 3 reviews)
    top_rated_offices = db.query(
        Office,
        func.avg(OfficeVisit.overall_rating).label('avg_rating'),
        func.count(OfficeVisit.id).label('review_count')
    ).join(OfficeVisit).filter(
        OfficeVisit.overall_rating.isnot(None)
    ).group_by(Office.id).having(
        func.count(OfficeVisit.id) >= 3
    ).order_by(
        desc('avg_rating')
    ).limit(5).all()
    
    # Most efficient offices (lowest wait time)
    most_efficient_offices = db.query(
        Office,
        func.avg(OfficeVisit.wait_duration_minutes).label('avg_wait'),
        func.count(OfficeVisit.id).label('visit_count')
    ).join(OfficeVisit).filter(
        OfficeVisit.wait_duration_minutes.isnot(None)
    ).group_by(Office.id).having(
        func.count(OfficeVisit.id) >= 3
    ).order_by(
        asc('avg_wait')
    ).limit(5).all()
    
    # Offices with bribe reports
    offices_with_bribes = db.query(
        Office,
        func.count(OfficeVisit.id).label('bribe_count'),
        func.count(OfficeVisit.id).label('total_visits')
    ).join(OfficeVisit).filter(
        OfficeVisit.asked_for_bribe == True
    ).group_by(Office.id).order_by(
        desc('bribe_count')
    ).limit(10).all()
    
    # Lowest rated offices
    lowest_rated_offices = db.query(
        Office,
        func.avg(OfficeVisit.overall_rating).label('avg_rating'),
        func.count(OfficeVisit.id).label('review_count')
    ).join(OfficeVisit).filter(
        OfficeVisit.overall_rating.isnot(None)
    ).group_by(Office.id).having(
        func.count(OfficeVisit.id) >= 3
    ).order_by(
        asc('avg_rating')
    ).limit(5).all()
    
    # Provincial statistics
    provincial_stats = {}
    provinces = db.query(Office.province).distinct().all()
    
    for (province,) in provinces:
        province_visits = db.query(OfficeVisit).join(Office).filter(
            Office.province == province
        )
        
        total_province_visits = province_visits.count()
        successful_province_visits = province_visits.filter(
            OfficeVisit.service_status == ServiceStatus.SUCCESS
        ).count()
        
        avg_province_rating = province_visits.filter(
            OfficeVisit.overall_rating.isnot(None)
        ).with_entities(
            func.avg(OfficeVisit.overall_rating)
        ).scalar() or 0
        
        avg_province_wait = province_visits.filter(
            OfficeVisit.wait_duration_minutes.isnot(None)
        ).with_entities(
            func.avg(OfficeVisit.wait_duration_minutes)
        ).scalar() or 0
        
        provincial_stats[province] = {
            "total_visits": total_province_visits,
            "success_rate": (successful_province_visits / total_province_visits * 100) if total_province_visits > 0 else 0,
            "avg_rating": round(avg_province_rating, 2),
            "avg_wait_minutes": round(avg_province_wait, 1)
        }
    
    # Recent visits (last 10)
    recent_visits = db.query(OfficeVisit).join(Office).join(OfficeService).order_by(
        desc(OfficeVisit.visit_date)
    ).limit(10).all()
    
    recent_visits_data = []
    for visit in recent_visits:
        recent_visits_data.append({
            "office_name": visit.office.name,
            "service_name": visit.service.service_name,
            "district": visit.office.district,
            "rating": visit.overall_rating,
            "wait_minutes": visit.wait_duration_minutes,
            "service_status": visit.service_status,
            "visit_date": visit.visit_date
        })
    
    return AnalyticsDashboard(
        total_offices=total_offices,
        total_visits=total_visits,
        avg_success_rate=round(avg_success_rate, 1),
        avg_overall_rating=avg_overall_rating,
        top_rated_offices=[
            {
                "name": office.name,
                "district": office.district,
                "avg_rating": round(avg_rating, 2),
                "review_count": review_count
            }
            for office, avg_rating, review_count in top_rated_offices
        ],
        most_efficient_offices=[
            {
                "name": office.name,
                "district": office.district,
                "avg_wait_minutes": round(avg_wait, 1),
                "visit_count": visit_count
            }
            for office, avg_wait, visit_count in most_efficient_offices
        ],
        offices_with_bribe_reports=[
            {
                "name": office.name,
                "district": office.district,
                "bribe_reports": bribe_count,
                "total_visits": total_visits
            }
            for office, bribe_count, total_visits in offices_with_bribes
        ],
        lowest_rated_offices=[
            {
                "name": office.name,
                "district": office.district,
                "avg_rating": round(avg_rating, 2),
                "review_count": review_count
            }
            for office, avg_rating, review_count in lowest_rated_offices
        ],
        provincial_stats=provincial_stats,
        recent_visits=recent_visits_data,
        last_updated=datetime.utcnow()
    )


@router.get("/office/{office_id}", response_model=OfficeAnalyticsResponse)
async def get_office_analytics(office_id: int, db: Session = Depends(get_database)):
    """Detailed analytics for a specific office"""
    
    office = db.query(Office).filter(Office.id == office_id).first()
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    
    # Visit statistics
    visits = db.query(OfficeVisit).filter(OfficeVisit.office_id == office_id)
    total_visits = visits.count()
    
    if total_visits == 0:
        return OfficeAnalyticsResponse(
            office_id=office.id,
            office_name=office.name,
            office_name_nepali=office.name_nepali,
            district=office.district,
            province=office.province,
            total_visits=0,
            successful_visits=0,
            failed_visits=0,
            success_rate=0.0,
            avg_overall_rating=0.0,
            avg_staff_behavior=0.0,
            avg_cleanliness=0.0,
            avg_efficiency=0.0,
            avg_information_clarity=0.0,
            avg_wait_time_minutes=0.0,
            min_wait_time_minutes=0,
            max_wait_time_minutes=0,
            bribe_reports=0,
            bribe_rate=0.0,
            district_rank=None,
            province_rank=None,
            national_rank=None,
            last_updated=datetime.utcnow()
        )
    
    # Success/failure counts
    successful_visits = visits.filter(OfficeVisit.service_status == ServiceStatus.SUCCESS).count()
    failed_visits = visits.filter(OfficeVisit.service_status == ServiceStatus.FAILED).count()
    success_rate = (successful_visits / total_visits * 100)
    
    # Average ratings
    ratings_query = visits.filter(OfficeVisit.overall_rating.isnot(None))
    avg_overall = ratings_query.with_entities(func.avg(OfficeVisit.overall_rating)).scalar() or 0
    avg_staff = ratings_query.with_entities(func.avg(OfficeVisit.staff_behavior_rating)).scalar() or 0
    avg_clean = ratings_query.with_entities(func.avg(OfficeVisit.office_cleanliness_rating)).scalar() or 0
    avg_efficiency = ratings_query.with_entities(func.avg(OfficeVisit.process_efficiency_rating)).scalar() or 0
    avg_info = ratings_query.with_entities(func.avg(OfficeVisit.information_clarity_rating)).scalar() or 0
    
    # Wait time statistics
    wait_times = visits.filter(OfficeVisit.wait_duration_minutes.isnot(None))
    avg_wait = wait_times.with_entities(func.avg(OfficeVisit.wait_duration_minutes)).scalar() or 0
    min_wait = wait_times.with_entities(func.min(OfficeVisit.wait_duration_minutes)).scalar() or 0
    max_wait = wait_times.with_entities(func.max(OfficeVisit.wait_duration_minutes)).scalar() or 0
    
    # Bribe statistics
    bribe_reports = visits.filter(OfficeVisit.asked_for_bribe == True).count()
    bribe_rate = (bribe_reports / total_visits * 100) if total_visits > 0 else 0
    
    return OfficeAnalyticsResponse(
        office_id=office.id,
        office_name=office.name,
        office_name_nepali=office.name_nepali,
        district=office.district,
        province=office.province,
        total_visits=total_visits,
        successful_visits=successful_visits,
        failed_visits=failed_visits,
        success_rate=round(success_rate, 1),
        avg_overall_rating=round(avg_overall, 2),
        avg_staff_behavior=round(avg_staff, 2),
        avg_cleanliness=round(avg_clean, 2),
        avg_efficiency=round(avg_efficiency, 2),
        avg_information_clarity=round(avg_info, 2),
        avg_wait_time_minutes=round(avg_wait, 1),
        min_wait_time_minutes=int(min_wait),
        max_wait_time_minutes=int(max_wait),
        bribe_reports=bribe_reports,
        bribe_rate=round(bribe_rate, 1),
        district_rank=None,  # TODO: Calculate rankings
        province_rank=None,
        national_rank=None,
        last_updated=datetime.utcnow()
    )


@router.post("/compare", response_model=ComparisonResponse)
async def compare_offices(
    request: ComparisonRequest,
    db: Session = Depends(get_database)
):
    """Compare multiple offices with radar chart data"""
    
    if len(request.office_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 offices required for comparison")
    
    radar_data = []
    
    for office_id in request.office_ids:
        office = db.query(Office).filter(Office.id == office_id).first()
        if not office:
            continue
        
        # Get analytics for this office
        visits = db.query(OfficeVisit).filter(OfficeVisit.office_id == office_id)
        total_visits = visits.count()
        
        if total_visits == 0:
            # Default values for offices with no visits
            metrics = {
                "overall_rating": 0,
                "efficiency": 0,
                "staff_behavior": 0,
                "cleanliness": 0,
                "bribe_rate": 0  # Inverted: 0 = no bribes (good), 5 = many bribes (bad)
            }
        else:
            # Calculate metrics (all normalized to 0-5 scale)
            ratings_query = visits.filter(OfficeVisit.overall_rating.isnot(None))
            overall_rating = ratings_query.with_entities(func.avg(OfficeVisit.overall_rating)).scalar() or 0
            staff_behavior = ratings_query.with_entities(func.avg(OfficeVisit.staff_behavior_rating)).scalar() or 0
            cleanliness = ratings_query.with_entities(func.avg(OfficeVisit.office_cleanliness_rating)).scalar() or 0
            
            # Efficiency: convert wait time to 1-5 scale (lower wait = higher score)
            avg_wait = visits.filter(OfficeVisit.wait_duration_minutes.isnot(None)).with_entities(
                func.avg(OfficeVisit.wait_duration_minutes)
            ).scalar() or 60  # Default 60 minutes
            
            # Convert wait time to efficiency score (5 = very fast, 1 = very slow)
            if avg_wait <= 15:
                efficiency = 5
            elif avg_wait <= 30:
                efficiency = 4
            elif avg_wait <= 60:
                efficiency = 3
            elif avg_wait <= 120:
                efficiency = 2
            else:
                efficiency = 1
            
            # Bribe rate (inverted: lower bribe rate = higher score)
            bribe_count = visits.filter(OfficeVisit.asked_for_bribe == True).count()
            bribe_rate = (bribe_count / total_visits * 100) if total_visits > 0 else 0
            
            # Convert bribe rate to score (5 = no bribes, 1 = many bribes)
            if bribe_rate == 0:
                bribe_score = 5
            elif bribe_rate <= 5:
                bribe_score = 4
            elif bribe_rate <= 15:
                bribe_score = 3
            elif bribe_rate <= 30:
                bribe_score = 2
            else:
                bribe_score = 1
            
            metrics = {
                "overall_rating": round(overall_rating, 1),
                "efficiency": efficiency,
                "staff_behavior": round(staff_behavior, 1),
                "cleanliness": round(cleanliness, 1),
                "integrity": bribe_score  # Renamed from bribe_rate for clarity
            }
        
        radar_data.append(RadarChartData(
            office_name=office.name,
            metrics=metrics
        ))
    
    metrics_info = {
        "overall_rating": "Overall satisfaction rating (1-5 stars)",
        "efficiency": "Service efficiency based on wait time",
        "staff_behavior": "Staff helpfulness and behavior rating", 
        "cleanliness": "Office cleanliness and environment rating",
        "integrity": "Corruption-free service (higher = no bribes reported)"
    }
    
    return ComparisonResponse(
        offices=radar_data,
        metrics_info=metrics_info
    )


@router.get("/rankings/{scope}")
async def get_office_rankings(
    scope: str,  # 'national', 'province', 'district'
    province: str = None,
    district: str = None,
    metric: str = "overall_rating",  # rating, efficiency, success_rate
    limit: int = 20,
    db: Session = Depends(get_database)
):
    """Get office rankings by different metrics"""
    
    query = db.query(Office).join(OfficeVisit)
    
    # Apply scope filters
    if scope == "province" and province:
        query = query.filter(Office.province == province)
    elif scope == "district" and district:
        query = query.filter(Office.district == district)
    
    # Group by office and calculate metrics
    if metric == "overall_rating":
        query = query.filter(OfficeVisit.overall_rating.isnot(None)).group_by(Office.id).having(
            func.count(OfficeVisit.id) >= 3  # At least 3 reviews
        ).with_entities(
            Office,
            func.avg(OfficeVisit.overall_rating).label('metric_value'),
            func.count(OfficeVisit.id).label('review_count')
        ).order_by(desc('metric_value'))
    
    elif metric == "efficiency":
        query = query.filter(OfficeVisit.wait_duration_minutes.isnot(None)).group_by(Office.id).having(
            func.count(OfficeVisit.id) >= 3
        ).with_entities(
            Office,
            func.avg(OfficeVisit.wait_duration_minutes).label('metric_value'),
            func.count(OfficeVisit.id).label('review_count')
        ).order_by(asc('metric_value'))  # Lower wait time = better
    
    elif metric == "success_rate":
        # Calculate success rate
        subquery = db.query(
            OfficeVisit.office_id,
            func.count(OfficeVisit.id).label('total_visits'),
            func.sum(
                func.case(
                    (OfficeVisit.service_status == ServiceStatus.SUCCESS, 1),
                    else_=0
                )
            ).label('successful_visits')
        ).group_by(OfficeVisit.office_id).subquery()
        
        query = db.query(Office, subquery).join(
            subquery, Office.id == subquery.c.office_id
        ).filter(
            subquery.c.total_visits >= 3
        ).with_entities(
            Office,
            (subquery.c.successful_visits / subquery.c.total_visits * 100).label('metric_value'),
            subquery.c.total_visits.label('review_count')
        ).order_by(desc('metric_value'))
    
    results = query.limit(limit).all()
    
    rankings = []
    for rank, (office, metric_value, review_count) in enumerate(results, 1):
        rankings.append({
            "rank": rank,
            "office_name": office.name,
            "district": office.district,
            "province": office.province,
            "metric_value": round(metric_value, 2),
            "review_count": review_count,
            "office_id": office.id
        })
    
    return {
        "scope": scope,
        "metric": metric,
        "rankings": rankings,
        "total_ranked": len(rankings)
    }