"""Page Object for the SauceDemo cart page (/cart.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    # --- Locators ---
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def is_loaded(self):
        return "cart" in self.current_url()

    def item_count(self):
        return len(self.find_all(self.CART_ITEM))

    def item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
