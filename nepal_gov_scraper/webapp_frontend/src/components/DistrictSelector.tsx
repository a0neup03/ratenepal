import React, { useState, useEffect } from 'react';
import { getTestDistricts } from '../services/api';

interface DistrictSelectorProps {
  onDistrictSelect: (district: string, province: string) => void;
}

const DistrictSelector: React.FC<DistrictSelectorProps> = ({ onDistrictSelect }) => {
  const [provinces, setProvinces] = useState<Record<string, string[]>>({});
  const [selectedProvince, setSelectedProvince] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDistricts = async () => {
      try {
        const data = await getTestDistricts();
        setProvinces(data.sample_provinces);
        setLoading(false);
      } catch (error) {
        console.error('Error loading districts:', error);
        setLoading(false);
      }
    };

    loadDistricts();
  }, []);

  const handleProvinceChange = (province: string) => {
    setSelectedProvince(province);
    setSelectedDistrict('');
  };

  const handleDistrictChange = (district: string) => {
    setSelectedDistrict(district);
    onDistrictSelect(district, selectedProvince);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-lg">जिल्लाहरू लोड भइरहे... (Loading districts...)</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        🌍 आफ्नो जिल्ला छान्नुहोस् (Select Your District)
      </h2>
      
      <div className="space-y-4">
        {/* Province Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            प्रदेश (Province)
          </label>
          <select
            value={selectedProvince}
            onChange={(e) => handleProvinceChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">प्रदेश छान्नुहोस्... (Select Province...)</option>
            {Object.keys(provinces).map((province) => (
              <option key={province} value={province}>
                {province}
              </option>
            ))}
          </select>
        </div>

        {/* District Selection */}
        {selectedProvince && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              जिल्ला (District)
            </label>
            <select
              value={selectedDistrict}
              onChange={(e) => handleDistrictChange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">जिल्ला छान्नुहोस्... (Select District...)</option>
              {provinces[selectedProvince].map((district) => (
                <option key={district} value={district}>
                  {district}
                </option>
              ))}
            </select>
          </div>
        )}

        {selectedDistrict && (
          <div className="bg-green-50 border border-green-200 rounded-md p-3">
            <p className="text-green-800">
              ✅ छानिएको: <strong>{selectedDistrict}, {selectedProvince}</strong>
            </p>
            <p className="text-sm text-green-600 mt-1">
              Selected: <strong>{selectedDistrict}, {selectedProvince}</strong>
            </p>
          </div>
        )}
      </div>

      <div className="mt-6 text-center">
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
          <p className="text-blue-800 font-medium">
            📊 कुल: {Object.values(provinces).flat().length} जिल्लाहरू उपलब्ध
          </p>
          <p className="text-sm text-blue-600">
            Total: {Object.values(provinces).flat().length} districts available
          </p>
        </div>
      </div>
    </div>
  );
};

export default DistrictSelector;