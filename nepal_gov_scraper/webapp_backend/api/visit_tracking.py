#!/usr/bin/env python3
"""
API endpoints for visit tracking with timer functionality
Timer Start -> Service End -> Rating Collection
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from database.connection import get_database
from models.database_models import Office, OfficeService, OfficeVisit, User, ServiceStatus
from models.pydantic_models import (
    TimerStartRequest, TimerStartResponse, VisitEndRequest,
    RatingRequest, FeedbackQuestions, WaitReasonOptions, UserRegistration
)

from api.dependencies import get_api_key

router = APIRouter(
    prefix="/api/visit",
    tags=["Visit Tracking"],
    dependencies=[Depends(get_api_key)]
)


@router.post("/start-timer", response_model=TimerStartResponse)
async def start_visit_timer(
    request: TimerStartRequest,
    db: Session = Depends(get_database)
):
    """🚨 START TIMER - Red button functionality"""
    
    # Verify office exists
    office = db.query(Office).filter(Office.id == request.office_id).first()
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    
    # Verify service exists for this office
    service = db.query(OfficeService).filter(
        OfficeService.office_id == request.office_id,
        OfficeService.id == request.service_id
    ).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found for this office")
    
    # Create new visit record
    visit = OfficeVisit(
        office_id=request.office_id,
        service_id=request.service_id,
        user_id=request.user_id,
        start_time=datetime.utcnow(),
        service_status=ServiceStatus.IN_PROGRESS
    )
    
    db.add(visit)
    db.commit()
    db.refresh(visit)
    
    return TimerStartResponse(
        visit_id=visit.id,
        start_time=visit.start_time,
        office_name=office.name,
        service_name=service.service_name
    )


@router.post("/end-visit")
async def end_visit(
    request: VisitEndRequest,
    db: Session = Depends(get_database)
):
    """End visit with SUCCESS (कaam भयो) or FAILED (काम भएन)"""
    
    # Find the visit
    visit = db.query(OfficeVisit).filter(OfficeVisit.id == request.visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    # Update visit status
    visit.end_time = datetime.utcnow()
    visit.service_status = request.service_status
    visit.service_completed = (request.service_status == ServiceStatus.SUCCESS)
    
    # Calculate wait duration
    if visit.start_time:
        duration = visit.end_time - visit.start_time
        visit.wait_duration_minutes = int(duration.total_seconds() / 60)
    
    db.commit()
    
    return {
        "visit_id": visit.id,
        "service_status": visit.service_status,
        "wait_duration_minutes": visit.wait_duration_minutes,
        "message": "Visit ended successfully. Please provide rating and feedback."
    }


@router.post("/rating")
async def submit_rating_and_feedback(
    rating: RatingRequest,
    db: Session = Depends(get_database)
):
    """Submit detailed rating and feedback in Nepali"""
    
    # Find the visit
    visit = db.query(OfficeVisit).filter(OfficeVisit.id == rating.visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    # Update visit with ratings
    visit.overall_rating = rating.overall_rating
    visit.staff_behavior_rating = rating.staff_behavior_rating
    visit.office_cleanliness_rating = rating.office_cleanliness_rating
    visit.process_efficiency_rating = rating.process_efficiency_rating
    visit.information_clarity_rating = rating.information_clarity_rating
    
    # Update Nepali questions
    visit.asked_for_bribe = rating.asked_for_bribe
    visit.staff_helpful = rating.staff_helpful
    visit.process_clear = rating.process_clear
    visit.documents_sufficient = rating.documents_sufficient
    visit.would_recommend = rating.would_recommend
    
    # Update additional feedback
    visit.wait_reason = rating.wait_reason
    visit.suggestions = rating.suggestions
    visit.complaints = rating.complaints
    
    visit.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": "धन्यवाद! तपाईंको फिडब्याक सफलतापूर्वक पेश गरियो।",
        "message_english": "Thank you! Your feedback has been submitted successfully.",
        "visit_id": visit.id,
        "overall_rating": visit.overall_rating
    }


@router.get("/feedback-questions", response_model=FeedbackQuestions)
async def get_feedback_questions():
    """Get Nepali feedback questions for frontend"""
    return FeedbackQuestions()


@router.get("/wait-reasons", response_model=WaitReasonOptions)
async def get_wait_reason_options():
    """Get wait reason options in Nepali"""
    return WaitReasonOptions()


@router.post("/register-user")
async def register_user(
    user_data: UserRegistration,
    db: Session = Depends(get_database)
):
    """Optional user registration for demographic tracking"""
    
    if not user_data.phone:
        raise HTTPException(status_code=400, detail="Phone number is required")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        return {
            "user_id": existing_user.id,
            "message": "User already registered"
        }
    
    # Create new user
    user = User(
        phone=user_data.phone,
        name=user_data.name,
        district=user_data.district,
        age_group=user_data.age_group,
        gender=user_data.gender,
        education_level=user_data.education_level
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "user_id": user.id,
        "message": "User registered successfully"
    }


@router.get("/visit-status/{visit_id}")
async def get_visit_status(visit_id: int, db: Session = Depends(get_database)):
    """Get current status of a visit (for ongoing timer display)"""
    
    visit = db.query(OfficeVisit).filter(OfficeVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    # Calculate current wait time
    current_wait = None
    if visit.start_time:
        if visit.end_time:
            duration = visit.end_time - visit.start_time
        else:
            duration = datetime.utcnow() - visit.start_time
        current_wait = int(duration.total_seconds() / 60)
    
    # Get office and service info
    office = db.query(Office).filter(Office.id == visit.office_id).first()
    service = db.query(OfficeService).filter(OfficeService.id == visit.service_id).first()
    
    return {
        "visit_id": visit.id,
        "office_name": office.name if office else "Unknown",
        "service_name": service.service_name if service else "Unknown",
        "start_time": visit.start_time,
        "end_time": visit.end_time,
        "current_wait_minutes": current_wait,
        "service_status": visit.service_status,
        "has_rating": visit.overall_rating is not None
    }


@router.get("/active-visits")
async def get_active_visits(db: Session = Depends(get_database)):
    """Get all currently active visits (for admin monitoring)"""
    
    active_visits = db.query(OfficeVisit).filter(
        OfficeVisit.service_status == ServiceStatus.IN_PROGRESS,
        OfficeVisit.start_time.isnot(None),
        OfficeVisit.end_time.is_(None)
    ).join(Office).join(OfficeService).all()
    
    result = []
    for visit in active_visits:
        current_duration = datetime.utcnow() - visit.start_time
        current_minutes = int(current_duration.total_seconds() / 60)
        
        result.append({
            "visit_id": visit.id,
            "office_name": visit.office.name,
            "service_name": visit.service.service_name,
            "start_time": visit.start_time,
            "current_wait_minutes": current_minutes,
            "district": visit.office.district
        })
    
    return {
        "active_visits": result,
        "total_active": len(result)
    }