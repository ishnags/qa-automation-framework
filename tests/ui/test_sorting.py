"""Regression: product sorting on the inventory page works both directions."""

import allure
import pytest


@allure.feature("Inventory")
@allure.story("Sort products by name")
@pytest.mark.regression
@pytest.mark.ui
def test_sort_name_a_to_z(inventory_page):
    inventory_page.sort_by("Name (A to Z)")
    names = inventory_page.product_names()
    assert names == sorted(names), "Products are not in ascending A->Z order"


@allure.feature("Inventory")
@allure.story("Sort products by name")
@pytest.mark.regression
@pytest.mark.ui
def test_sort_name_z_to_a(inventory_page):
    inventory_page.sort_by("Name (Z to A)")
    names = inventory_page.product_names()
    assert names == sorted(names, reverse=True), "Products are not in descending Z->A order"
