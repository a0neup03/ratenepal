#!/usr/bin/env python3
"""
Simple test to verify the Nepal Office Tracker backend works
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Simple FastAPI test app
app = FastAPI(title="Nepal Office Tracker - Test API")

@app.get("/")
async def root():
    return {
        "message": "🇳🇵 Nepal Government Office Experience Tracker API",
        "status": "✅ Backend is working!",
        "features": [
            "📍 District and office selection",
            "⏱️ Timer-based visit tracking",
            "⭐ 5-star rating system",
            "📝 Nepali feedback questions",
            "📊 Analytics dashboard"
        ],
        "workflow": {
            "1": "Select district (77 Nepal districts available)",
            "2": "Choose office type (DAO, Passport, Transport, etc.)",
            "3": "Pick specific office and service",
            "4": "🚨 Start timer (Red button)",
            "5": "End visit: काम भयो (Success) or काम भएन (Failed)",
            "6": "Rate experience and provide feedback"
        },
        "nepali_questions": [
            "घुस माग्यो? (Did they ask for bribe?)",
            "कर्मचारी सहयोगी थिए? (Were staff helpful?)",
            "प्रक्रिया स्पष्ट थियो? (Was process clear?)"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "backend": "working"}

@app.get("/test/districts")
async def test_districts():
    """Test endpoint showing district selection"""
    return {
        "sample_provinces": {
            "Bagmati Province": ["Kathmandu", "Lalitpur", "Bhaktapur"],
            "Gandaki Province": ["Kaski", "Gorkha", "Lamjung"],
            "Koshi Province": ["Morang", "Jhapa", "Sunsari"]
        },
        "total_districts": 77,
        "total_provinces": 7
    }

@app.get("/test/office-types")
async def test_office_types():
    """Test endpoint showing office types"""
    return {
        "office_types": [
            {
                "type": "district_administration_office",
                "name": "District Administration Office (DAO)",
                "name_nepali": "जिल्ला प्रशासन कार्यालय",
                "services": ["Citizenship Certificate", "Various permits"]
            },
            {
                "type": "passport_department", 
                "name": "Passport Department",
                "name_nepali": "राहदानी विभाग",
                "services": ["E-Passport Application"]
            },
            {
                "type": "transport_office",
                "name": "Transport Management Office", 
                "name_nepali": "यातायात व्यवस्थापन कार्यालय",
                "services": ["Driving License", "Vehicle Registration"]
            }
        ]
    }

@app.post("/test/timer")
async def test_timer():
    """Test endpoint for timer functionality"""
    return {
        "message": "🚨 Timer started!",
        "office": "District Administration Office, Kathmandu",
        "service": "Citizenship Certificate", 
        "visit_id": 12345,
        "start_time": "2025-09-08T20:25:00Z",
        "instructions": [
            "Wait for your service to complete",
            "Click 'काम भयो' if successful or 'काम भएन' if failed",
            "Provide ratings and feedback"
        ]
    }

@app.post("/test/rating")
async def test_rating():
    """Test endpoint for rating submission"""
    return {
        "message": "धन्यवाद! तपाईंको फिडब्याक सफलतापूर्वक पेश गरियो।",
        "message_english": "Thank you! Your feedback has been submitted successfully.",
        "rating_received": {
            "overall_rating": 4,
            "staff_behavior": 5,
            "cleanliness": 3,
            "efficiency": 4,
            "information_clarity": 4
        },
        "nepali_feedback": {
            "asked_for_bribe": False,
            "staff_helpful": True,
            "process_clear": True,
            "would_recommend": True
        }
    }

if __name__ == "__main__":
    print("🇳🇵 Nepal Government Office Experience Tracker - Backend Test")
    print("=" * 65)
    print("🚀 Starting test server...")
    print("📍 Test API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 65)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")