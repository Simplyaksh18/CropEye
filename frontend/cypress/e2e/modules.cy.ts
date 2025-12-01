/// <reference types="cypress" />

describe("Module Pages Tests", () => {
  const modules = ["Crops", "NDVI", "Weather", "Soil", "Water", "Pests"];

  beforeEach(() => {
    cy.visit("/dashboard");
  });

  it("should set location input and navigate to each module page, verifying API data and UI elements", () => {
    const location = "Punjab";

    // Set location input on DashboardPage
    cy.get('input[data-testid="location-input"]').clear().type(location);
    cy.get('button[data-testid="submit-location"]').click();

    // Use Cypress-controlled iteration to avoid command queuing issues
    cy.wrap(modules).each((module) => {
      // Navigate to module page
      cy.contains(module).click();

      // Verify API data is fetched and displayed correctly
      cy.get('[data-testid="api-data"]').should("exist").and("not.be.empty");

      // Test loading state (should not be visible after load)
      cy.get('[data-testid="loading-spinner"]').should("not.exist");

      // Test error state by intercepting API requests and forcing an error on reload
      // Use a route matcher object to catch any method and be more robust
      cy.intercept({ url: "**/api/**" }, { statusCode: 500 }).as("apiError");
      cy.reload();
      cy.wait("@apiError");
      cy.get('[data-testid="error-message"]').should("exist");

      // Test interactive elements (buttons/forms/navigation)
      cy.get("button, input, select").first().should("be.visible");

      // Navigate back to dashboard for the next iteration
      cy.visit("/dashboard");
    });
  });
});
