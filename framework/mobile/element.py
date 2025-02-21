import json
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from framework.mobile.prints import text_print
from framework.init.base import locator_map

class Element:


    def __init__(self, driver, file_path):
        text_print(f"Initializing Element class with file_path: {file_path}",'green')  # Debug log
        if not driver:
            raise ValueError("Driver cannot be None")
        if not file_path:
            raise ValueError("File path cannot be None")
            
        self.file_path = file_path
        self.locators = self.load_locators()
        self.driver = driver
        text_print("Element class initialized successfully",'green')  # Debug log

    def load_locators(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                locators = json.load(file)
                return locators
        except Exception as e:
            print(f"Error loading locator file: {e}")
            return {}

    def get_locator(self, locator_name):
        locator = self.locators.get(locator_name)
        if not locator:
            raise ValueError(f"Locator '{locator_name}' not found in the locators file.")
        return locator

    def _find_element(self, locator):
        locator_type = locator.get("locator_type").lower()
        locator_value = locator.get("locator")  # Direct reference to locator
        
        by_type = locator_map.get(locator_type)
        if not by_type:
            raise ValueError(f"Unsupported locator type: {locator_type}")
            
        return self.driver.find_element(by_type, locator_value)

    def tap_on_element(self, locator_name, timeout=1):
        try:
            locator = self.get_locator(locator_name)
            locator_type = locator.get("locator_type").lower()
            locator_value = locator.get("locator")
            
            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            
            # Wait for element to be clickable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by_type, locator_value))
            )
            element.click()
            text_print(f"Clicked on {locator_name}",'green')
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not clickable after {timeout} seconds")

    def enter_text(self, locator_name, text_to_enter, timeout=1):
        try:
            locator = self.get_locator(locator_name)
            locator_type = locator.get("locator_type").lower()
            locator_value = locator.get("locator")
            
            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            
            # Wait for element to be present and interactable
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, locator_value))
            )
            element.clear()
            element.send_keys(text_to_enter)
            print(f"Entered text in {locator_name}: {text_to_enter}")
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error entering text in '{locator_name}': {str(e)}")
