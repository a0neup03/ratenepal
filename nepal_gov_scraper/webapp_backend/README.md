# 🇳🇵 Nepal Government Office Experience Tracker - Backend API

Real-time citizen experience tracking system for Nepal government offices with timer functionality and Nepali feedback collection.

## 🌟 Key Features

### **📍 Office Selection Flow**
- **District Selection**: Choose from all 77 Nepal districts
- **Office Type Selection**: DAO, Passport, Transport, Land Revenue, etc.  
- **Service Selection**: Specific services (citizenship, passport, licenses)

### **⏱️ Timer-Based Visit Tracking**
- **🚨 Red Start Timer Button**: Prominent timer start functionality
- **Real-time Duration Tracking**: Live wait time calculation
- **Service Status**: कaam भयो (Success) / काम भएन (Failed) buttons

### **⭐ Comprehensive Rating System**
- **5-Star Ratings**: Overall, staff behavior, cleanliness, efficiency, information clarity
- **Nepali Feedback Questions**: 
  - घुस माग्यो? (Did they ask for bribe?)
  - कर्मचारी सहयोगी थिए? (Were staff helpful?)
  - प्रक्रिया स्पष्ट थियो? (Was process clear?)
  - कागजात पुग्यो? (Were documents sufficient?)
  - सिफारिस गर्नुहुन्छ? (Would you recommend?)

### **📊 Analytics Dashboard**
- **Office Performance Metrics**: Success rates, wait times, ratings
- **Radar Charts**: Multi-dimensional office comparison
- **Provincial Statistics**: Province-wise performance analysis
- **Bribe Reporting**: Anonymous corruption tracking

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
cd webapp_backend
pip install -r requirements.txt
```

### **2. Database Setup**
```bash
# Copy environment file
cp .env.example .env

# For SQLite (development)
# No additional setup needed

# For PostgreSQL (production)
# Update DATABASE_URL in .env
createdb nepal_office_tracker
```

### **3. Run Server**
```bash
# Simple way
python run_server.py

# Or directly with uvicorn
cd app
uvicorn main:app --reload --port 8000
```

### **4. Access API**
- **API Base**: http://localhost:8000
- **Documentation**: http://localhost:8000/api/docs
- **Interactive API**: http://localhost:8000/api/redoc

## 📋 API Endpoints

### **Office Selection**
```bash
# Get all districts
GET /api/selection/districts

# Get office types in district
GET /api/selection/office-types/{district}

# Get specific offices
GET /api/selection/offices/{district}/{office_type}

# Get office services
GET /api/selection/services/{office_id}
```

### **Visit Tracking**
```bash
# 🚨 Start timer (Red button)
POST /api/visit/start-timer
{
  "office_id": 1,
  "service_id": 1,
  "user_id": null
}

# End visit (Success/Failed buttons)
POST /api/visit/end-visit
{
  "visit_id": 123,
  "service_status": "kaam_bhayo"  # or "kaam_bhayena"
}

# Submit rating and feedback
POST /api/visit/rating
{
  "visit_id": 123,
  "overall_rating": 4,
  "staff_behavior_rating": 5,
  "asked_for_bribe": false,
  "staff_helpful": true,
  "suggestions": "सुझाव यहाँ लेख्नुहोस्"
}
```

### **Analytics**
```bash
# Main dashboard
GET /api/analytics/dashboard

# Office-specific analytics
GET /api/analytics/office/{office_id}

# Compare offices (radar chart)
POST /api/analytics/compare
{
  "office_ids": [1, 2, 3],
  "metrics": ["overall_rating", "efficiency", "staff_behavior"]
}

# Rankings
GET /api/analytics/rankings/national?metric=overall_rating
```

## 🗄️ Database Schema

### **Core Tables**
- **offices**: Government office information
- **office_services**: Services available at each office
- **office_visits**: Individual visit records with timing
- **users**: Optional user registration
- **office_analytics**: Aggregated performance metrics

### **Key Visit Fields**
- **Timer Data**: start_time, end_time, wait_duration_minutes
- **Outcome**: service_status (success/failed), service_completed
- **Ratings**: 5 different 1-5 star ratings
- **Nepali Questions**: Boolean responses to cultural questions
- **Feedback**: Suggestions, complaints, wait reasons

## 🎯 Frontend Integration

### **Typical User Flow**
1. **Select District** → API: `/api/selection/districts`
2. **Select Office Type** → API: `/api/selection/office-types/{district}`
3. **Select Specific Office** → API: `/api/selection/offices/{district}/{type}`
4. **Select Service** → API: `/api/selection/services/{office_id}`
5. **🚨 Start Timer** → API: `/api/visit/start-timer`
6. **[Wait for service...]**
7. **End Visit** → API: `/api/visit/end-visit`
8. **Rate Experience** → API: `/api/visit/rating`

### **React.js Example**
```javascript
// Start timer (Red button click)
const startTimer = async () => {
  const response = await fetch('/api/visit/start-timer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      office_id: selectedOffice.id,
      service_id: selectedService.id
    })
  });
  const data = await response.json();
  setVisitId(data.visit_id);
  setTimerStarted(true);
};

// End visit buttons
const endVisit = async (status) => {
  await fetch('/api/visit/end-visit', {
    method: 'POST', 
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      visit_id: visitId,
      service_status: status  // "kaam_bhayo" or "kaam_bhayena"
    })
  });
  showRatingForm();
};
```

## 📊 Analytics Features

### **Dashboard Metrics**
- Total offices and visits
- Average success rate and ratings
- Top/bottom performing offices
- Provincial comparisons
- Recent activity feed

### **Radar Chart Comparison**
- Overall rating (1-5)
- Efficiency (wait time based)
- Staff behavior (1-5)
- Cleanliness (1-5) 
- Integrity (bribe-free score)

### **Rankings System**
- National, provincial, district rankings
- Multiple metrics: rating, efficiency, success rate
- Minimum visit thresholds for fairness

## 🛡️ Data Quality & Privacy

### **Anonymous Usage**
- No required user registration
- Optional demographics collection
- Anonymous feedback submission

### **Data Validation**
- Input validation with Pydantic models
- SQL injection prevention
- Rate limiting on API endpoints

### **Corruption Tracking**
- Anonymous bribe reporting
- Aggregated statistics only
- No individual incident details exposed

## 🚀 Production Deployment

### **Environment Setup**
```bash
# Production environment variables
DATABASE_URL=postgresql://user:pass@host:5432/nepal_office_tracker
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
```

### **Docker Deployment**
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app/webapp_backend
RUN pip install -r requirements.txt
CMD ["python", "run_server.py"]
```

---

## 🎯 Next Steps

1. **Test API Endpoints**: Use `/api/docs` to test all functionality
2. **Build Frontend**: React.js interface consuming these APIs
3. **Load Real Data**: Import 88 offices from scraper output
4. **Gather Feedback**: Deploy and collect real citizen experiences
5. **Generate Insights**: Use analytics to improve government services

**Built for Nepal citizens to create transparency and accountability in government services! 🇳🇵**