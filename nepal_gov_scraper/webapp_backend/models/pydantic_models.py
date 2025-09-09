#!/usr/bin/env python3
"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ServiceStatus(str, Enum):
    SUCCESS = "kaam_bhayo"      # काम भयो
    FAILED = "kaam_bhayena"     # काम भएन
    IN_PROGRESS = "chalirahe"   # चलिरहे


class DistrictResponse(BaseModel):
    """Response for district selection"""
    districts: List[str]
    provinces: Dict[str, List[str]]  # Province -> Districts mapping


class OfficeType(BaseModel):
    """Office type selection"""
    office_type: str
    display_name: str
    display_name_nepali: str
    count: int  # Number of offices of this type in selected district


class ServiceOption(BaseModel):
    """Service/task selection"""
    service_id: str
    service_name: str
    service_name_nepali: str
    estimated_time: Optional[str] = None
    fees: Optional[Dict[str, Any]] = None


class OfficeListResponse(BaseModel):
    """List of offices in selected district and type"""
    district: str
    office_type: str
    offices: List[Dict[str, Any]]


class TimerStartRequest(BaseModel):
    """Request to start visit timer"""
    office_id: int
    service_id: int
    user_id: Optional[int] = None


class TimerStartResponse(BaseModel):
    """Response when timer starts"""
    visit_id: int
    start_time: datetime
    office_name: str
    service_name: str


class VisitEndRequest(BaseModel):
    """Request to end visit"""
    visit_id: int
    service_status: ServiceStatus  # kaam_bhayo or kaam_bhayena


class RatingRequest(BaseModel):
    """Rating and feedback request"""
    visit_id: int
    
    # 1-5 Star Ratings
    overall_rating: int = Field(..., ge=1, le=5)
    staff_behavior_rating: int = Field(..., ge=1, le=5)
    office_cleanliness_rating: int = Field(..., ge=1, le=5)
    process_efficiency_rating: int = Field(..., ge=1, le=5)
    information_clarity_rating: int = Field(..., ge=1, le=5)
    
    # Nepali Questions (True/False/None)
    asked_for_bribe: Optional[bool] = None          # घुस माग्यो?
    staff_helpful: Optional[bool] = None            # कर्मचारी सहयोगी थिए?
    process_clear: Optional[bool] = None            # प्रक्रिया स्पष्ट थियो?
    documents_sufficient: Optional[bool] = None      # कागजात पुग्यो?
    would_recommend: Optional[bool] = None          # सिफारिस गर्नुहुन्छ?
    
    # Additional Feedback
    wait_reason: Optional[str] = None               # पर्खनुको कारण
    suggestions: Optional[str] = None               # सुझाव
    complaints: Optional[str] = None                # गुनासो


class FeedbackQuestions(BaseModel):
    """Nepali feedback questions for frontend"""
    questions: List[Dict[str, str]] = [
        {
            "id": "asked_for_bribe",
            "question_nepali": "के तपाईंलाई घुस माग्यो?",
            "question_english": "Did they ask for a bribe?",
            "type": "boolean",
            "critical": True
        },
        {
            "id": "staff_helpful",
            "question_nepali": "कर्मचारी सहयोगी र विनम्र थिए?",
            "question_english": "Were the staff helpful and polite?",
            "type": "boolean",
            "critical": False
        },
        {
            "id": "process_clear",
            "question_nepali": "प्रक्रिया स्पष्ट र बुझ्न सजिलो थियो?",
            "question_english": "Was the process clear and easy to understand?",
            "type": "boolean",
            "critical": False
        },
        {
            "id": "documents_sufficient",
            "question_nepali": "तपाईंसँग भएका कागजात पुगे?",
            "question_english": "Were your documents sufficient?",
            "type": "boolean",
            "critical": False
        },
        {
            "id": "would_recommend",
            "question_nepali": "के तपाईं यो कार्यालयलाई अरूलाई सिफारिस गर्नुहुन्छ?",
            "question_english": "Would you recommend this office to others?",
            "type": "boolean",
            "critical": False
        }
    ]


