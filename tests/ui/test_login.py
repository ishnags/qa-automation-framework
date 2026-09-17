"""
Login tests: smoke + data-driven positive/negative coverage.

Data-driven design: the valid users and the invalid-login cases are read from
data/login_data.json (see tests/ui/conftest.py). Adding a new case is a data
edit, not a code change -- that is the "maintainable design" signal.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage
from tests.ui.conftest import load_login_data

_LOGIN_DATA = load_login_data()


@allure.feature("Authentication")
@allure.story("Login page loads")
@pytest.mark.smoke
@pytest.mark.ui
def test_login_page_loads(login_page):
    """The login page renders and shows its branding."""
    assert login_page.is_loaded()


@allure.feature("Authentication")
@allure.story("Valid login")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "user",
    _LOGIN_DATA["valid_users"],
    ids=[u["username"] for u in _LOGIN_DATA["valid_users"]],
)
def test_valid_login(driver, login_page, user):
    """Each valid user lands on the inventory page after logging in."""
    login_page.login(user["username"], user["password"])
    assert InventoryPage(driver).is_loaded()


@allure.feature("Authentication")
@allure.story("Rejected login")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.parametrize(
    "case",
    _LOGIN_DATA["invalid_logins"],
    ids=[c["case"] for c in _LOGIN_DATA["invalid_logins"]],
)
def test_invalid_login_is_rejected(login_page, case):
    """Locked-out / wrong-password / empty-field logins show the right error."""
    login_page.login(case["username"], case["password"])
    assert login_page.has_error(), f"Expected an error for case '{case['case']}'"
    assert case["expected_error"] in login_page.error_text()
