ODO List for CropEye Frontend Updates

## 1. Update Preset Locations to Indian Samples

- [x] Modify `src/context/LocationContext.tsx` to replace US preset locations with Indian farming locations (e.g., Delhi, Mumbai, Bangalore, Chennai).

## 2. Ensure Sample Locations Set as Current Location and Trigger Analysis

- [x] Verify and update `src/components/LocationInput.tsx` so clicking preset locations sets the location and navigates to crops page for analysis calculation.

## 3. Make "Did You Know" Always Floating with Insights at Bottom

- [x] Update `src/components/DidYouKnowCard.tsx` to make it always visible (floating), place educational insights at the bottom of the page, and remove any toggling feature.

## 4. Make Footer Visible on Every Page

- [x] Modify `src/App.tsx` or relevant layout to ensure `Footer.tsx` is rendered on all pages.

## 5. Fix Navigation in Services (e.g., Pest Detection to Pest Page)

- [x] Update `src/components/ModuleCard.tsx` or relevant component to navigate to correct pages when clicking service modules (e.g., pest detection to `/pests`).

## 6. Confirm Mobile Responsiveness

- [x] Verify that the app supports mobile devices using Tailwind CSS responsive classes (sm:, md:, lg:).

## Followup Steps

- [ ] Test the app on mobile devices or emulators.
- [ ] Run the development server and check navigation, location setting, and UI elements.
- [ ] Ensure no console errors and all features work as expected.
