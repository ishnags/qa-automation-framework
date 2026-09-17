"""Cart tests: adding items updates the badge, and items reach the cart page."""

import allure
import pytest

from pages.cart_page import CartPage


@allure.feature("Cart")
@allure.story("Add single item updates cart badge")
@pytest.mark.functional
@pytest.mark.ui
def test_add_item_updates_cart_count(inventory_page):
    assert inventory_page.cart_count() == 0
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    assert inventory_page.cart_count() == 1


@allure.feature("Cart")
@allure.story("Add multiple items")
@pytest.mark.functional
@pytest.mark.ui
def test_add_multiple_items(inventory_page):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.add_item_to_cart("sauce-labs-bike-light")
    inventory_page.add_item_to_cart("sauce-labs-bolt-t-shirt")
    assert inventory_page.cart_count() == 3


@allure.feature("Cart")
@allure.story("Items carry through to the cart page")
@pytest.mark.regression
@pytest.mark.ui
def test_item_appears_on_cart_page(driver, inventory_page):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()

    cart = CartPage(driver)
    assert cart.is_loaded()
    assert cart.item_count() == 1
    assert "Sauce Labs Backpack" in cart.item_names()
