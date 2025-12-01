import React, { createContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import type { Location, FarmingLand } from "../types";

interface LocationContextType {
  location: Location | null;
  setLocation: (location: Location) => void;
  farmingLand: FarmingLand | null;
  setFarmingLand: (farmingLand: FarmingLand) => void;
  presetLocations: Location[];
}

export const LocationContext = createContext<LocationContextType | undefined>(
  undefined
);

export const LocationProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [location, setLocation] = useState<Location | null>(() => {
    try {
      const raw = localStorage.getItem("cropEye.location");
      return raw ? (JSON.parse(raw) as Location) : null;
    } catch (e) {
      return null;
    }
  });

  const [farmingLand, setFarmingLand] = useState<FarmingLand | null>(() => {
    try {
      const raw = localStorage.getItem("cropEye.farmingLand");
      return raw ? (JSON.parse(raw) as FarmingLand) : null;
    } catch (e) {
      return null;
    }
  });

  // Preset fallback locations for GPS input
  const presetLocations: Location[] = [
    { lat: 28.6139, lng: 77.209, name: "Delhi Farm Sample" },
    { lat: 19.076, lng: 72.8777, name: "Mumbai Farm Sample" },
    { lat: 12.9716, lng: 77.5946, name: "Bangalore Farm Sample" },
    { lat: 13.0827, lng: 80.2707, name: "Chennai Farm Sample" },
  ];

  // persist changes
  useEffect(() => {
    try {
      if (location) {
        localStorage.setItem("cropEye.location", JSON.stringify(location));
      } else {
        localStorage.removeItem("cropEye.location");
      }
    } catch (e) {
      // ignore storage errors
    }
  }, [location]);

  useEffect(() => {
    try {
      if (farmingLand) {
        localStorage.setItem(
          "cropEye.farmingLand",
          JSON.stringify(farmingLand)
        );
      } else {
        localStorage.removeItem("cropEye.farmingLand");
      }
    } catch (e) {
      // ignore
    }
  }, [farmingLand]);

  return (
    <LocationContext.Provider
      value={{
        location,
        setLocation,
        farmingLand,
        setFarmingLand,
        presetLocations,
      }}
    >
      {children}
    </LocationContext.Provider>
  );
};

// Persist location and farmingLand to localStorage when they change
// Doing this after the component definition to avoid hooks misuse; use a small effect inside the provider is preferable,
// but to keep changes minimal we add the effect above inside the provider scope instead.
