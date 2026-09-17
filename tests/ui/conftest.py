"""
UI-layer fixtures and data loaders.

Kept separate from the root conftest so API tests don't import Selenium
helpers they never use.
"""

import csv
import json
from pathlib import Path

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Repo-root/data directory, resolved relative to this file so it works no
# matter what directory pytest is launched from.
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


# --- Data-driven loaders ------------------------------------------------
def load_login_data():
    with open(DATA_DIR / "login_data.json", encoding="utf-8") as f:
        return json.load(f)


def load_checkout_rows():
    with open(DATA_DIR / "checkout_data.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# --- Fixtures -----------------------------------------------------------
@pytest.fixture
def login_page(driver, base_url):
    """A freshly loaded login page."""
    return LoginPage(driver).load(base_url)


@pytest.fixture
def inventory_page(driver, base_url):
    """Log in as the standard user and return the inventory Page Object."""
    LoginPage(driver).load(base_url).login(STANDARD_USER, PASSWORD)
    page = InventoryPage(driver)
    assert page.is_loaded(), "Precondition failed: standard user did not reach inventory"
    return page
