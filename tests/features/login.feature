Feature: SauceDemo login
  As a shopper
  I want to sign in to the store
  So that I can browse and buy products

  Background:
    Given the login page is open

  @smoke @bdd
  Scenario: Successful login with valid credentials
    When I log in as "standard_user" with password "secret_sauce"
    Then I should land on the products page

  @regression @bdd @negative
  Scenario: Locked-out user is rejected
    When I log in as "locked_out_user" with password "secret_sauce"
    Then I should see the error "Sorry, this user has been locked out."

  @regression @bdd @negative
  Scenario: Wrong password is rejected
    When I log in as "standard_user" with password "wrong_password"
    Then I should see the error "Username and password do not match any user in this service"
