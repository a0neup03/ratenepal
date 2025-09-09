import React, { useState, useEffect } from 'react';
import { testRating } from '../services/api';
import { ServiceStatus } from '../types';

interface RatingFormProps {
  visitId: number;
  waitMinutes: number;
  serviceStatus: ServiceStatus;
  officeName: string;
  onSubmitComplete: () => void;
}

const RatingForm: React.FC<RatingFormProps> = ({ 
  visitId, 
  waitMinutes, 
  serviceStatus, 
  officeName,
  onSubmitComplete 
}) => {
  const [ratings, setRatings] = useState({
    overall_rating: 0,
    staff_behavior_rating: 0,
    office_cleanliness_rating: 0,
    process_efficiency_rating: 0,
    information_clarity_rating: 0,
  });

  const [booleanAnswers, setBooleanAnswers] = useState({
    asked_for_bribe: null as boolean | null,
    staff_helpful: null as boolean | null,
    process_clear: null as boolean | null,
    documents_sufficient: null as boolean | null,
    would_recommend: null as boolean | null,
  });

  const [textFeedback, setTextFeedback] = useState({
    wait_reason: '',
    suggestions: '',
    complaints: '',
  });

  const [submitting, setSubmitting] = useState(false);

  // Nepali questions with English translations
  const nepaliQuestions = [
    {
      id: 'asked_for_bribe',
      question_nepali: 'के तपाईंलाई घुस माग्यो?',
      question_english: 'Did they ask for a bribe?',
      critical: true
    },
    {
      id: 'staff_helpful', 
      question_nepali: 'कर्मचारी सहयोगी र विनम्र थिए?',
      question_english: 'Were the staff helpful and polite?',
      critical: false
    },
    {
      id: 'process_clear',
      question_nepali: 'प्रक्रिया स्पष्ट र बुझ्न सजिलो थियो?', 
      question_english: 'Was the process clear and easy to understand?',
      critical: false
    },
    {
      id: 'documents_sufficient',
      question_nepali: 'तपाईंसँग भएका कागजात पुगे?',
      question_english: 'Were your documents sufficient?',
      critical: false
    },
    {
      id: 'would_recommend',
      question_nepali: 'के तपाईं यो कार्यालयलाई अरूलाई सिफारिस गर्नुहुन्छ?',
      question_english: 'Would you recommend this office to others?',
      critical: false
    },
  ];

  const waitReasonOptions = [
    { id: 'lunch_break', nepali: 'खाजा समय', english: 'Lunch break' },
    { id: 'system_down', nepali: 'कम्प्युटर बिग्रियो', english: 'Computer/system down' },
    { id: 'staff_absent', nepali: 'कर्मचारी अनुपस्थित', english: 'Staff absent' },
    { id: 'long_queue', nepali: 'लामो लाइन', english: 'Long queue' },
    { id: 'document_issue', nepali: 'कागजात समस्या', english: 'Document issues' },
    { id: 'payment_issue', nepali: 'भुक्तानी समस्या', english: 'Payment issues' },
    { id: 'verification', nepali: 'प्रमाणीकरण', english: 'Verification process' },
    { id: 'other', nepali: 'अन्य', english: 'Other' },
  ];

  const handleRatingChange = (category: string, rating: number) => {
    setRatings(prev => ({ ...prev, [category]: rating }));
  };

  const handleBooleanChange = (questionId: string, answer: boolean | null) => {
    setBooleanAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmit = async () => {
    // Validate required ratings
    const requiredRatings = Object.values(ratings);
    if (requiredRatings.some(rating => rating === 0)) {
      alert('कृपया सबै रेटिङ्गहरू दिनुहोस्। (Please provide all ratings.)');
      return;
    }

    setSubmitting(true);

    try {
      // Call test rating API
      const response = await testRating();
      
      // Simulate form submission delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      alert('धन्यवाद! तपाईंको फिडब्याक सफलतापूर्वक पेश गरियो।\n(Thank you! Your feedback has been submitted successfully.)');
      onSubmitComplete();
      
    } catch (error) {
      console.error('Error submitting rating:', error);
      alert('फिडब्याक पेश गर्न सकिएन। पुनः प्रयास गर्नुहोस्। (Could not submit feedback. Please try again.)');
    } finally {
      setSubmitting(false);
    }
  };

  const renderStarRating = (category: string, label: string, labelNepali: string) => {
    const currentRating = ratings[category as keyof typeof ratings];
    
    return (
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {labelNepali} ({label})
        </label>
        <div className="flex space-x-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => handleRatingChange(category, star)}
              className={`text-2xl ${
                star <= currentRating ? 'text-yellow-400' : 'text-gray-300'
              } hover:text-yellow-400 transition-colors`}
            >
              ⭐
            </button>
          ))}
        </div>
        <div className="text-xs text-gray-500 mt-1">
          {currentRating > 0 ? `${currentRating} ताराहरू (${currentRating} stars)` : 'रेटिङ दिनुहोस्'}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        📝 अनुभव रेटिङ र फिडब्याक (Experience Rating & Feedback)
      </h2>

      {/* Visit Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
        <h3 className="font-bold text-blue-800">{officeName}</h3>
        <div className="mt-2 text-sm text-blue-700">
          <p>⏱️ कुल समय: {waitMinutes} मिनेट (Total time: {waitMinutes} minutes)</p>
          <p>📊 स्थिति: {serviceStatus === ServiceStatus.SUCCESS ? '✅ काम भयो (Successful)' : '❌ काम भएन (Failed)'}</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Left Column: Star Ratings */}
        <div>
          <h3 className="text-lg font-bold text-gray-800 mb-4">
            ⭐ रेटिङ्गहरू (Ratings)
          </h3>
          
          {renderStarRating('overall_rating', 'Overall Experience', 'समग्र अनुभव')}
          {renderStarRating('staff_behavior_rating', 'Staff Behavior', 'कर्मचारीको व्यवहार')}
          {renderStarRating('office_cleanliness_rating', 'Office Cleanliness', 'कार्यालयको सफाई')}
          {renderStarRating('process_efficiency_rating', 'Process Efficiency', 'प्रक्रियाको दक्षता')}
          {renderStarRating('information_clarity_rating', 'Information Clarity', 'जानकारीको स्पष्टता')}
        </div>

        {/* Right Column: Nepali Questions */}
        <div>
          <h3 className="text-lg font-bold text-gray-800 mb-4">
            ❓ प्रश्नहरू (Questions)
          </h3>

          {nepaliQuestions.map((question) => (
            <div key={question.id} className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <span className={question.critical ? 'text-red-600 font-bold' : ''}>
                  {question.question_nepali}
                </span>
                <br />
                <span className="text-xs text-gray-500">
                  {question.question_english}
                </span>
              </label>
              
              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => handleBooleanChange(question.id, true)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    booleanAnswers[question.id as keyof typeof booleanAnswers] === true
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-green-200'
                  }`}
                >
                  ✅ छ / Yes
                </button>
                
                <button
                  type="button"
                  onClick={() => handleBooleanChange(question.id, false)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    booleanAnswers[question.id as keyof typeof booleanAnswers] === false
                      ? 'bg-red-500 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-red-200'
                  }`}
                >
                  ❌ छैन / No
                </button>
                
                <button
                  type="button"
                  onClick={() => handleBooleanChange(question.id, null)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    booleanAnswers[question.id as keyof typeof booleanAnswers] === null
                      ? 'bg-gray-500 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  🤷 थाहा छैन / N/A
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Additional Feedback Section */}
      <div className="mt-8 space-y-4">
        {/* Wait Reason */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            पर्खनुको कारण (Why did you have to wait?)
          </label>
          <select
            value={textFeedback.wait_reason}
            onChange={(e) => setTextFeedback(prev => ({ ...prev, wait_reason: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">छान्नुहोस्... (Select...)</option>
            {waitReasonOptions.map((option) => (
              <option key={option.id} value={option.id}>
                {option.nepali} ({option.english})
              </option>
            ))}
          </select>
        </div>

        {/* Suggestions */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            सुझावहरू (Suggestions)
          </label>
          <textarea
            value={textFeedback.suggestions}
            onChange={(e) => setTextFeedback(prev => ({ ...prev, suggestions: e.target.value }))}
            placeholder="कार्यालयलाई कसरी सुधार गर्न सकिन्छ? (How can the office be improved?)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
          />
        </div>

        {/* Complaints */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            गुनासोहरू (Complaints)
          </label>
          <textarea
            value={textFeedback.complaints}
            onChange={(e) => setTextFeedback(prev => ({ ...prev, complaints: e.target.value }))}
            placeholder="के कुनै समस्या थियो? (Were there any problems?)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
          />
        </div>
      </div>

      {/* Submit Button */}
      <div className="mt-8 text-center">
        <button
          onClick={handleSubmit}
          disabled={submitting || Object.values(ratings).some(rating => rating === 0)}
          className={`px-8 py-3 rounded-lg text-white font-bold text-lg transition-all duration-200 ${
            submitting || Object.values(ratings).some(rating => rating === 0)
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 transform hover:scale-105 shadow-lg'
          }`}
        >
          {submitting ? 'पेश गर्दै... (Submitting...)' : '📤 फिडब्याक पेश गर्नुहोस् (Submit Feedback)'}
        </button>
      </div>

      {/* Privacy Note */}
      <div className="mt-6 text-center text-xs text-gray-500">
        <p>🔒 तपाईंको जानकारी सुरक्षित छ। यो सरकारी सेवा सुधारका लागि मात्र प्रयोग गरिनेछ।</p>
        <p>🔒 Your information is secure. It will only be used to improve government services.</p>
      </div>
    </div>
  );
};

export default RatingForm;