"""
Step definitions for tests/features/login.feature.

pytest-bdd turns each Scenario into a real pytest test, so it reuses the same
`driver`/`base_url`/`config` fixtures as the rest of the suite -- the Gherkin
layer sits on top of the existing Page Objects, it does not replace them.

The file must be named test_*.py so pytest collects the scenarios.
"""

from pytest_bdd import scenarios, given, when, then, parsers

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Bind every scenario in the feature file to this module.
scenarios("../login.feature")


@given("the login page is open", target_fixture="login_page")
def open_login_page(driver, base_url):
    return LoginPage(driver).load(base_url)


@when(
    parsers.parse('I log in as "{username}" with password "{password}"')
)
def do_login(login_page, username, password):
    login_page.login(username, password)


@then("I should land on the products page")
def on_products_page(driver):
    assert InventoryPage(driver).is_loaded()


@then(parsers.parse('I should see the error "{message}"'))
def see_error(login_page, message):
    assert login_page.has_error()
    assert message in login_page.error_text()
