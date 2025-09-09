import React, { useState } from 'react';
import DistrictSelector from './components/DistrictSelector';
import OfficeSelector from './components/OfficeSelector';
import VisitTimer from './components/VisitTimer';
import RatingForm from './components/RatingForm';
import { Office, Service, ServiceStatus } from './types';

// Simple CSS-in-JS styles
const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f3f4f6',
    padding: '20px',
  },
  header: {
    textAlign: 'center' as const,
    marginBottom: '30px',
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: '10px',
  },
  subtitle: {
    fontSize: '18px',
    color: '#6b7280',
    marginBottom: '20px',
  },
  badge: {
    display: 'inline-block',
    backgroundColor: '#dbeafe',
    color: '#1e40af',
    padding: '8px 16px',
    borderRadius: '20px',
    fontSize: '14px',
    fontWeight: '500',
  },
  content: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  progressBar: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: '30px',
    gap: '10px',
  },
  progressStep: (active: boolean, completed: boolean) => ({
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
    fontSize: '16px',
    backgroundColor: completed ? '#10b981' : active ? '#3b82f6' : '#e5e7eb',
    color: completed || active ? 'white' : '#6b7280',
  }),
  progressLine: (completed: boolean) => ({
    width: '50px',
    height: '3px',
    backgroundColor: completed ? '#10b981' : '#e5e7eb',
  }),
  stepLabel: {
    textAlign: 'center' as const,
    marginTop: '8px',
    fontSize: '12px',
    color: '#6b7280',
  },
};

enum AppStep {
  DISTRICT_SELECTION = 1,
  OFFICE_SELECTION = 2,
  TIMER = 3,
  RATING = 4,
  COMPLETE = 5,
}

interface VisitData {
  visitId: number;
  waitMinutes: number;
  serviceStatus: ServiceStatus;
}

const App: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<AppStep>(AppStep.DISTRICT_SELECTION);
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [selectedProvince, setSelectedProvince] = useState<string>('');
  const [selectedOffice, setSelectedOffice] = useState<Office | null>(null);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [visitData, setVisitData] = useState<VisitData | null>(null);

  const handleDistrictSelect = (district: string, province: string) => {
    setSelectedDistrict(district);
    setSelectedProvince(province);
    setCurrentStep(AppStep.OFFICE_SELECTION);
  };

  const handleOfficeServiceSelect = (office: Office, service: Service) => {
    setSelectedOffice(office);
    setSelectedService(service);
    setCurrentStep(AppStep.TIMER);
  };

  const handleTimerEnd = (visitId: number, status: ServiceStatus, waitMinutes: number) => {
    setVisitData({ visitId, waitMinutes, serviceStatus: status });
    setCurrentStep(AppStep.RATING);
  };

  const handleRatingComplete = () => {
    setCurrentStep(AppStep.COMPLETE);
  };

  const handleStartOver = () => {
    setCurrentStep(AppStep.DISTRICT_SELECTION);
    setSelectedDistrict('');
    setSelectedProvince('');
    setSelectedOffice(null);
    setSelectedService(null);
    setVisitData(null);
  };

  const renderProgressBar = () => {
    const steps = [
      { num: 1, label: 'जिल्ला' },
      { num: 2, label: 'कार्यालय' },
      { num: 3, label: 'टाइमर' },
      { num: 4, label: 'रेटिङ' },
      { num: 5, label: 'सम्पूर्ण' },
    ];

    return (
      <div style={styles.progressBar}>
        {steps.map((step, index) => (
          <React.Fragment key={step.num}>
            <div>
              <div style={styles.progressStep(currentStep === step.num, currentStep > step.num)}>
                {currentStep > step.num ? '✓' : step.num}
              </div>
              <div style={styles.stepLabel}>{step.label}</div>
            </div>
            {index < steps.length - 1 && (
              <div style={styles.progressLine(currentStep > step.num)} />
            )}
          </React.Fragment>
        ))}
      </div>
    );
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case AppStep.DISTRICT_SELECTION:
        return <DistrictSelector onDistrictSelect={handleDistrictSelect} />;

      case AppStep.OFFICE_SELECTION:
        return (
          <OfficeSelector
            district={selectedDistrict}
            province={selectedProvince}
            onOfficeServiceSelect={handleOfficeServiceSelect}
          />
        );

      case AppStep.TIMER:
        return selectedOffice && selectedService ? (
          <VisitTimer
            office={selectedOffice}
            service={selectedService}
            onTimerEnd={handleTimerEnd}
          />
        ) : null;

      case AppStep.RATING:
        return visitData && selectedOffice ? (
          <RatingForm
            visitId={visitData.visitId}
            waitMinutes={visitData.waitMinutes}
            serviceStatus={visitData.serviceStatus}
            officeName={selectedOffice.name}
            onSubmitComplete={handleRatingComplete}
          />
        ) : null;

      case AppStep.COMPLETE:
        return (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <div className="mb-6">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-3xl font-bold text-green-600 mb-4">
                धन्यवाद! (Thank You!)
              </h2>
              <p className="text-lg text-gray-700 mb-2">
                तपाईंको फिडब्याक सफलतापूर्वक पेश गरियो।
              </p>
              <p className="text-gray-600 mb-6">
                Your feedback has been submitted successfully.
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
              <h3 className="font-bold text-blue-800 mb-2">🎯 तपाईंको योगदान (Your Contribution)</h3>
              <p className="text-blue-700 text-sm">
                तपाईंको फिडब्याकले सरकारी सेवालाई अझ राम्रो बनाउन मद्दत गर्छ।
                <br />
                Your feedback helps improve government services for everyone.
              </p>
            </div>

            <div className="space-y-4">
              <button
                onClick={handleStartOver}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded-lg shadow-md transform hover:scale-105 transition-all duration-200"
              >
                🔄 फेरि सुरु गर्नुहोस् (Start Again)
              </button>

              <div className="text-sm text-gray-500">
                <p>कुनै प्रश्न छ? सहायताका लागि सम्पर्क गर्नुहोस्।</p>
                <p>Questions? Contact us for help.</p>
              </div>
            </div>
          </div>
        );

      default:
        return <div>Loading...</div>;
    }
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.title}>
          🇳🇵 Nepal Government Office Experience Tracker
        </h1>
        <p style={styles.subtitle}>
          नेपाल सरकारी कार्यालय अनुभव ट्र्याकर
        </p>
        <span style={styles.badge}>
          Real-time citizen feedback system
        </span>
      </div>

      <div style={styles.content}>
        {/* Progress Bar */}
        {renderProgressBar()}

        {/* Current Step Content */}
        {renderCurrentStep()}
      </div>

      {/* Footer */}
      <div className="text-center mt-12 text-sm text-gray-500">
        <p>🔒 Secure & Anonymous • 📊 Data for Government Service Improvement</p>
        <p className="mt-1">Made with ❤️ for Nepal Citizens</p>
      </div>
    </div>
  );
};

export default App;