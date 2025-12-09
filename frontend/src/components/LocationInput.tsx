// src/components/LocationInput.tsx
import { useContext, useState } from "react";
import { LocationContext } from "../context/LocationContext";

export default function LocationInput() {
  const { location, setLocation } = useContext(LocationContext)!;

  const [query, setQuery] = useState("");
  type LocationOption = { name: string; lat: number; lng: number };

  const [suggestions, setSuggestions] = useState<LocationOption[]>([]);
  const [loadingGPS, setLoadingGPS] = useState(false);

  // 🌍 Static preset locations fallback
  const staticLocations = [
    { name: "Chennai, India", lat: 13.0827, lng: 80.2707 },
    { name: "Coimbatore, India", lat: 11.0168, lng: 76.9558 },
    { name: "Bengaluru, India", lat: 12.9716, lng: 77.5946 },
    { name: "Delhi, India", lat: 28.7041, lng: 77.1025 },
  ];

  const useGPS = () => {
    if (!navigator.geolocation) return;

    setLoadingGPS(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocation({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          name: "📍 My Location",
        });
        setLoadingGPS(false);
      },
      () => setLoadingGPS(false)
    );
  };

  const handleSelect = (loc: LocationOption) => {
    setLocation({
      lat: loc.lat,
      lng: loc.lng,
      name: loc.name,
    });
    setQuery("");
    setSuggestions([]);
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow mb-6">
      <p className="text-sm font-medium text-gray-700 mb-2">
        Set Your Farm Location
      </p>

      {/* Input Box */}
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search or use GPS"
        className="border rounded-lg w-full p-2 text-gray-700"
      />

      {/* Suggestions dropdown */}
      {suggestions && suggestions.length > 0 && (
        <div className="bg-white border rounded-lg mt-1 shadow-md">
          {suggestions.map((loc, idx) => (
            <div
              key={idx}
              className="p-2 hover:bg-gray-200 cursor-pointer"
              onClick={() => handleSelect(loc)}
            >
              {loc.name}
            </div>
          ))}
        </div>
      )}

      {/* Static Quick Picks */}
      <div className="flex flex-wrap gap-2 mt-3">
        {staticLocations.map((loc, idx) => (
          <button
            key={idx}
            onClick={() => handleSelect(loc)}
            className="bg-green-50 text-green-700 px-3 py-1 rounded-lg border"
          >
            {loc.name}
          </button>
        ))}
      </div>

      {/* GPS Button */}
      <button
        onClick={useGPS}
        className="bg-green-600 text-white mt-3 px-4 py-2 rounded-lg w-full"
      >
        {loadingGPS ? "Fetching GPS…" : "📍 Use My GPS Location"}
      </button>

      {/* Display selected */}
      {location.lat && (
        <p className="mt-2 text-gray-600 text-center text-sm">
          Selected: <b>{location.name}</b>
        </p>
      )}
    </div>
  );
}
