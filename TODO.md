# Thorough Testing Plan for CropEye Project

## Frontend Thorough Testing

- [x] Visit DashboardPage, verify presence of all modules and location input.
- [x] For each module page (Crops, NDVI, Weather, Soil, Water, Pests):
  - [x] Set location input on DashboardPage.
  - [x] Navigate to the module page.
  - [x] Verify API data is fetched and displayed correctly (Crops API tested successfully).
  - [ ] Test loading and error states by simulating delays/errors.
  - [ ] Test interactive elements like buttons, forms, and navigation.
  - [x] Test NDVI page API calls.
  - [ ] Test Weather page API calls.
  - [ ] Test Soil page API calls.
  - [ ] Test Water page API calls.
  - [ ] Test Pests page API calls.
- [ ] Test LoginPage for authentication flows.
- [ ] Test Navbar functionality and logout flow.
- [ ] Check UI responsiveness and styling consistency.

## Backend Thorough Testing

- [ ] Main App API (port 5000): Test endpoints /api/analyze-location, /api/status, /health.
- [ ] NDVI Service (port 5001): Test /api/ndvi/analyze and related endpoints.
- [ ] Soil Service (port 5002): Test /api/soil/analyze and related endpoints.
- [ ] Weather Service (port 5003): Test /api/weather/current, /api/weather/agricultural.
- [ ] Crop Service (port 5004): Test /api/crop/recommend.
- [ ] Water Service (port 5005): Test /api/water/irrigation/calculate.
- [ ] Pest & Disease Service (port 5006): Test /api/threats/comprehensive and related.

For each endpoint:

- [ ] Test happy path with valid input.
- [ ] Test invalid and edge case inputs.
- [ ] Validate response correctness and HTTP status.
- [ ] Check error handling and timeouts.

---

Once this TODO is reviewed, I will begin implementing the tests step by step.
