import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
import json
from framework.mobile.prints import text_print
from framework.init.base import locator_map
class Verify:
    def __init__(self, driver, file_path):
        self.driver = driver
        self.file_path = file_path
        self.locators = self.load_locators()

    def load_locators(self):
        """
        Load locators from a JSON file.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Locator file not found: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.file_path}")

    def element_visible(self, locator_name, timeout=10):
        try:
            locator = self.locators.get(locator_name)
            if not locator:
                raise ValueError(f"Locator '{locator_name}' not found in locators file")

            locator_type = locator.get("locator_type", "").lower()
            if not locator_type:
                raise ValueError(f"Locator type not specified for '{locator_name}'")

            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(
                    f"Unsupported locator type: '{locator_type}'. Supported types are: {list(locator_map.keys())}")

            locator_value = locator.get("locator")
            if not locator_value:
                raise ValueError(f"Locator value not specified for '{locator_name}'")

            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by_type, locator_value))
            )
            text_print(f"Element '{locator_name}' is visible", "green")
            return True
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not visible after {timeout} seconds")

    def element_not_visible(self, locator_name, timeout=10):
        try:
            locator = self.locators.get(locator_name)
            if not locator:
                raise ValueError(f"Locator '{locator_name}' not found in locators file")

            locator_type = locator.get("locator_type", "").lower()
            if not locator_type:
                raise ValueError(f"Locator type not specified for '{locator_name}'")

            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(
                    f"Unsupported locator type: '{locator_type}'. Supported types are: {list(locator_map.keys())}")

            locator_value = locator.get("locator")
            if not locator_value:
                raise ValueError(f"Locator value not specified for '{locator_name}'")
    
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by_type, locator_value))
            )
            text_print(f"Element '{locator_name}' is not visible", "green")
            return True
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' still visible after {timeout} seconds")


    def element_present(self, locator_name, timeout=10):
        """
        Verifies if an element is present in the DOM.

        Args:
            locator_name (str): Name of the locator in the JSON file
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            bool: True if element is present

        Raises:
            ValueError: If locator is invalid or missing
            TimeoutException: If element is not present within timeout period
            :param timeout:
            :param locator_name:
            :param self:
        """
        try:
            locator = self.locators.get(locator_name)
            if not locator:
                raise ValueError(f"Locator '{locator_name}' not found in locators file")

            locator_type = locator.get("locator_type", "").lower()
            if not locator_type:
                raise ValueError(f"Locator type not specified for '{locator_name}'")

            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(
                    f"Unsupported locator type: '{locator_type}'. Supported types are: {list(locator_map.keys())}")

            locator_value = locator.get("locator")
            if not locator_value:
                raise ValueError(f"Locator value not specified for '{locator_name}'")

            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, locator_value))
            )
            text_print(f"Element '{locator_name}' is present", "green")
            return True
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")

    def verify_element_text(self, locator_name, expected_text, contains=False, case_sensitive=True, timeout=10):
        """
        Gets text from element and verifies it against expected text.

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
            locator = self.locators.get(locator_name)
            locator_type = locator.get("locator_type").lower()
            locator_value = locator.get("locator")

            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(f"Unsupported locator type: {locator_type}")

            # Wait for element to be present
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, locator_value))
            )

            # Get text from element
            actual_text = element.text

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

        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error verifying text for '{locator_name}': {str(e)}")