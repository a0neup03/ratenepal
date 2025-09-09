# 🇳🇵 Nepal Government Office Experience Tracker - Frontend

Interactive React.js web application for tracking citizen experiences with Nepal government offices in real-time.

## 🌟 Key Features Implemented

### **📍 Complete User Flow**
1. **District Selection**: Choose from all 77 Nepal districts by province
2. **Office Selection**: Select office type (DAO, Passport, Transport, etc.)
3. **Service Selection**: Pick specific government service needed
4. **🚨 Timer Tracking**: Prominent red button to start visit timing
5. **Service Completion**: End with "काम भयो" (Success) or "काम भएन" (Failed)
6. **Rating & Feedback**: Comprehensive rating system with Nepali questions

### **⏱️ Timer-Based Visit Tracking**
- **🚨 Red Start Timer Button**: Highly visible, distinctive red button
- **Real-time Duration Display**: Live countdown with color coding
- **Visual Progress Indicators**: Green (<15 min), Yellow (15-30 min), Red (>30 min)
- **End Visit Buttons**: Clear success/failure options in Nepali and English

### **⭐ Comprehensive Rating System**
- **5-Star Ratings**: Overall, staff behavior, cleanliness, efficiency, information clarity
- **Nepali Cultural Questions**:
  - घुस माग्यो? (Did they ask for bribe?) - Critical question highlighted in red
  - कर्मचारी सहयोगी थिए? (Were staff helpful?)
  - प्रक्रिया स्पष्ट थियो? (Was process clear?)
  - कागजात पुग्यो? (Were documents sufficient?)
  - सिफारिस गर्नुहुन्छ? (Would you recommend?)

### **🎨 User Experience Features**
- **Bilingual Interface**: All text in both Nepali and English
- **Progress Bar**: Visual step-by-step progress indicator
- **Responsive Design**: Works on desktop and mobile devices
- **Color-Coded Feedback**: Visual cues for different states
- **Smooth Animations**: Professional transitions between steps

## 🛠️ Technical Implementation

### **Frontend Stack**
- **React.js 18** with TypeScript for type safety
- **Custom CSS** with utility classes (Tailwind-inspired)
- **Axios** for API communication
- **Component-based Architecture** for maintainability

### **Project Structure**
```
webapp_frontend/
├── src/
│   ├── components/
│   │   ├── DistrictSelector.tsx    # Province/district selection
│   │   ├── OfficeSelector.tsx      # Office and service selection  
│   │   ├── VisitTimer.tsx          # Timer functionality with red button
│   │   └── RatingForm.tsx          # Rating stars and Nepali questions
│   ├── services/
│   │   └── api.ts                  # API service functions
│   ├── types/
│   │   └── index.ts                # TypeScript type definitions
│   ├── App.tsx                     # Main app with step flow
│   └── index.tsx                   # App entry point
├── public/
│   └── index.html                  # HTML template with Nepal theme
├── demo.html                       # Standalone interactive demo
└── package.json                    # Dependencies and scripts
```

### **Component Features**

#### **DistrictSelector.tsx**
- Province-based district filtering
- Real-time validation and state management
- Bilingual labels and confirmation messages

#### **OfficeSelector.tsx**
- Office type cards with visual selection
- Service listing with estimated processing times
- Complete office information display (address, phone)

#### **VisitTimer.tsx**
- **🚨 Prominent red start button** with hover effects
- Real-time timer with minute:second format
- Color-coded timer (green → yellow → red progression)
- Dual end buttons for success/failure outcomes

#### **RatingForm.tsx**
- Interactive 5-star rating system
- Boolean question buttons with three states (Yes/No/N/A)
- Critical question highlighting (bribe reporting in red)
- Text areas for suggestions and complaints
- Wait reason dropdown with Nepali options

## 🖥️ Demo & Testing

### **Interactive HTML Demo**
```bash
# Open the standalone demo
open webapp_frontend/demo.html
```

The demo includes:
- **Full workflow simulation**: All 5 steps of the user journey
- **Working timer**: Real-time countdown with color changes
- **Interactive elements**: Star ratings, boolean questions, form validation
- **Responsive design**: Works on all screen sizes
- **Bilingual interface**: Complete Nepal/English language support

### **API Integration**
```typescript
// Example API calls
import { startTimer, endVisit, submitRating } from './services/api';

// Start timer
const visit = await startTimer(officeId, serviceId);

// End visit
await endVisit(visitId, ServiceStatus.SUCCESS);

// Submit rating
await submitRating({
  visit_id: visitId,
  overall_rating: 4,
  asked_for_bribe: false,
  // ... other ratings
});
```

## 🎯 User Experience Highlights

### **Nepali-First Design**
- All primary text in Devanagari script
- Cultural context for questions (corruption, helpfulness)
- Respectful language and tone throughout
- English translations for accessibility

### **Visual Design**
- **Nepal flag emoji** (🇳🇵) prominent throughout
- **Red timer button** that stands out visually
- **Progress indicators** showing completion status
- **Color-coded feedback** for quick understanding

### **Accessibility Features**
- High contrast colors for readability
- Large, touchable buttons for mobile use
- Clear visual hierarchy and spacing
- Loading states and error handling

## 🔄 Integration with Backend

### **API Endpoints Used**
- `GET /test/districts` - District selection data
- `GET /test/office-types` - Available office types  
- `POST /test/timer` - Start visit timer
- `POST /test/rating` - Submit rating and feedback

### **Data Flow**
```
User Action → Frontend State → API Call → Backend Processing → Response → UI Update
```

### **Error Handling**
- Network error messages in Nepali and English
- Graceful fallbacks for failed API calls
- User-friendly error notifications
- Retry mechanisms for critical operations

## 🚀 Future Enhancements

### **Phase 2 Features**
- **Analytics Dashboard**: Charts and comparisons
- **Real-time Updates**: Live office status
- **Push Notifications**: Visit reminders
- **Offline Support**: Service Worker implementation

### **Advanced Features**
- **Photo Upload**: Evidence for feedback
- **Location Services**: GPS verification
- **Social Sharing**: Share experiences
- **Government Integration**: Direct data sync

---

## 🎊 Complete System Status

**✅ Frontend: 100% Complete**
- All user flow components implemented
- Timer functionality with red button working
- Nepali feedback form with star ratings complete
- Responsive design and animations implemented
- API integration layer ready

**✅ Backend: 100% Complete**  
- FastAPI server with all endpoints
- Database models for visits and ratings
- Timer tracking and analytics ready
- Nepali question processing implemented

**✅ Demo Ready**
Open `demo.html` to see the complete working system!

**Built with ❤️ for Nepal citizens to improve government services! 🇳🇵**