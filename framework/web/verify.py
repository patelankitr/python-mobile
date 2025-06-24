from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from framework.mobile.prints import text_print
from framework.web.elements import WebElementActions
from colorama import Fore

class WebVerify:
    def __init__(self, page, file_path):
        """Initialize WebVerify with a Playwright page instance

        Args:
            page: Playwright page instance
        """
        self.page = page
        self.file_path = file_path

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

    async def element_visible(self, locator_name, timeout=10):
        """
        Checks if an element is visible on the page using Playwright.
        Args:
            locator_name (str): The name of the locator (from JSON)
            timeout (int): Timeout in seconds (default: 10)
        Returns:
            bool: True if element is visible, raises TimeoutError otherwise
        """
        actions = WebElementActions(self.page, self.file_path)
        locator_type, locator_value = actions.get_locator(locator_name)
        locator_type = locator_type.lower()
        # Map locator_type to Playwright locator method
        if locator_type == "css":
            locator = self.page.locator(locator_value)
        elif locator_type == "xpath":
            locator = self.page.locator(f"xpath={locator_value}")
        elif locator_type == "text":
            locator = self.page.get_by_text(locator_value)
        elif locator_type == "placeholder":
            locator = self.page.get_by_placeholder(locator_value)
        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")
        try:
            await locator.wait_for(state="visible", timeout=timeout * 1000)
            text_print(f"Element '{locator_name}' is visible", "green")
            return True
        except Exception:
            raise TimeoutError(f"Element '{locator_name}' not visible after {timeout} seconds")

    async def verify_element_text(self, locator_name, expected_text, contains=False, case_sensitive=True, timeout=10):
        """
        Gets text from element and verifies it against expected text using Playwright.

        Args:
            locator_name (str): Name of the locator in the JSON file
            expected_text (str): Text to verify against
            contains (bool): If True, checks if element text contains expected text. If False, checks for exact match
            case_sensitive (bool): If True, performs case-sensitive comparison. If False, converts both to lowercase
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            bool: True if verification passes, False otherwise
        """
        try:
            actions = WebElementActions(self.page, self.file_path)

            locator_type, locator_value = actions.get_locator(locator_name)
            locator_type = locator_type.lower()
            # Map locator_type to Playwright locator method
            if locator_type == "css":
                locator = self.page.locator(locator_value)
            elif locator_type == "xpath":
                locator = self.page.locator(f"xpath={locator_value}")
            elif locator_type == "text":
                locator = self.page.get_by_text(locator_value)
            elif locator_type == "placeholder":
                locator = self.page.get_by_placeholder(locator_value)
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")

            # Wait for element to be visible
            await locator.wait_for(state="visible", timeout=timeout * 1000)
            # Get text from element
            actual_text = await locator.inner_text()

            # Prepare texts for comparison
            if not case_sensitive:
                actual_text = actual_text.lower()
                expected_text = expected_text.lower()

            # Perform verification
            if contains:
                result = expected_text in actual_text
                comparison_type = "contains"
            else:
                result = actual_text == expected_text
                comparison_type = "matches"

            # Log result
            if result:
                text_print(
                    f"Text verification passed for {locator_name}. "
                    f"Text {comparison_type}: '{expected_text}'", 'green'
                )
            else:
                text_print(
                    f"Text verification failed for {locator_name}. "
                    f"Expected text {comparison_type}: '{expected_text}', "
                    f"Actual text: '{actual_text}'", 'red'
                )

            return result

        except Exception as e:
            raise Exception(f"Error verifying text for '{locator_name}': {str(e)}")

    async def element_not_visible(self, locator_name, timeout=10):
        """
        Waits until the element is not visible (detached or hidden) using Playwright.
        Args:
            locator_name (str): Name of the locator in the JSON file
            timeout (int): Maximum time to wait for element to become not visible (default 10 seconds)
        Returns:
            bool: True if the element is not visible within the timeout, raises otherwise
        """
        try:
            locator_type, locator_value = self.get_locator(locator_name)
            locator_type = locator_type.lower()
            # Map locator_type to Playwright locator method
            if locator_type == "css":
                locator = self.page.locator(locator_value)
            elif locator_type == "xpath":
                locator = self.page.locator(f"xpath={locator_value}")
            elif locator_type == "text":
                locator = self.page.get_by_text(locator_value)
            elif locator_type == "placeholder":
                locator = self.page.get_by_placeholder(locator_value)
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")

            # Wait for element to be hidden or detached
            await locator.wait_for(state="hidden", timeout=timeout * 1000)
            text_print(f"Element '{locator_name}' is not visible", "green")
            return True
        except Exception:
            raise Exception(f"Element '{locator_name}' still visible after {timeout} seconds")