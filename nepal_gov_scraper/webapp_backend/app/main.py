#!/usr/bin/env python3
"""
Main FastAPI application for Nepal Government Office Experience Tracker
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routes
from api.office_selection import router as office_selection_router
from api.visit_tracking import router as visit_tracking_router
from api.analytics import router as analytics_router

# Import database setup
from database.connection import init_database, load_scraper_data

# Create FastAPI app
app = FastAPI(
    title="Nepal Government Office Experience Tracker",
    description="API for tracking citizen experiences with Nepal government offices",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend integration
# In production, this should be restricted to the actual frontend domain
# For local development, we allow localhost and 127.0.0.1
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(office_selection_router)
app.include_router(visit_tracking_router)
app.include_router(analytics_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Nepal Government Office Experience Tracker API",
        "version": "1.0.0",
        "description": "Track citizen experiences and rate government office services",
        "features": [
            "Office selection by district and type",
            "Timer-based visit tracking", 
            "Nepali feedback questions and ratings",
            "Analytics dashboard with comparisons",
            "Radar charts for office comparison"
        ],
        "docs": "/api/docs",
        "endpoints": {
            "districts": "/api/selection/districts",
            "office_types": "/api/selection/office-types/{district}",
            "start_timer": "/api/visit/start-timer",
            "analytics": "/api/analytics/dashboard"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Nepal Office Tracker API is running",
        "timestamp": "2025-09-08T20:00:00Z"
    }

# System info endpoint
@app.get("/api/info")
async def system_info():
    """System information and statistics"""
    return {
        "system": "Nepal Government Office Experience Tracker",
        "purpose": "Citizen feedback and office performance tracking",
        "languages": ["English", "Nepali"],
        "coverage": "All 77 districts of Nepal",
        "office_types": [
            "District Administration Office (DAO)",
            "Passport Department", 
            "Transport Management Office",
            "Land Revenue Office",
            "Survey Department",
            "Company Registrar Office"
        ],
        "key_features": {
            "timer_tracking": "Real-time visit duration tracking",
            "nepali_feedback": "Cultural-appropriate feedback questions",
            "bribe_reporting": "Anonymous corruption reporting", 
            "comparative_analysis": "Office performance comparison",
            "provincial_stats": "Province-wise performance metrics"
        }
    }

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and load data on startup"""
    print("🚀 Starting Nepal Government Office Experience Tracker API...")
    
    print("🗄️ Initializing database...")
    init_database()
    
    print("📂 Loading scraper data...")
    load_scraper_data()
    
    print("✅ API startup completed successfully!")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error messages"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error occurred",
            "error": str(exc),
            "type": type(exc).__name__
        }
    )

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # Set to False in production
        log_level="info"
    )