# 🌐 Nepal Government Office Feedback Webapp Architecture

## 📋 Project Overview

**Goal**: Create a user-friendly web application that allows citizens to provide feedback, corrections, and updates to Nepal government office data collected by the scraper.

**Target Users**: 
- Nepal citizens who interact with government offices
- Government office staff who want to update their information
- Researchers and journalists working with government data

## 🏗️ System Architecture

### **1. Frontend (User Interface)**
- **Framework**: React.js + TypeScript
- **Styling**: Tailwind CSS for responsive design
- **Maps**: Leaflet.js for Nepal district visualization
- **Data Visualization**: Chart.js for office statistics

### **2. Backend (API & Data Processing)**
- **Framework**: FastAPI (Python) for high-performance API
- **Database**: PostgreSQL for structured data + Redis for caching
- **Authentication**: JWT-based auth for user accounts
- **Data Validation**: Pydantic models matching scraper schema

### **3. Data Pipeline Integration**
- **Input**: JSON files from comprehensive scraper
- **Processing**: Automated data import and validation
- **Output**: Updated JSON files + database sync

## 🎯 Core Features

### **Phase 1: Data Viewing & Feedback**
1. **Office Directory**
   - Browse all 88+ government offices by province/district
   - Search by office name, services, or location  
   - Filter by office type (DAO, passport, transport, etc.)

2. **Office Detail Pages**
   - Complete office information display
   - Contact details with click-to-call/email
   - Service listings with fees and requirements
   - Operating hours and staff information
   - Interactive map showing office location

3. **Feedback System**
   - Report incorrect information (phone, address, hours)
   - Suggest missing services or updated fees
   - Upload photos of office signage or documents
   - Rate data accuracy and user experience

### **Phase 2: User Contributions**
1. **User Accounts**
   - Registration with phone verification
   - Profile management with contribution history
   - Reputation system based on verified contributions

2. **Crowdsourced Updates**
   - Submit new office information
   - Report office closures or relocations
   - Add missing staff details and contact info
   - Contribute service fee updates

3. **Verification System**
   - Admin review queue for user submissions
   - Automated verification using government APIs
   - Community voting on disputed information

### **Phase 3: Advanced Features**
1. **Analytics Dashboard**
   - Data completeness metrics by province
   - User engagement and contribution statistics
   - Office accessibility and citizen satisfaction scores

2. **API Endpoints**
   - Public API for developers and researchers  
   - Real-time data exports in JSON/CSV formats
   - Integration with government systems

## 🗂️ Database Schema

### **Core Tables**
```sql
-- Government Offices
offices (
    id SERIAL PRIMARY KEY,
    office_id VARCHAR UNIQUE,
    name VARCHAR NOT NULL,
    name_nepali VARCHAR,
    type VARCHAR NOT NULL,
    district VARCHAR NOT NULL,
    province VARCHAR NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Contact Information
contacts (
    id SERIAL PRIMARY KEY,
    office_id INTEGER REFERENCES offices(id),
    phone_general VARCHAR,
    phone_citizenship VARCHAR,
    email VARCHAR,
    website VARCHAR,
    address TEXT
);

-- Services
services (
    id SERIAL PRIMARY KEY,
    office_id INTEGER REFERENCES offices(id),
    service_id VARCHAR NOT NULL,
    service_name VARCHAR NOT NULL,
    service_name_nepali VARCHAR,
    fees JSONB,
    required_documents JSONB,
    processing_times JSONB
);

-- User Feedback
feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    office_id INTEGER REFERENCES offices(id),
    feedback_type VARCHAR, -- 'correction', 'addition', 'report'
    field_name VARCHAR,    -- which field is being updated
    old_value TEXT,        -- current value
    new_value TEXT,        -- suggested value
    evidence_url VARCHAR,  -- photo/document upload
    status VARCHAR DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    created_at TIMESTAMP
);

-- Users
users (
    id SERIAL PRIMARY KEY,
    phone VARCHAR UNIQUE,
    name VARCHAR,
    district VARCHAR,
    verified BOOLEAN DEFAULT FALSE,
    reputation_score INTEGER DEFAULT 0,
    created_at TIMESTAMP
);
```

## 🔧 Technical Implementation

### **1. Data Import Pipeline**
```python
# data_importer.py
class OfficeDataImporter:
    def import_scraper_data(self, json_file_path: str):
        """Import comprehensive scraper JSON into database"""
        # Parse JSON file
        # Validate against Pydantic models
        # Upsert offices, contacts, services
        # Update completeness scores
        pass
        
    def export_updated_data(self) -> str:
        """Export database back to scraper JSON format"""
        # Query all offices with latest data
        # Include user contributions
        # Generate updated JSON file
        pass
```

