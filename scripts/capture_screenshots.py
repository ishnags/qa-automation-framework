"""
Capture a couple of proof screenshots for the README / portfolio.

Run:  python scripts/capture_screenshots.py
Output: docs/screenshots/*.png

This is a small utility, not part of the test suite. It drives the same Page
Objects the tests use, so it doubles as a live demo of the framework.
"""

import os
import sys
from pathlib import Path

# Make the project root importable when run from anywhere.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=opts)


def main():
    driver = make_driver()
    try:
        # 1. Login page
        login = LoginPage(driver).load(BASE_URL)
        assert login.is_loaded()
        driver.save_screenshot(str(OUT / "01_login_page.png"))

        # 2. Inventory after login
        login.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        assert inventory.is_loaded()
        inventory.add_item_to_cart("sauce-labs-backpack")
        driver.save_screenshot(str(OUT / "02_inventory_item_added.png"))

        # 3. Completed checkout ("Thank you for your order!")
        inventory.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("Ada", "Lovelace", "560001")
        checkout.finish()
        assert checkout.is_order_complete()
        driver.save_screenshot(str(OUT / "03_order_complete.png"))

        print(f"Saved screenshots to {OUT}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
