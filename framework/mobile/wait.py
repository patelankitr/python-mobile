import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
import json
from framework.mobile.prints import text_print
locator_map = {
            'xpath': AppiumBy.XPATH,
            'id': AppiumBy.ID,
            'path': AppiumBy.XPATH,
            'content': AppiumBy.ACCESSIBILITY_ID,
            'uiautomator':AppiumBy.ANDROID_UIAUTOMATOR,
            'class': AppiumBy.CLASS_NAME
}
class Wait:
    def __init__(self, driver, file_path):
        self.driver = driver
        self.file_path = file_path
        self.locators = self.load_locators()

    def load_locators(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading locators from {self.file_path}: {str(e)}")
            return {}


    def wait_until_element_is_visible(self, locator_name):
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

            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((by_type, locator_value))
            )
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not visible after 30 seconds")
        except ValueError as e:
            raise ValueError(str(e))
        
    def wait_for_seconds(self, seconds):
        """
        Pauses the execution for the specified number of seconds.
        
        Args:
            seconds (int/float): The number of seconds to wait
        """
        time.sleep(seconds)
        text_print(f"Waited for {seconds} seconds","🔄","green")
