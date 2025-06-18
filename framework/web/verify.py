from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from colorama import Fore

class WebVerify:
    def __init__(self, page):
        """Initialize WebVerify with a Playwright page instance

        Args:
            page: Playwright page instance
        """
        self.page = page

    async def element_present(self, selector, timeout=10):
        """Verifies if an element is present in the DOM.

        Args:
            selector (str): CSS selector or XPath for the element
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            bool: True if element is present

        Raises:
            TimeoutException: If element is not present within timeout period
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout * 1000)
            print(Fore.GREEN + f"Element '{selector}' is present")
            return True
        except TimeoutException:
            raise TimeoutException(f"Element '{selector}' not present after {timeout} seconds")

    async def verify_title(self, expected_title, timeout=10):
        """Verifies if the page title contains the expected text.

        Args:
            expected_title (str): Expected text in the page title
            timeout (int): Maximum time to wait for title (default 10 seconds)

        Returns:
            bool: True if title contains expected text

        Raises:
            TimeoutException: If title verification fails within timeout period
            AssertionError: If title does not contain expected text
        """
        try:
            title = await self.page.title()
            assert expected_title in title, f"Expected '{expected_title}' in title, but got: {title}"
            print(Fore.GREEN + f"Page title contains '{expected_title}'")
            return True
        except TimeoutException:
            raise TimeoutException(f"Title verification failed after {timeout} seconds")

    async def verify_url(self, expected_url: str):
        """
        Assert that the current page URL matches the expected URL.
        Args:
            expected_url (str): The URL to verify
        Raises:
            AssertionError: If the current URL does not match expected_url
        """
        actual_url = self.page.url if not callable(self.page.url) else await self.page.url()
        assert actual_url == expected_url, f"Expected URL '{expected_url}', but got '{actual_url}'"