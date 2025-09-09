import React, { useState, useEffect } from 'react';
import { testTimer } from '../services/api';
import { Office, Service, ServiceStatus } from '../types';

interface VisitTimerProps {
  office: Office;
  service: Service;
  onTimerEnd: (visitId: number, status: ServiceStatus, waitMinutes: number) => void;
}

const VisitTimer: React.FC<VisitTimerProps> = ({ office, service, onTimerEnd }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [startTime, setStartTime] = useState<Date | null>(null);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [visitId, setVisitId] = useState<number | null>(null);

  // Update elapsed time every second when running
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    
    if (isRunning && startTime) {
      interval = setInterval(() => {
        const now = new Date();
        const elapsed = Math.floor((now.getTime() - startTime.getTime()) / 1000);
        setElapsedTime(elapsed);
      }, 1000);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isRunning, startTime]);

  const handleStartTimer = async () => {
    try {
      // Call test timer API
      const response = await testTimer();
      
      setIsRunning(true);
      setStartTime(new Date());
      setElapsedTime(0);
      setVisitId(response.visit_id || 12345); // Use mock visit_id
      
    } catch (error) {
      console.error('Error starting timer:', error);
      alert('टाइमर सुरु गर्न सकिएन। पुनः प्रयास गर्नुहोस्। (Could not start timer. Please try again.)');
    }
  };

  const handleEndVisit = (status: ServiceStatus) => {
    if (!visitId || !startTime) return;

    setIsRunning(false);
    const waitMinutes = Math.floor(elapsedTime / 60);
    onTimerEnd(visitId, status, waitMinutes);
  };

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimerColor = (): string => {
    if (elapsedTime < 900) return 'text-green-600'; // < 15 minutes - green
    if (elapsedTime < 1800) return 'text-yellow-600'; // < 30 minutes - yellow  
    if (elapsedTime < 3600) return 'text-orange-600'; // < 1 hour - orange
    return 'text-red-600'; // > 1 hour - red
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        ⏱️ भिजिट ट्र्याकर (Visit Tracker)
      </h2>

      {/* Office and Service Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
        <h3 className="font-bold text-blue-800">{office.name}</h3>
        <p className="text-blue-700">{office.name_nepali}</p>
        <div className="mt-2">
          <p className="font-medium text-blue-800">सेवा: {service.service_name}</p>
          <p className="text-sm text-blue-600">({service.service_name_nepali})</p>
        </div>
        {office.address && (
          <p className="text-sm text-blue-600 mt-1">📍 {office.address}</p>
        )}
      </div>

      {/* Timer Display */}
      <div className="text-center mb-8">
        {!isRunning ? (
          <div>
            <p className="text-lg text-gray-600 mb-4">
              कार्यालयमा पुगेपछि टाइमर सुरु गर्नुहोस्
            </p>
            <p className="text-sm text-gray-500 mb-6">
              Start timer when you arrive at the office
            </p>
            
            {/* 🚨 RED START BUTTON */}
            <button
              onClick={handleStartTimer}
              className="bg-red-600 hover:bg-red-700 text-white font-bold text-xl px-8 py-4 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-200 border-4 border-red-800"
            >
              🚨 टाइमर सुरु गर्नुहोस् (START TIMER)
            </button>
          </div>
        ) : (
          <div>
            {/* Running Timer Display */}
            <div className={`text-6xl font-mono font-bold mb-4 ${getTimerColor()}`}>
              {formatTime(elapsedTime)}
            </div>
            
            <div className="text-lg text-gray-600 mb-2">
              पर्खाइ जारी... (Waiting ongoing...)
            </div>
            
            <div className="text-sm text-gray-500 mb-6">
              {startTime && `सुरु भएको: ${startTime.toLocaleTimeString('en-GB')} (Started at: ${startTime.toLocaleTimeString('en-GB')})`}
            </div>

            {/* Progress Indicators */}
            <div className="flex justify-center space-x-4 mb-6">
              <div className={`px-3 py-1 rounded-full text-sm ${
                elapsedTime < 900 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'
              }`}>
                < 15 मिनेट (Quick)
              </div>
              <div className={`px-3 py-1 rounded-full text-sm ${
                elapsedTime >= 900 && elapsedTime < 1800 ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-500'
              }`}>
                15-30 मिनेट (Normal)
              </div>
              <div className={`px-3 py-1 rounded-full text-sm ${
                elapsedTime >= 1800 ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-500'
              }`}>
                > 30 मिनेट (Long wait)
              </div>
            </div>

            {/* END BUTTONS */}
            <div className="flex justify-center space-x-4">
              {/* Success Button - काम भयो */}
              <button
                onClick={() => handleEndVisit(ServiceStatus.SUCCESS)}
                className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-3 rounded-lg shadow-md transform hover:scale-105 transition-all duration-200"
              >
                ✅ काम भयो
                <br />
                <span className="text-sm font-normal">(Service Successful)</span>
              </button>

              {/* Failed Button - काम भएन */}
              <button
                onClick={() => handleEndVisit(ServiceStatus.FAILED)}
                className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-3 rounded-lg shadow-md transform hover:scale-105 transition-all duration-200"
              >
                ❌ काम भएन
                <br />
                <span className="text-sm font-normal">(Service Failed)</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
        <h4 className="font-medium text-gray-800 mb-2">निर्देशन (Instructions):</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>1. कार्यालयमा पुगेपछि 🚨 <strong>लाल बटन</strong> थिच्नुहोस्</li>
          <li>2. आफ्नो काम सकिएपछि उपयुक्त बटन थिच्नुहोस्</li>
          <li>3. रेटिङ र फिडब्याक दिनुहोस्</li>
        </ul>
        <ul className="text-sm text-gray-500 space-y-1 mt-2">
          <li>1. Press the 🚨 <strong>red button</strong> when you arrive at the office</li>
          <li>2. Press appropriate button when your work is done</li>
          <li>3. Provide rating and feedback</li>
        </ul>
      </div>
    </div>
  );
};

export default VisitTimer;