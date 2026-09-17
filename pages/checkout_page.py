"""
Page Object for the SauceDemo checkout flow.

Checkout is two screens:
  step one  -> customer information form (/checkout-step-one.html)
  step two  -> order overview + Finish   (/checkout-step-two.html)
  complete  -> confirmation page          (/checkout-complete.html)

They are modelled here as one Page Object because they are a single user
journey; the methods map onto each screen in order.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # --- Step one: customer information ---
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Step two: overview ---
    FINISH = (By.ID, "finish")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")

    # --- Complete ---
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_customer_info(self, first_name, last_name, postal_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)

    def error_text(self):
        return self.text_of(self.ERROR_MESSAGE)

    def finish(self):
        self.click(self.FINISH)

    def confirmation_message(self):
        """Return the 'Thank you for your order!' header text."""
        return self.text_of(self.COMPLETE_HEADER)

    def is_order_complete(self):
        return self.is_visible(self.COMPLETE_HEADER)
