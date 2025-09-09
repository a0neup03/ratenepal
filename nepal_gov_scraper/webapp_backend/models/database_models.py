#!/usr/bin/env python3
"""
Database models for Nepal Government Office User Experience Tracking
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

Base = declarative_base()


class ServiceStatus(str, Enum):
    SUCCESS = "kaam_bhayo"      # काम भयो - Service successful
    FAILED = "kaam_bhayena"     # काम भएन - Service failed
    IN_PROGRESS = "chalirahe"   # चलिरहे - Still ongoing


class Office(Base):
    """Government offices table"""
    __tablename__ = "offices"
    
    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(String, unique=True, index=True)  # From scraper data
    name = Column(String, nullable=False)
    name_nepali = Column(String)
    office_type = Column(String, nullable=False)  # dao, passport_office, etc.
    district = Column(String, nullable=False, index=True)
    province = Column(String, nullable=False, index=True)
    address = Column(Text)
    phone = Column(String)
    website = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    visits = relationship("OfficeVisit", back_populates="office")
    services = relationship("OfficeService", back_populates="office")


class OfficeService(Base):
    """Services available at each office"""
    __tablename__ = "office_services"
    
    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"))
    service_id = Column(String, nullable=False)  # citizenship_certificate, passport, etc.
    service_name = Column(String, nullable=False)
    service_name_nepali = Column(String)
    fees = Column(JSON)  # Fee structure
    processing_time = Column(String)  # Expected processing time
    required_documents = Column(JSON)  # List of required documents
    
    # Relationships
    office = relationship("Office", back_populates="services")
    visits = relationship("OfficeVisit", back_populates="service")


class User(Base):
    """Users providing feedback"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)  # Optional registration
    name = Column(String)
    district = Column(String)  # User's home district
    age_group = Column(String)  # 18-25, 26-35, etc.
    gender = Column(String)  # Male, Female, Other
    education_level = Column(String)  # For demographics
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    visits = relationship("OfficeVisit", back_populates="user")


class OfficeVisit(Base):
    """Individual office visits with timing and ratings"""
    __tablename__ = "office_visits"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    office_id = Column(Integer, ForeignKey("offices.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("office_services.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Anonymous allowed
    
    # Visit Timing
    visit_date = Column(DateTime, default=datetime.utcnow)
    start_time = Column(DateTime)  # When timer started
    end_time = Column(DateTime)    # When timer ended
    wait_duration_minutes = Column(Integer)  # Calculated wait time
    
    # Visit Outcome
    service_status = Column(String, default=ServiceStatus.IN_PROGRESS)  # kaam_bhayo, kaam_bhayena
    service_completed = Column(Boolean, default=False)
    
    # Ratings (1-5 stars)
    overall_rating = Column(Integer)  # Overall experience
    staff_behavior_rating = Column(Integer)  # Staff politeness/helpfulness
    office_cleanliness_rating = Column(Integer)  # Office cleanliness
    process_efficiency_rating = Column(Integer)  # Process speed/efficiency
    information_clarity_rating = Column(Integer)  # Information provided clarity
    
    # Nepali Questions (Yes/No/N/A)
    asked_for_bribe = Column(Boolean)  # घुस माग्यो? (Ghus magyo?)
    staff_helpful = Column(Boolean)   # कर्मचारी सहयोगी थिए? (Karmachari sahayogi thie?)
    process_clear = Column(Boolean)   # प्रक्रिया स्पष्ट थियो? (Prakriya spashta thiyo?)
    documents_sufficient = Column(Boolean)  # कागजात पुग्यो? (Kagjat pugyo?)
    would_recommend = Column(Boolean)  # सिफारिस गर्नुहुन्छ? (Sifarish garnuhuncha?)
    
    # Additional Feedback
    wait_reason = Column(String)  # Why did you wait? (lunch, system down, etc.)
    suggestions = Column(Text)    # सुझाव (Sujhav)
    complaints = Column(Text)     # गुनासो (Gunaso)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    office = relationship("Office", back_populates="visits")
    service = relationship("OfficeService", back_populates="visits")
    user = relationship("User", back_populates="visits")


class OfficeAnalytics(Base):
    """Aggregated analytics for offices (updated periodically)"""
    __tablename__ = "office_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"), unique=True)
    
    # Visit Statistics
    total_visits = Column(Integer, default=0)
    successful_visits = Column(Integer, default=0)  # kaam_bhayo
    failed_visits = Column(Integer, default=0)      # kaam_bhayena
    success_rate = Column(Float, default=0.0)       # Percentage
    
    # Average Ratings
    avg_overall_rating = Column(Float, default=0.0)
    avg_staff_behavior = Column(Float, default=0.0)
    avg_cleanliness = Column(Float, default=0.0)
    avg_efficiency = Column(Float, default=0.0)
    avg_information_clarity = Column(Float, default=0.0)
    
    # Wait Time Statistics
    avg_wait_time_minutes = Column(Float, default=0.0)
    min_wait_time_minutes = Column(Integer, default=0)
    max_wait_time_minutes = Column(Integer, default=0)
    
    # Problem Indicators
    bribe_reports = Column(Integer, default=0)  # Number of bribe reports
    bribe_rate = Column(Float, default=0.0)     # Percentage
    
    # Rankings
    district_rank = Column(Integer)  # Rank within district
    province_rank = Column(Integer)  # Rank within province
    national_rank = Column(Integer)  # National rank
    
    # Last Updated
    last_calculated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    office = relationship("Office")


# Database initialization helper
def create_tables(engine):
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)