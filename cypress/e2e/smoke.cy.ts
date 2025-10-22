describe("CropEye smoke", () => {
  it("loads the app root and shows branding", () => {
    // visit root (Cypress will use baseUrl from cypress.config.ts)
    cy.visit("/");

    // basic sanity checks
    cy.get("body").should("exist");

    // check for branding text or logo (case-insensitive)
    cy.contains(/CropEye/i).should("exist");
  });
});
