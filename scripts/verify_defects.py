"""
Verify the planted SauceDemo defects firsthand (defect log DEF-02, DEF-03).

Logs in as `problem_user` and checks:
  * DEF-02: product images are all identical (wrong image mapping)
  * DEF-03: the sort dropdown does not reorder products

Run:  python scripts/verify_defects.py
Prints a CONFIRMED / NOT CONFIRMED verdict for each so you can speak to them
in an interview and set the defect-log status with evidence.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")


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
        LoginPage(driver).load(BASE_URL).login("problem_user", "secret_sauce")
        inventory = InventoryPage(driver)
        assert inventory.is_loaded(), "problem_user did not reach inventory"

        # --- DEF-02: are all product images the same? ---
        imgs = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_img img")
        srcs = [i.get_attribute("src") for i in imgs]
        unique = set(srcs)
        def02 = len(unique) == 1 and len(srcs) > 1
        print(f"DEF-02 (identical product images): "
              f"{'CONFIRMED' if def02 else 'NOT CONFIRMED'} "
              f"-> {len(srcs)} images, {len(unique)} unique")

        # --- DEF-03: does the sort dropdown actually reorder? ---
        before = inventory.product_names()
        inventory.sort_by("Name (Z to A)")
        after = inventory.product_names()
        expected = sorted(before, reverse=True)
        # Bug present if the order did NOT change to the expected Z->A order.
        def03 = after != expected
        print(f"DEF-03 (sort dropdown does nothing): "
              f"{'CONFIRMED' if def03 else 'NOT CONFIRMED'} "
              f"-> after-sort order {'unchanged' if after == before else 'changed'}, "
              f"matches expected Z->A: {after == expected}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
