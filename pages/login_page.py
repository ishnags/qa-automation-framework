"""Page Object for the SauceDemo login page (https://www.saucedemo.com)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # --- Locators (all in one place; if the UI changes, you fix them here) ---
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")

    PATH = "/"

    def load(self, base_url):
        """Open the login page and return self for chaining."""
        self.open(base_url + self.PATH)
        return self

    def is_loaded(self):
        """Smoke check: the login logo/branding is visible."""
        return self.is_visible(self.LOGIN_LOGO)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_text(self):
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)
