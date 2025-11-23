import React, { createContext, useState } from "react";
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
  const [location, setLocation] = useState<Location | null>(null);
  const [farmingLand, setFarmingLand] = useState<FarmingLand | null>(null);

  // Preset fallback locations for GPS input
  const presetLocations: Location[] = [
    { lat: 28.6139, lng: 77.209, name: "Delhi Farm Sample" },
    { lat: 19.076, lng: 72.8777, name: "Mumbai Farm Sample" },
    { lat: 12.9716, lng: 77.5946, name: "Bangalore Farm Sample" },
    { lat: 13.0827, lng: 80.2707, name: "Chennai Farm Sample" },
  ];

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
