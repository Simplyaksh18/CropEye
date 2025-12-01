/// <reference types="cypress" />

// Provide minimal globals for TypeScript if cypress/mocha types aren't picked up
declare const describe: (name: string, fn: () => void) => void;
declare const it: (name: string, fn: () => void) => void;
declare const beforeEach: (fn: () => void) => void;

describe("DashboardPage Tests", () => {
  beforeEach(() => {
    cy.visit("/dashboard");
  });

  it("should display all modules and location input", () => {
    const modules = ["Crops", "NDVI", "Weather", "Soil", "Water", "Pests"];

    // Check location input presence
    cy.get('input[data-testid="location-input"]').should("exist");

    // Check each module card presence
    modules.forEach((module) => {
      cy.contains(module).should("exist");
    });
  });
});
