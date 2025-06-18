import base64
import json
import os
from pathlib import Path
from utils.screenshots import highlight_element
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from framework.mobile.prints import text_print
from framework.init.base import locator_map
from framework.readers.fileReader import FileReader
from playwright.async_api import Page, Locator
from typing import List, Any, Optional
from colorama import Fore
CONFIG_PATH = "config/TestConfig.json"

class Element:

    @staticmethod
    def load_config():
        if not os.path.exists(CONFIG_PATH):
            print(f"❌ Config file '{CONFIG_PATH}' not found.")
            sys.exit(1)
        with open(CONFIG_PATH) as f:
            return json.load(f)

    def __init__(self, file_path, page:Page):
        text_print(f"\n Initializing Element class with file_path: {file_path}",'green')  # Debug log
        # if not driver:
        #     raise ValueError("Driver cannot be None")
        if not file_path:
            raise ValueError("File path cannot be None")
            
        self.file_path = file_path
        self.locators = self.load_locators()
        self.page = page
        # self.driver = driver
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
            
        return self.page.find_element(by_type, locator_value)

    def click_element(self, locator_name, timeout=10000): # Playwright uses milliseconds for timeout
        try:
            print(Fore.GREEN +"\nSetting up test...")
            locator_details = self.get_locator(locator_name) # Assuming get_locator works for web locators too
            print(Fore.GREEN +"\nSetting up test...")
            # Playwright uses CSS selectors or XPath primarily. 
            # You might need to adjust get_locator or how locators are defined for web.
            # For this example, let's assume locator_value is a CSS selector or XPath string.
            locator_value = locator_details.get("locator") # Use the locator from the JSON file
            print(Fore.GREEN +"\nSetting up test...")

            # Convert timeout to milliseconds for Playwright
            playwright_timeout = timeout * 2000

            element = self.page.locator(locator_value)
            print(f"element")
            print(element)
            print(f"element")
            element.wait_for(state='visible', timeout=playwright_timeout)
            # element.wait_for(state='enabled', timeout=playwright_timeout) # 'enabled' is not a valid state for wait_for, 'visible' is usually sufficient before click
            
            # Highlighting in Playwright is typically done via its tracing tools or custom JavaScript.
            # For simplicity, direct visual highlighting like in Appium is omitted here.
            # If you have a custom highlight_element_playwright function, you can call it here.

            element.click(timeout=playwright_timeout)
            text_print(f"Clicked on {locator_name} using Playwright", 'green')
        except Exception as e: # Catching a broader exception as Playwright might raise different errors
            # Log the original Playwright error for more details
            detailed_error_message = f"Playwright click failed for '{locator_name}'. Error: {str(e)}"
            print(Fore.RED + detailed_error_message)
            # Raise a more generic exception or a custom one if you prefer
            raise Exception(f"Element '{locator_name}' not clickable or other error occurred. Details: {str(e)}")    

    # -----------------------------------
    # Element collection methods
    # -----------------------------------

    async def get_all_elements(self, selector: str) -> List[Locator]:
        """Get all locator handles matching the selector."""
        locator = self.page.locator(selector)
        return await locator.all()

    async def get_all_inner_texts(self, selector: str) -> List[str]:
        """Get inner texts (only visible text) of all matched elements."""
        locator = self.page.locator(selector)
        return await locator.all_inner_texts()

    async def get_all_text_contents(self, selector: str) -> List[str]:
        """Get all text content (even hidden/styled off) of matched elements."""
        locator = self.page.locator(selector)
        return await locator.all_text_contents()

    # -----------------------------------
    # Action methods
    # -----------------------------------

    async def click_element(self, selector: str, timeout: Optional[int] = 10000, force: bool = False):
        """
        Click on an element by selector.

        Args:
            selector (str): CSS/XPath selector.
            timeout (int): Wait time before failing (default 10s).
            force (bool): Force click even if element is not interactable.
        """
        await self.page.locator(selector).click(timeout=timeout, force=force)

    async def check_element(self, selector: str, force: bool = False):
        """
        Check a checkbox element.

        Args:
            selector (str): Checkbox selector.
            force (bool): Force action if necessary.
        """
        await self.page.locator(selector).check(force=force)

    async def evaluate_script_on_element(self, selector: str, script: str) -> Any:
        """
        Evaluate a JavaScript expression on the selected element.

        Args:
            selector (str): Element selector.
            script (str): JavaScript code to run in the context of the element.

        Returns:
            Any: Result of the evaluation.
        """
        locator = self.page.locator(selector)
        return await locator.evaluate(script)

    async def dispatch_event_on_element(self, selector: str, event_type: str, event_init: Optional[dict] = None):
        """
        Dispatch a DOM event on the given element.

        Args:
            selector (str): Element selector.
            event_type (str): Type of event (e.g., 'click', 'mouseover').
            event_init (dict, optional): Optional event initialization dictionary.
        """
        await self.page.locator(selector).dispatch_event(event_type, event_init or {})
    
    # def goto(self, url: str):
    #     self.page.goto(url)

    # def fill_textbox(self, selector: str, text: str):
    #     self.page.fill(selector, text)

    # def click_element(self, selector: str):
    #     self.page.click(selector)

    # def get_title(self) -> str:
    #     return self.page.title()