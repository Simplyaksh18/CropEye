// src/hooks/useLocation.ts
import { useContext } from "react";
import LocationContext from "../context/location-context";
import type { LocationContextType } from "../context/location-context";

export const useLocation = (): LocationContextType => {
  const context = useContext(LocationContext) as
    | LocationContextType
    | undefined;
  if (!context) {
    throw new Error("useLocation must be used within LocationProvider");
  }
  return context;
};

export default useLocation;
