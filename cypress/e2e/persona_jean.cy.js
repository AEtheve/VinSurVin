describe('Persona Jean', () => {
  beforeEach(() => {
    cy.viewport(1280, 720)
  })

  it('passes', () => {
    cy.visit('http://localhost:5173/');
    cy.get('#explorer-button').click();
    cy.wait(1000);
    cy.get('.pagination-controls').scrollIntoView();
    cy.wait(1000);
    cy.get(':nth-child(1) > #product-box > a > .product_card > .overlay').scrollIntoView();
    cy.wait(1000);
    cy.get(':nth-child(1) > #product-box > a > .product_card > .overlay').click();  
    cy.get('.cart_button').scrollIntoView();
    cy.wait(1000);
    cy.get('.cart_button').click();
  })
})