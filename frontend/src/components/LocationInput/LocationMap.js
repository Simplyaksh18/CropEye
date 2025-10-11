import React, { useState, useRef } from 'react';
import { MapContainer, TileLayer, useMapEvents, Marker, Popup } from 'react-leaflet';
import { useLocation } from '../../context/LocationContext';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const LocationSelector = ({ onLocationSelect }) => {
  const [selectedPosition, setSelectedPosition] = useState(null);

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setSelectedPosition([lat, lng]);
    }
  });

  const handleConfirm = () => {
    if (selectedPosition) {
      onLocationSelect(selectedPosition[0], selectedPosition[1]);
    }
  };

  return selectedPosition === null ? null : (
    <Marker position={selectedPosition}>
      <Popup>
        <div className="map-popup">
          <p>Selected Location:</p>
          <p><strong>{selectedPosition[0].toFixed(4)}, {selectedPosition[1].toFixed(4)}</strong></p>
          <button onClick={handleConfirm} className="confirm-location-btn">
            Analyze This Location
          </button>
        </div>
      </Popup>
    </Marker>
  );
};

const LocationMap = ({ onLocationSelect }) => {
  const { userLocation } = useLocation();

  // Default center (India)
  const defaultCenter = [20.5937, 78.9629];
  const center = userLocation ? [userLocation.lat, userLocation.lng] : defaultCenter;
  const zoom = userLocation ? 12 : 5;

  return (
    <div className="location-map">
      <div className="map-instructions">
        <p>Click anywhere on the map to select a location for analysis</p>
      </div>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '400px', width: '100%' }}
        className="leaflet-container"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationSelector onLocationSelect={onLocationSelect} />

        {/* Show current location if available */}
        {userLocation && (
          <Marker position={[userLocation.lat, userLocation.lng]}>
            <Popup>
              <div>
                <strong>Current Location</strong>
                <br />
                {userLocation.address}
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>
    </div>
  );
};

export default LocationMap;