### **2. Feedback Processing**
```python
# feedback_processor.py
class FeedbackProcessor:
    def process_feedback(self, feedback_id: int):
        """Review and apply approved feedback"""
        # Load feedback record
        # Validate new data
        # Update office record
        # Notify user of status
        pass
        
    def auto_verify(self, feedback: FeedbackModel) -> bool:
        """Attempt automatic verification"""
        # Check against government APIs
        # Verify phone numbers
        # Cross-reference with other submissions
        pass
```

### **3. API Endpoints**
```python
# api/routes.py
@app.get("/api/offices")
async def get_offices(province: str = None, district: str = None):
    """Get filtered list of offices"""
    pass

@app.get("/api/offices/{office_id}")
async def get_office_details(office_id: str):
    """Get complete office information"""
    pass

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackModel, user: User):
    """Submit user feedback/corrections"""
    pass

@app.get("/api/stats")
async def get_statistics():
    """Get system-wide statistics"""
    pass
```

## 📱 User Interface Design

### **Homepage**
- Search bar for quick office lookup
- Province map of Nepal with office counts
- Recently updated offices
- User contribution statistics

### **Office List Page**
- Filters: Province, District, Office Type, Services
- Sort: Name, Distance, Update Date, Completeness Score
- Grid/List view toggle
- Pagination with 20 offices per page

### **Office Detail Page**
- Header: Office name, type, completeness score
- Tabs: Contact Info, Services, Staff, Feedback
- Action buttons: Report Issue, Suggest Update, Share
- Embedded map with directions

### **Feedback Form**
- Field-specific feedback forms
- File upload for evidence
- Preview before submission
- Progress tracking after submission

## 🚀 Development Plan

### **Week 1-2: Backend Foundation**
- Set up FastAPI project structure
- Design and create database schema
- Implement data import pipeline
- Basic CRUD operations for offices

### **Week 3-4: Frontend Setup**
- Create React.js application
- Design component structure
- Implement office browsing and search
- Connect to backend API

### **Week 5-6: Feedback System**
- Build feedback submission forms
- Implement admin review interface
- Add user authentication
- Create feedback processing pipeline

### **Week 7-8: Polish & Deploy**
- Add data visualization and maps
- Implement caching and performance optimization
- User testing and bug fixes
- Deploy to production server

## 📊 Success Metrics

### **Data Quality**
- **Target**: 95%+ data accuracy after 6 months
- **Measure**: User feedback resolution rate
- **Goal**: <24 hour response time for critical corrections

### **User Engagement**
- **Target**: 1000+ registered users in first 3 months
- **Measure**: Monthly active feedback contributors
- **Goal**: 50+ verified corrections per month

### **System Performance**
- **Target**: <2 second page load times
- **Measure**: API response times and user satisfaction
- **Goal**: 99.9% uptime

## 💾 Data Storage & Backup

### **Primary Database**: PostgreSQL
- Real-time transactional data
- User accounts and feedback
- Processed office information

### **File Storage**: AWS S3 / Local Storage
- Original scraper JSON files
- User-uploaded evidence photos
- Data export archives

### **Caching**: Redis
- Frequently accessed office data
- Search result caching
- Session management

### **Backup Strategy**
- Daily automated database backups
- Weekly full system snapshots
- Continuous replication to secondary server

## 🔐 Security & Privacy

### **Data Protection**
- HTTPS encryption for all communications
- JWT tokens with expiration
- Input validation and SQL injection prevention
- Rate limiting on API endpoints

### **User Privacy**
- Minimal data collection (phone + name only)
- Anonymized analytics and reporting
- User consent for data usage
- Right to delete account and contributions

### **Content Moderation**
- Automated spam detection
- Manual review for sensitive corrections
- Reputation system to prevent abuse
- Appeal process for rejected submissions

## 🌍 Deployment Architecture

### **Production Environment**
- **Server**: Digital Ocean Droplet (4GB RAM, 2 vCPU)
- **Database**: Managed PostgreSQL instance
- **CDN**: Cloudflare for static assets
- **Monitoring**: Grafana + Prometheus

### **Development Workflow**
- **Version Control**: Git with feature branches
- **CI/CD**: GitHub Actions for automated testing
- **Testing**: pytest for backend, Jest for frontend
- **Code Quality**: ESLint, Prettier, Black formatter

---

## 🎯 Next Steps

1. **Immediate**: Set up development environment and database schema
2. **Week 1**: Implement data import from scraper JSON files
3. **Week 2**: Create basic API endpoints and React frontend
4. **Week 3**: Build feedback submission and admin review system
5. **Month 2**: Launch beta version with initial user testing
6. **Month 3**: Production deployment with full feature set

This webapp will transform the static government office data into a living, community-maintained resource that serves Nepal citizens more effectively! 🇳🇵