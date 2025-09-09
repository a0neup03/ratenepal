#!/usr/bin/env python3
"""
Database connection and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database Configuration - Default to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./nepal_office_tracker.db"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    # SQLite specific settings
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True  # Set to False in production
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Initialize database with tables"""
    from models.database_models import Base, create_tables
    create_tables(engine)
    print("✅ Database tables created successfully")


def load_scraper_data():
    """Load office data from scraper JSON files"""
    import json
    import glob
    from models.database_models import Office, OfficeService
    from sqlalchemy.orm import Session
    
    db = SessionLocal()
    
    try:
        # Find the latest comprehensive scraper output
        json_files = glob.glob("../data/comprehensive_nepal_offices_*.json")
        if not json_files:
            print("⚠️ No scraper data files found in ../data/")
            return
            
        latest_file = sorted(json_files)[-1]
        print(f"📂 Loading data from: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            scraper_data = json.load(f)
        
        offices_data = scraper_data.get('offices', [])
        
        for office_data in offices_data:
            # Check if office already exists
            existing_office = db.query(Office).filter(
                Office.office_id == office_data['id']
            ).first()
            
            if existing_office:
                continue  # Skip if already exists
            
            # Create new office
            office = Office(
                office_id=office_data['id'],
                name=office_data['name'],
                name_nepali=office_data.get('name_nepali'),
                office_type=office_data['type'],
                district=office_data['location']['district'],
                province=office_data['location']['province'],
                address=office_data['location'].get('address'),
                phone=office_data.get('contact', {}).get('phone_general'),
                website=office_data.get('contact', {}).get('website')
            )
            
            db.add(office)
            db.flush()  # Get the ID
            
            # Add services
            for service_data in office_data.get('services', []):
                service = OfficeService(
                    office_id=office.id,
                    service_id=service_data['service_id'],
                    service_name=service_data['service_name'],
                    service_name_nepali=service_data.get('service_name_nepali'),
                    fees=service_data.get('fees', {}),
                    processing_time=service_data.get('processing_times', {}).get('total_normal'),
                    required_documents=service_data.get('required_documents', [])
                )
                db.add(service)
        
        db.commit()
        
        # Count loaded data
        office_count = db.query(Office).count()
        service_count = db.query(OfficeService).count()
        
        print(f"✅ Loaded {office_count} offices and {service_count} services")
        
    except Exception as e:
        print(f"❌ Error loading scraper data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🗄️ Initializing Nepal Office Tracker Database...")
    init_database()
    load_scraper_data()
    print("✅ Database setup complete!")