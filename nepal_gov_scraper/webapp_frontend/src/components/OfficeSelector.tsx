import React, { useState, useEffect } from 'react';
import { getTestOfficeTypes } from '../services/api';
import { OfficeType, Office, Service } from '../types';

interface OfficeSelectorProps {
  district: string;
  province: string;
  onOfficeServiceSelect: (office: Office, service: Service) => void;
}

const OfficeSelector: React.FC<OfficeSelectorProps> = ({ 
  district, 
  province, 
  onOfficeServiceSelect 
}) => {
  const [officeTypes, setOfficeTypes] = useState<OfficeType[]>([]);
  const [selectedOfficeType, setSelectedOfficeType] = useState<string>('');
  const [selectedOffice, setSelectedOffice] = useState<Office | null>(null);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(true);

  // Mock office and service data since we're using test API
  const mockOffices: Record<string, Office[]> = {
    'district_administration_office': [{
      id: 1,
      office_id: 'dao_kathmandu',
      name: `District Administration Office, ${district}`,
      name_nepali: `जिल्ला प्रशासन कार्यालय, ${district}`,
      address: `${district}, Nepal`,
      phone: '015362828',
    }],
    'passport_department': [{
      id: 2, 
      office_id: 'passport_dept',
      name: 'Department of Passport',
      name_nepali: 'राहदानी विभाग',
      address: 'Tripureshwor, Kathmandu',
      phone: '15970330',
    }],
    'transport_office': [{
      id: 3,
      office_id: 'tmo_kathmandu', 
      name: `Transport Management Office, ${district}`,
      name_nepali: `यातायात व्यवस्थापन कार्यालय, ${district}`,
      address: `${district}, Nepal`,
      phone: '015970525',
    }],
  };

  const mockServices: Record<string, Service[]> = {
    'district_administration_office': [
      {
        service_id: 'citizenship_certificate',
        service_name: 'Citizenship Certificate',
        service_name_nepali: 'नागरिकता प्रमाणपत्र',
        estimated_time: '15-20 days',
      }
    ],
    'passport_department': [
      {
        service_id: 'passport_application',
        service_name: 'E-Passport Application', 
        service_name_nepali: 'राहदानी आवेदन',
        estimated_time: '15-30 days',
      }
    ],
    'transport_office': [
      {
        service_id: 'driving_license',
        service_name: 'Driving License',
        service_name_nepali: 'सवारी चालक अनुमतिपत्र',
        estimated_time: '7-15 days',
      },
      {
        service_id: 'vehicle_registration',
        service_name: 'Vehicle Registration',
        service_name_nepali: 'सवारी दर्ता',
        estimated_time: '3-7 days',
      }
    ],
  };

  useEffect(() => {
    const loadOfficeTypes = async () => {
      try {
        const data = await getTestOfficeTypes();
        setOfficeTypes(data.office_types);
        setLoading(false);
      } catch (error) {
        console.error('Error loading office types:', error);
        setLoading(false);
      }
    };

    loadOfficeTypes();
  }, [district]);

  const handleOfficeTypeChange = (officeType: string) => {
    setSelectedOfficeType(officeType);
    setSelectedOffice(null);
    setSelectedService(null);
  };

  const handleOfficeChange = (office: Office) => {
    setSelectedOffice(office);
    setSelectedService(null);
  };

  const handleServiceChange = (service: Service) => {
    setSelectedService(service);
    if (selectedOffice && service) {
      onOfficeServiceSelect(selectedOffice, service);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-lg">कार्यालयहरू लोड भइरहे... (Loading offices...)</div>
      </div>
    );
  }

  const availableOffices = selectedOfficeType ? mockOffices[selectedOfficeType] || [] : [];
  const availableServices = selectedOfficeType ? mockServices[selectedOfficeType] || [] : [];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        🏢 कार्यालय र सेवा छान्नुहोस् (Select Office & Service)
      </h2>
      
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
        <p className="text-blue-800 font-medium">
          📍 स्थान: {district}, {province}
        </p>
        <p className="text-sm text-blue-600">Location: {district}, {province}</p>
      </div>

      <div className="space-y-4">
        {/* Office Type Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            कार्यालयको प्रकार (Office Type)
          </label>
          <select
            value={selectedOfficeType}
            onChange={(e) => handleOfficeTypeChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">कार्यालयको प्रकार छान्नुहोस्... (Select Office Type...)</option>
            {officeTypes.map((officeType) => (
              <option key={officeType.type} value={officeType.type}>
                {officeType.display_name} - {officeType.display_name_nepali}
              </option>
            ))}
          </select>
        </div>

        {/* Specific Office Selection */}
        {selectedOfficeType && availableOffices.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              कार्यालय (Specific Office)
            </label>
            <div className="space-y-2">
              {availableOffices.map((office) => (
                <div
                  key={office.id}
                  className={`p-3 border rounded-md cursor-pointer transition-colors ${
                    selectedOffice?.id === office.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-blue-300'
                  }`}
                  onClick={() => handleOfficeChange(office)}
                >
                  <h4 className="font-medium text-gray-800">{office.name}</h4>
                  <p className="text-sm text-gray-600">{office.name_nepali}</p>
                  {office.address && (
                    <p className="text-sm text-gray-500">📍 {office.address}</p>
                  )}
                  {office.phone && (
                    <p className="text-sm text-gray-500">📞 {office.phone}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Service Selection */}
        {selectedOffice && availableServices.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              सेवा/काम (Service/Task)
            </label>
            <div className="space-y-2">
              {availableServices.map((service) => (
                <div
                  key={service.service_id}
                  className={`p-3 border rounded-md cursor-pointer transition-colors ${
                    selectedService?.service_id === service.service_id
                      ? 'border-green-500 bg-green-50'
                      : 'border-gray-300 hover:border-green-300'
                  }`}
                  onClick={() => handleServiceChange(service)}
                >
                  <h4 className="font-medium text-gray-800">{service.service_name}</h4>
                  <p className="text-sm text-gray-600">{service.service_name_nepali}</p>
                  {service.estimated_time && (
                    <p className="text-sm text-blue-600">
                      ⏱️ अनुमानित समय: {service.estimated_time}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Confirmation */}
        {selectedOffice && selectedService && (
          <div className="bg-green-50 border border-green-200 rounded-md p-4">
            <h3 className="font-bold text-green-800 mb-2">✅ चयन पूरा भयो (Selection Complete)</h3>
            <p><strong>कार्यालय:</strong> {selectedOffice.name}</p>
            <p><strong>सेवा:</strong> {selectedService.service_name} ({selectedService.service_name_nepali})</p>
            <p className="text-sm text-green-700 mt-2">
              अब तपाईं टाइमर सुरु गर्न सक्नुहुन्छ। (Now you can start the timer.)
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default OfficeSelector;