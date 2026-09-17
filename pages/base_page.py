"""
BasePage: the parent of every Page Object.

Why this exists
---------------
Every page needs the same low-level actions: click something, type into a
field, read text, wait for an element to appear. Putting them here once means:
  * page objects stay short and readable
  * we use EXPLICIT waits (WebDriverWait) everywhere instead of time.sleep()
  * flaky "element not found yet" failures are handled in ONE place

Explicit waits vs time.sleep():
  time.sleep(3) always waits the full 3s and still races if the page is slow.
  WebDriverWait polls until the condition is true (or times out), so it is
  both faster on average and far more reliable. This is the single biggest
  lever against flaky UI tests -- see docs/test-plan.md.
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    # Default seconds any explicit wait will poll before giving up.
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # -- navigation -------------------------------------------------------
    def open(self, url):
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    # -- waited interactions ---------------------------------------------
    def _find_visible(self, locator):
        """Wait until the element is present AND visible, then return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _find_clickable(self, locator):
        """Wait until the element is clickable, then return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def _scroll_into_view(self, element):
        """Center an element in the viewport before interacting with it.

        Selenium's native click auto-scrolls, but doing it explicitly and
        centering the element avoids intermittent 'element not interactable'
        / missed clicks for items lower on the page in headless mode.
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def click(self, locator):
        element = self._find_clickable(locator)
        self._scroll_into_view(element)
        element.click()

    def type(self, locator, text):
        el = self._find_visible(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator):
        return self._find_visible(locator).text

    def is_visible(self, locator, timeout=None):
        """Return True if the element becomes visible within the timeout."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def find_all(self, locator):
        """Wait for at least one match, then return every matching element."""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
