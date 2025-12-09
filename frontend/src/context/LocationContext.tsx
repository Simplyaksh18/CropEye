import React, { createContext, useContext, useState } from "react";

interface Location {
  lat: number | null;
  lng: number | null;
  name?: string;
}

type SetLocationFn = (
  ...args: [number, number] | [{ lat: number; lng: number; name?: string }]
) => void;

interface LocationContextType {
  location: Location;
  // Accept either (lat,lng) or an object {lat,lng}
  setLocation: SetLocationFn;
  bestCrop: string | null;
  setBestCrop: (crop: string | null) => void;
}

const LocationContext = createContext<LocationContextType | undefined>(
  undefined
);

export const LocationProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [location, setLocationState] = useState<Location>({
    lat: null,
    lng: null,
  });
  const [bestCrop, setBestCrop] = useState<string | null>(null);

  const setLocation = (
    a: number | { lat: number; lng: number; name?: string },
    b?: number
  ) => {
    if (typeof a === "number" && typeof b === "number") {
      setLocationState({ lat: a, lng: b });
    } else if (typeof a === "object" && a !== null) {
      setLocationState({ lat: a.lat, lng: a.lng, name: a.name });
    } else {
      // ignore invalid calls
      return;
    }
    setBestCrop(null); // reset crop when location changes
  };

  return (
    <LocationContext.Provider
      value={{ location, setLocation, bestCrop, setBestCrop }}
    >
      {children}
    </LocationContext.Provider>
  );
};

export const useLocation = () => {
  const context = useContext(LocationContext);
  if (!context)
    throw new Error("useLocation must be used within LocationProvider");
  return context;
};

export { LocationContext };
