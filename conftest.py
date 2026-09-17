"""
Global pytest fixtures for the QA automation framework.

Responsibilities:
  * load configuration from environment / .env
  * build a Selenium WebDriver (local Chrome/Firefox OR remote Selenium Grid)
  * expose base URLs to tests
  * attach a screenshot to the Allure report whenever a UI test fails

Everything a test needs is injected as a fixture, so tests never create a
driver themselves. That keeps the tests short and the setup in one place.
"""

import os

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Load variables from a local .env file if present (no error if it is missing).
load_dotenv()


# ---------------------------------------------------------------------------
# Configuration fixture
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def config():
    """Central config read once per test session from the environment."""
    return {
        "ui_base_url": os.getenv("UI_BASE_URL", "https://www.saucedemo.com"),
        "api_base_url": os.getenv(
            "API_BASE_URL", "https://restful-booker.herokuapp.com"
        ),
        "api_username": os.getenv("API_USERNAME", "admin"),
        "api_password": os.getenv("API_PASSWORD", "password123"),
        "run_mode": os.getenv("RUN_MODE", "local").lower(),
        "remote_url": os.getenv("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub"),
        "browser": os.getenv("BROWSER", "chrome").lower(),
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
    }


@pytest.fixture(scope="session")
def base_url(config):
    """Convenience: the UI base URL on its own."""
    return config["ui_base_url"]


# ---------------------------------------------------------------------------
# WebDriver factory
# ---------------------------------------------------------------------------
def _build_chrome_options(headless: bool) -> ChromeOptions:
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    # Flags that make Chrome stable inside Docker / CI containers.
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    return opts


def _build_firefox_options(headless: bool) -> FirefoxOptions:
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--width=1920")
    opts.add_argument("--height=1080")
    return opts


def _make_driver(config):
    """Create a WebDriver based on RUN_MODE (local vs grid) and BROWSER."""
    browser = config["browser"]
    headless = config["headless"]

    if browser == "chrome":
        options = _build_chrome_options(headless)
    elif browser == "firefox":
        options = _build_firefox_options(headless)
    else:
        raise ValueError(f"Unsupported BROWSER '{browser}'. Use chrome or firefox.")

    if config["run_mode"] == "grid":
        # Remote execution against a Selenium Grid (used in Docker / parallel runs).
        return webdriver.Remote(command_executor=config["remote_url"], options=options)

    # --- Local execution ---
    # Selenium 4.6+ ships Selenium Manager, which auto-resolves the driver binary,
    # so no manual chromedriver path is needed.
    if browser == "chrome":
        return webdriver.Chrome(options=options)
    return webdriver.Firefox(options=options)


# ---------------------------------------------------------------------------
# Driver fixture (function-scoped: a fresh, isolated browser per test)
# ---------------------------------------------------------------------------
@pytest.fixture
def driver(config, request):
    """Yield a ready WebDriver and always quit it afterwards."""
    drv = _make_driver(config)
    drv.implicitly_wait(0)  # we rely on EXPLICIT waits, not implicit — see base_page

    # In headless mode the --window-size arg already fixes a stable 1920x1080
    # viewport; calling maximize_window() on top of it can snap the window to a
    # small virtual-display default, pushing lower page elements out of a
    # predictable position and causing intermittent click misses. Only maximize
    # when running headed (watching it locally).
    if not config["headless"]:
        drv.maximize_window()
    else:
        drv.set_window_size(1920, 1080)

    # Make the driver reachable from the failure hook below.
    request.node._driver = drv

    yield drv

    drv.quit()


# ---------------------------------------------------------------------------
# Screenshot-on-failure: attach a PNG to Allure when a UI test fails.
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = getattr(item, "_driver", None)
        if drv is not None:
            allure.attach(
                drv.get_screenshot_as_png(),
                name=f"failure-{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
