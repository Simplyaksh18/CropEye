import React, { useState } from "react";
import type { Location } from "../types";
import { useLocation } from "../hooks/useLocation";

interface LocationInputProps {
  onLocationSelect: (location: Location) => void;
}

export const LocationInput: React.FC<LocationInputProps> = ({
  onLocationSelect,
}) => {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { presetLocations } = useLocation();

  const handlePresetLocation = (preset: Location) => {
    // Update input field with formatted coordinates
    const formattedInput = `${preset.lat}, ${preset.lng}`;
    setInput(formattedInput);

    // Immediately call the parent callback
    onLocationSelect(preset);

    // Clear any previous errors
    setError("");
  };

  const parseCoordinates = (input: string): Location | null => {
    // Try to parse as "lat,lng" or "lat lng"
    const parts = input.split(/[,\s]+/).map((s) => s.trim());

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
        return { lat, lng };
      }
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const location = parseCoordinates(input);

    if (!location) {
      setError("Please enter valid coordinates (e.g., 40.7128, -74.0060)");
      setLoading(false);
      return;
    }

    // Simulate API call delay
    setTimeout(() => {
      onLocationSelect(location);
      setLoading(false);
    }, 500);
  };

  const handleCurrentLocation = () => {
    setLoading(true);
    setError("");

    if (!navigator.geolocation) {
      setError("Geolocation is not supported by this browser");
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        // Fill the input box with current location
        setInput(`${location.lat.toFixed(4)}, ${location.lng.toFixed(4)}`);

        onLocationSelect(location);
        setLoading(false);
      },
      () => {
        setError("Unable to retrieve your location");
        setLoading(false);
      }
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        📍 Set Your Location
      </h2>

      {/* Preset Locations */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Quick Select Sample Locations:
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {presetLocations.map((preset, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handlePresetLocation(preset)}
              disabled={loading}
              className="p-3 border border-gray-300 rounded-lg hover:bg-green-50 hover:border-green-300 transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed text-left"
            >
              <div className="font-medium text-gray-800">{preset.name}</div>
              <div className="text-sm text-gray-500">
                {preset.lat.toFixed(4)}, {preset.lng.toFixed(4)}
              </div>
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="coordinates"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Enter Coordinates (Latitude, Longitude)
          </label>
          <input
            id="coordinates"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., 40.7128, -74.0060"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? "Setting..." : "Set Location"}
          </button>

          <button
            type="button"
            onClick={handleCurrentLocation}
            disabled={loading}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? "Getting..." : "📍 Use Current Location"}
          </button>
        </div>
      </form>

      <p className="mt-4 text-xs text-gray-500">
        Enter coordinates as "latitude, longitude" or use your current location.
        This information is used for accurate agricultural recommendations.
      </p>
    </div>
  );
};

export default LocationInput;