class WaitReasonOptions(BaseModel):
    """Wait reason options in Nepali"""
    options: List[Dict[str, str]] = [
        {"id": "lunch_break", "nepali": "खाजा समय", "english": "Lunch break"},
        {"id": "system_down", "nepali": "कम्प्युटर बिग्रियो", "english": "Computer/system down"},
        {"id": "staff_absent", "nepali": "कर्मचारी अनुपस्थित", "english": "Staff absent"},
        {"id": "long_queue", "nepali": "लामो लाइन", "english": "Long queue"},
        {"id": "document_issue", "nepali": "कागजात समस्या", "english": "Document issues"},
        {"id": "payment_issue", "nepali": "भुक्तानी समस्या", "english": "Payment issues"},
        {"id": "verification", "nepali": "प्रमाणीकरण", "english": "Verification process"},
        {"id": "other", "nepali": "अन्य", "english": "Other"}
    ]


class UserRegistration(BaseModel):
    """Optional user registration"""
    phone: Optional[str] = None
    name: Optional[str] = None
    district: Optional[str] = None
    age_group: Optional[str] = None
    gender: Optional[str] = None
    education_level: Optional[str] = None


class OfficeAnalyticsResponse(BaseModel):
    """Analytics response for an office"""
    office_id: int
    office_name: str
    office_name_nepali: Optional[str]
    district: str
    province: str
    
    # Visit Statistics
    total_visits: int
    successful_visits: int
    failed_visits: int
    success_rate: float
    
    # Average Ratings (1-5)
    avg_overall_rating: float
    avg_staff_behavior: float
    avg_cleanliness: float
    avg_efficiency: float
    avg_information_clarity: float
    
    # Wait Time Statistics
    avg_wait_time_minutes: float
    min_wait_time_minutes: int
    max_wait_time_minutes: int
    
    # Problem Indicators
    bribe_reports: int
    bribe_rate: float
    
    # Rankings
    district_rank: Optional[int]
    province_rank: Optional[int]
    national_rank: Optional[int]
    
    last_updated: datetime


class ComparisonRequest(BaseModel):
    """Request to compare offices"""
    office_ids: List[int] = Field(..., min_items=2, max_items=5)
    metrics: List[str] = ["overall_rating", "efficiency", "staff_behavior", "cleanliness", "bribe_rate"]


class RadarChartData(BaseModel):
    """Radar chart data for office comparison"""
    office_name: str
    metrics: Dict[str, float]  # metric_name -> value (0-5)


class ComparisonResponse(BaseModel):
    """Response for office comparison"""
    offices: List[RadarChartData]
    metrics_info: Dict[str, str]  # metric descriptions


class AnalyticsDashboard(BaseModel):
    """Main analytics dashboard data"""
    total_offices: int
    total_visits: int
    avg_success_rate: float
    avg_overall_rating: float
    
    # Top Performing Offices
    top_rated_offices: List[Dict[str, Any]]  # Top 5 by rating
    most_efficient_offices: List[Dict[str, Any]]  # Top 5 by wait time
    
    # Problem Areas
    offices_with_bribe_reports: List[Dict[str, Any]]
    lowest_rated_offices: List[Dict[str, Any]]
    
    # Provincial Statistics
    provincial_stats: Dict[str, Dict[str, float]]  # Province -> metrics
    
    # Recent Activity
    recent_visits: List[Dict[str, Any]]  # Last 10 visits
    
    last_updated: datetime


class OfficeSearchRequest(BaseModel):
    """Search and filter offices"""
    district: Optional[str] = None
    province: Optional[str] = None
    office_type: Optional[str] = None
    min_rating: Optional[float] = None
    max_wait_time: Optional[int] = None
    services: Optional[List[str]] = None
    sort_by: Optional[str] = "rating"  # rating, wait_time, success_rate
    order: Optional[str] = "desc"  # asc, desc
    limit: Optional[int] = 20