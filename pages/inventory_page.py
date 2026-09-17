"""Page Object for the SauceDemo inventory (products) page shown after login."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    # --- Locators ---
    TITLE = (By.CLASS_NAME, "title")  # header reading "Products"
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def is_loaded(self):
        """True once the inventory list is on screen (i.e. login succeeded)."""
        return self.is_visible(self.TITLE) and "inventory" in self.current_url()

    def add_item_to_cart(self, item_slug):
        """Add a product by its slug, e.g. 'sauce-labs-backpack'.

        Waits for the button to flip to its 'Remove' state, which is the
        page's own confirmation that the add registered -- more reliable than
        assuming the click took effect immediately.
        """
        self.click((By.ID, f"add-to-cart-{item_slug}"))
        # Confirm the add landed before returning control to the test.
        self.wait.until(
            EC.presence_of_element_located((By.ID, f"remove-{item_slug}"))
        )

    def cart_count(self):
        """Return the number shown on the cart badge, or 0 if it is absent."""
        if self.is_visible(self.CART_BADGE, timeout=5):
            return int(self.text_of(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    # --- Sorting (used by a regression test) ---
    def sort_by(self, visible_text):
        """Select a sort option, e.g. 'Name (Z to A)'."""
        dropdown = self._find_visible(self.SORT_DROPDOWN)
        Select(dropdown).select_by_visible_text(visible_text)

    def product_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAMES)]
