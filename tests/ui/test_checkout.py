"""
Checkout tests.

  * A full happy-path checkout, data-driven from data/checkout_data.csv.
  * A negative test: checkout with a missing first name is rejected.
"""

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.ui.conftest import load_checkout_rows

_CHECKOUT_ROWS = load_checkout_rows()


@allure.feature("Checkout")
@allure.story("Complete an order")
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.parametrize(
    "row",
    _CHECKOUT_ROWS,
    ids=[f"{r['first_name']}-{r['item_slug']}" for r in _CHECKOUT_ROWS],
)
def test_complete_checkout(driver, inventory_page, row):
    """Add an item and complete checkout with customer data from the CSV."""
    inventory_page.add_item_to_cart(row["item_slug"])
    inventory_page.go_to_cart()

    CartPage(driver).proceed_to_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_customer_info(
        row["first_name"], row["last_name"], row["postal_code"]
    )
    checkout.finish()

    assert checkout.is_order_complete()
    assert "Thank you for your order" in checkout.confirmation_message()


@allure.feature("Checkout")
@allure.story("Reject missing customer information")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.ui
def test_checkout_missing_first_name_is_rejected(driver, inventory_page):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()
    CartPage(driver).proceed_to_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_customer_info("", "Hopper", "110001")

    assert checkout.has_error()
    assert "First Name is required" in checkout.error_text()
