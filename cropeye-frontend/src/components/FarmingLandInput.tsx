import React, { useState } from "react";
import type { FarmingLand, Location } from "../types";

interface FarmingLandInputProps {
  onFarmingLandSelect: (farmingLand: FarmingLand) => void;
  onLocationAutoSet?: (location: Location) => void;
}

export const FarmingLandInput: React.FC<FarmingLandInputProps> = ({
  onFarmingLandSelect,
  onLocationAutoSet,
}) => {
  const [input, setInput] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Predefined farming land areas for quick selection
  const predefinedLands: FarmingLand[] = [
    {
      name: "Small Family Farm",
      boundaries: [
        { lat: 40.7128, lng: -74.006 },
        { lat: 40.7138, lng: -74.007 },
        { lat: 40.7148, lng: -74.008 },
        { lat: 40.7138, lng: -74.009 },
      ],
      area: 2.5,
    },
    {
      name: "Medium Commercial Farm",
      boundaries: [
        { lat: 34.0522, lng: -118.2437 },
        { lat: 34.0532, lng: -118.2447 },
        { lat: 34.0542, lng: -118.2457 },
        { lat: 34.0552, lng: -118.2467 },
        { lat: 34.0562, lng: -118.2477 },
        { lat: 34.0572, lng: -118.2487 },
      ],
      area: 15.0,
    },
    {
      name: "Large Agricultural Field",
      boundaries: [
        { lat: 41.8781, lng: -87.6298 },
        { lat: 41.8791, lng: -87.6308 },
        { lat: 41.8801, lng: -87.6318 },
        { lat: 41.8811, lng: -87.6328 },
        { lat: 41.8821, lng: -87.6338 },
        { lat: 41.8831, lng: -87.6348 },
        { lat: 41.8841, lng: -87.6358 },
        { lat: 41.8851, lng: -87.6368 },
      ],
      area: 50.0,
    },
  ];

  const parseCoordinates = (input: string): Location[] | null => {
    // Parse multiple coordinates separated by semicolons or newlines
    const coords = input
      .split(/[;\n]+/)
      .map((s) => s.trim())
      .filter(Boolean);
    const locations: Location[] = [];

    for (const coord of coords) {
      const parts = coord.split(/[,\s]+/).map((s) => s.trim());
      if (parts.length === 2) {
        const lat = parseFloat(parts[0]);
        const lng = parseFloat(parts[1]);
        if (
          !isNaN(lat) &&
          !isNaN(lng) &&
          lat >= -90 &&
          lat <= 90 &&
          lng >= -180 &&
          lng <= 180
        ) {
          locations.push({ lat, lng });
        } else {
          return null;
        }
      } else {
        return null;
      }
    }

    return locations.length >= 3 ? locations : null;
  };

  const calculateArea = (boundaries: Location[]): number => {
    // Simple area calculation using shoelace formula (approximate for hectares)
    if (boundaries.length < 3) return 0;

    let area = 0;
    for (let i = 0; i < boundaries.length; i++) {
      const j = (i + 1) % boundaries.length;
      area += boundaries[i].lat * boundaries[j].lng;
      area -= boundaries[j].lat * boundaries[i].lng;
    }
    area = Math.abs(area) / 2;

    // Convert to hectares (rough approximation)
    return Math.round(((area * 111319.5 * 111319.5) / 10000) * 100) / 100;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const boundaries = parseCoordinates(input);
    if (!boundaries) {
      setError(
        "Please enter valid coordinates (e.g., 40.7128, -74.0060; 40.7138, -74.0070; ...)"
      );
      setLoading(false);
      return;
    }

    const area = calculateArea(boundaries);
    const farmingLand: FarmingLand = {
      boundaries,
      area,
      name: name.trim() || `Custom Farm (${area} ha)`,
    };

    // Simulate API call delay
    setTimeout(() => {
      onFarmingLandSelect(farmingLand);
      setLoading(false);
    }, 500);
  };

  const calculateCenter = (boundaries: Location[]): Location => {
    const avgLat =
      boundaries.reduce((sum, b) => sum + b.lat, 0) / boundaries.length;
    const avgLng =
      boundaries.reduce((sum, b) => sum + b.lng, 0) / boundaries.length;
    return { lat: avgLat, lng: avgLng };
  };

  const handlePredefinedSelect = (land: FarmingLand) => {
    setLoading(true);
    setTimeout(() => {
      onFarmingLandSelect(land);
      if (onLocationAutoSet) {
        const center = calculateCenter(land.boundaries);
        onLocationAutoSet(center);
      }
      setLoading(false);
    }, 500);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Select Farming Land
      </h3>

      {/* Predefined Options */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3">
          Quick Select Predefined Areas:
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {predefinedLands.map((land) => (
            <button
              key={land.name}
              onClick={() => handlePredefinedSelect(land)}
              disabled={loading}
              className="p-3 border border-gray-300 rounded-lg hover:bg-green-50 hover:border-green-300 transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              <div className="text-sm font-medium text-gray-900">
                {land.name}
              </div>
              <div className="text-xs text-gray-600">{land.area} hectares</div>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Input */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Farm Name (Optional)
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., My Wheat Field"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
            disabled={loading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Boundary Coordinates
          </label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter coordinates for land boundaries (one per line):
40.7128, -74.0060
40.7138, -74.0070
40.7148, -74.0080
40.7138, -74.0090"
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none resize-none"
            disabled={loading}
          />
        </div>

        {error && <div className="text-red-600 text-sm">{error}</div>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 font-medium transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? "Setting Farming Land..." : "Set Custom Farming Land"}
        </button>
      </form>

      <div className="mt-4 text-sm text-gray-600">
        <p>
          Define your farming land boundaries using GPS coordinates. Enter at
          least 3 points to form a polygon. The area will be automatically
          calculated.
        </p>
      </div>
    </div>
  );
};

export default FarmingLandInput;
