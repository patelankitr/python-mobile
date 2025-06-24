import base64
import json
import os
from pathlib import Path
from framework.readers.fileReader import FileReader
from framework.mobile.prints import text_print

class WebElementActions:
    """
    Reusable actions for web elements using Playwright.
    """
    def __init__(self, page, file_path):
        self.page = page
        self.file_path = file_path
        self.locators = self.load_locators()

    def load_locators(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                locators = json.load(file)
                return locators
        except Exception as e:
            print(f"Error loading locator file: {e}")
            return {}      

    def get_locator(self, locator_name):
        """
        Retrieve locator_type and locator from a JSON file based on a key.
        Args:
            key (str): The key in the JSON file (e.g., 'login_mobile_number')
            json_path (str or Path): Path to the JSON file. If None, uses default Sadak login path.
        Returns:
            tuple: (locator_type, locator)
        """
        
        # Default to Sadak login page object JSON
        json_path = self.file_path
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        locator_info = data.get(locator_name)
        if not locator_info:
            raise KeyError(f"Locator key '{locator_name}' not found in {json_path}")
        return locator_info["locator_type"], locator_info["locator"]

    async def enter_text(self, locator_name, text_to_enter, timeout=10, highlight=False, label=None):
        """
        Enter text into an element using Playwright, supporting dynamic locator types.
        Args:
            locator_name (str): The name of the locator (e.g., 'mobile_input', 'password_input')
            text_to_enter (str): The text to enter
            timeout (int): Timeout in seconds (default: 10)
            highlight (bool): Whether to highlight the element (default: False)
            label (str): Optional label for highlighting
        """
        locator_type, locator_value = self.get_locator(locator_name)
        print(f"Using locator type: {locator_type}, value: {locator_value}")
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

        # Wait for element to be visible and enabled
        await locator.wait_for(state="visible", timeout=timeout * 1000)
        await locator.fill("")  # Clear existing text
        await locator.fill(text_to_enter)

        if highlight:
            # Optionally highlight the element (custom JS or screenshot logic can be added here)
            await self.page.evaluate(
                "el => el.style.border = '2px solid red'", await locator.element_handle()
            )
        # Optionally print debug info
        if label:
            print(f"Entered text in {label}: {text_to_enter}")

    async def click_element(self, locator_name, timeout=10, highlight=False, label=None):
        """
        Click an element using Playwright, supporting dynamic locator types.
        Args:
            locator_name (str): The name of the locator (e.g., 'mobile_input', 'password_input')
            timeout (int): Timeout in seconds (default: 10)
            highlight (bool): Whether to highlight the element (default: False)
            label (str): Optional label for highlighting
        """
        locator = self.page.locator(locator_name)
        print(f"Using locator: {locator}")
        locator_type, locator_value = self.get_locator(locator_name)
        print(f"Using locator type: {locator_type}, value: {locator_value}")
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

        locator = locator.first
        # Wait for element to be visible and enabled (clickable)
        await locator.wait_for(state="visible", timeout=timeout * 1000)
        await locator.wait_for(state="attached", timeout=timeout * 1000)
        # await locator.wait_for(state="enabled", timeout=timeout * 1000)

        if highlight:
            await self.page.evaluate(
                "el => el.style.border = '2px solid red'", await locator.element_handle()
            )
        await locator.click()
        if label:
            print(f"Clicked on {label}")

    async def fill_otp_by_locator(self, locator_key, otp_value, json_path=None, timeout=60000, delay=300):
        """
        Fills OTP fields by focusing the first input and typing the OTP value.
        Args:
            locator_key (str): Key in the JSON locator file for the first OTP input
            otp_value (str): The OTP value to type (e.g., '123456')
            json_path (str, optional): Path to the locator JSON file
            timeout (int): Timeout in ms for waiting for the first OTP input (default: 60000)
            delay (int): Delay in ms between typing each digit (default: 300)
        """
        locator_type, locator_value = self.get_locator(locator_key)
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

        otp_input = await locator.wait_for(state="visible", timeout=timeout)
        # await otp_input.focus()
        for digit in otp_value:
            await self.page.keyboard.type(digit)
            await self.page.wait_for_timeout(delay)

    async def enter_text_from_file(self, locator_name, file_name, cell_reference, sheet_name=None, json_path=None, timeout=10, highlight=False):
        """
        Reads a value from a file (CSV or Excel) and enters it into the specified element using Playwright.
        Args:
            locator_name (str): Key in the JSON file for the locator.
            file_name (str): Name of the file to read the data from (.csv or .xlsx).
            cell_reference (str): Cell reference (e.g., 'A1' for Excel, or column name for CSV).
            sheet_name (str, optional): Name of the sheet (required for Excel files).
            json_path (str, optional): Path to the locator JSON file.
            timeout (int): Timeout in seconds (default: 10).
            highlight (bool): Whether to highlight the element (default: False).
        Returns:
            The value read from the file (cell_reference value)
        Raises:
            Exception: If the value is empty, or if file type is unsupported or reading fails.
        """
        try:
            extension = Path(file_name).suffix.lower()
            text_print(f"Detected file extension: {extension}", 'blue')

            if extension in ['.xlsx', '.xls']:
                if not sheet_name:
                    raise ValueError("sheet_name must be provided for Excel files.")
                value = FileReader.get_cell_value_from_excel(file_name, sheet_name, cell_reference)
                text_print(f"Value from Excel ({sheet_name}:{cell_reference}): {value}", 'blue')
            elif extension == '.csv':
                value = FileReader.read_csv_cell(file_name, cell_reference)
                text_print(f"Value from CSV column '{cell_reference}': {value}", 'blue')
            else:
                raise ValueError(f"Unsupported file extension: {extension}")

            if value is None or str(value).strip() == "":
                raise ValueError(f"No value found in file '{file_name}' at reference '{cell_reference}'")

            await self.enter_text(locator_name, str(value), timeout=timeout, highlight=highlight, label=locator_name)
            text_print(f"Entered text into '{locator_name}': {value}", 'green')
            return value
        except Exception as e:
            raise Exception(f"Error in enter_text_from_file: {str(e)}")

    # async def select_dropdown_option_by_text(
    #     self,
    #     dropdown_locator,
    #     option_text,
    #     dropdown_by,              # 'locator', 'text', 'xpath'
    #     options_locator,     # Optional selector for all options
    #     option_by_text_template,  # Optional template like "//div[.='{option_text}']"
    #     timeout: int = 10
    # ):
    #     """
    #     Generic method to select an option from any dropdown based on visible text.

    #     Args:
    #         dropdown_locator (str): Selector or text used to open the dropdown.
    #         option_text (str): Visible text to select from the dropdown.
    #         dropdown_by (str): Strategy to locate dropdown - 'locator', 'xpath', 'text'
    #         options_locator (str, optional): Selector for all dropdown options.
    #         option_by_text_template (str, optional): Xpath/CSS template with {option_text} to locate desired option.
    #         timeout (int): Timeout in seconds.
    #     """

    #     try:

    #          # STEP 1: Open the dropdown using the reusable click_element()
    #         await self.click_element(
    #             locator_name=dropdown_locator,
    #             timeout=timeout
    #         )

    #         await self.page.wait_for_timeout(500)  # Allow options to render

    #         # STEP 2: Build the option locator dynamically
    #         if option_by_text_template:
    #             formatted_option = option_by_text_template.format(option_text=option_text)
    #             option_locator = self.page.locator(formatted_option)
    #         else:
    #             option_locator = self.page.get_by_text(option_text)

    #         count = await option_locator.count()
    #         print(f"🔍 Found {count} option(s) matching '{option_text}'")

    #         # STEP 3: Fallback: list all available options for debugging
    #         if count == 0:
    #             if options_locator:
    #                 all_options = self.page.locator(options_locator)
    #                 total = await all_options.count()
    #                 print(f"❌ Option '{option_text}' not found. Available options:")
    #                 for i in range(total):
    #                     txt = await all_options.nth(i).inner_text()
    #                     print(f"  • Option {i}: {txt}")
    #             raise Exception(f"Dropdown option '{option_text}' not found.")    

    #         # STEP 4: Click the matching option
    #         await option_locator.first.wait_for(state="visible", timeout=timeout * 1000)

    #         # if highlight:
    #         #     await self.page.evaluate(
    #         #         "el => el.style.border = '2px solid green'",
    #         #         await option_locator.first.element_handle()
    #         #     )

    #         await option_locator.first.click()
    #         print(f"✅ Selected option '{option_text}' from dropdown '{dropdown_locator_name}'")

    #     except Exception as e:
    #         raise Exception(f"⚠️ Failed to select dropdown option '{option_text}': {str(e)}")    
        
    async def select_dropdown_option_by_text(
        self,
        dropdown_locator_name,
        option_text,
        option_locator_xpath="//div[contains(@class, 'ng-option') and contains(., '{option_text}')]",
        all_options_xpath="//div[contains(@class, 'ng-option')]",
        timeout=10
    ):
        """
        Opens a dropdown and selects an option by visible text. Generic for any dropdown structure.
        Args:
            dropdown_locator_name (str): The locator name for the dropdown (from JSON)
            option_text (str): The visible text of the option to select
            option_locator_xpath (str): XPath for the dropdown option (default: ng-option)
            all_options_xpath (str): XPath for all dropdown options (default: ng-option)
            timeout (int): Timeout in seconds (default: 10)
        """
        # Open the dropdown
        await self.click_element(dropdown_locator_name, timeout=timeout)
        await self.page.wait_for_timeout(500)  # Wait for options to render
        option_locator_xpath="//div[contains(@class, 'ng-option') and contains(., '{option_text}')]"
        all_options_xpath="//div[contains(@class, 'ng-option')]"
        # Format the option locator with the desired text
        formatted_option_xpath = option_locator_xpath.format(option_text=option_text)
        option_locator = self.page.locator(formatted_option_xpath)
        count = await option_locator.count()
        print(f"Found {count} options matching '{option_text}'")
        if count == 0:
            # Print all available options for debugging
            all_options = self.page.locator(all_options_xpath)
            all_count = await all_options.count()
            print(f"All options count: {all_count}")
            for i in range(all_count):
                text = await all_options.nth(i).inner_text()
                print(f"Option {i}: {text}")
            raise Exception(f"Dropdown option '{option_text}' not found after opening dropdown")
        await option_locator.first.wait_for(state="visible", timeout=timeout * 1000)
        await option_locator.first.click()
        print(f"Selected option '{option_text}' from dropdown '{dropdown_locator_name}'")

    async def get_text(self, locator_name, timeout=10):
        """
            Gets text from the specified element using Playwright.

            Args:
                locator_name (str): Name of the locator in the JSON file
                timeout (int): Maximum time to wait for element presence (default 10 seconds)

            Returns:
                str: Text content of the element
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

            # Wait for element to be visible
            await locator.wait_for(state="visible", timeout=timeout * 1000)
            # Get text from element
            element_text = await locator.inner_text()
            text_print(f"Text from {locator_name}: {element_text}", 'green')
            return element_text
        except Exception as e:
            raise Exception(f"Error getting text from '{locator_name}': {str(e)}")
        
    async def swipe_element_to_element(self, start_locator_name, end_locator_name, duration=None, timeout=10):
        """
        Simulates a swipe (drag-and-drop) from one element to another using Playwright for web.

        Args:
            start_locator_name (str): Name of the starting element locator
            end_locator_name (str): Name of the ending element locator
            duration (int, optional): Time in milliseconds for the swipe action (simulated with wait)
            timeout (int): Maximum time to wait for elements to be present (default 10 seconds)
        """
        try:
            # Get locators
            start_type, start_value = self.get_locator(start_locator_name)
            end_type, end_value = self.get_locator(end_locator_name)
            # Map locator_type to Playwright locator method
            if start_type.lower() == "css":
                start_locator = self.page.locator(start_value)
            elif start_type.lower() == "xpath":
                start_locator = self.page.locator(f"xpath={start_value}")
            elif start_type.lower() == "text":
                start_locator = self.page.get_by_text(start_value)
            else:
                raise ValueError(f"Unsupported locator type: {start_type}")

            if end_type.lower() == "css":
                end_locator = self.page.locator(end_value)
            elif end_type.lower() == "xpath":
                end_locator = self.page.locator(f"xpath={end_value}")
            elif end_type.lower() == "text":
                end_locator = self.page.get_by_text(end_value)
            else:
                raise ValueError(f"Unsupported locator type: {end_type}")

            # Wait for both elements to be visible
            await start_locator.wait_for(state="visible", timeout=timeout * 1000)
            await end_locator.wait_for(state="visible", timeout=timeout * 1000)

            # Get bounding boxes
            start_box = await start_locator.bounding_box()
            end_box = await end_locator.bounding_box()
            if not start_box or not end_box:
                raise Exception("Could not get bounding box for one or both elements.")

            # Calculate center points
            start_x = start_box["x"] + start_box["width"] / 2
            start_y = start_box["y"] + start_box["height"] / 2
            end_x = end_box["x"] + end_box["width"] / 2
            end_y = end_box["y"] + end_box["height"] / 2

            # Perform drag and drop (simulate swipe)
            await self.page.mouse.move(start_x, start_y)
            await self.page.mouse.down()
            if duration:
                # Simulate slow drag
                steps = 20
                for i in range(1, steps + 1):
                    intermediate_x = start_x + (end_x - start_x) * i / steps
                    intermediate_y = start_y + (end_y - start_y) * i / steps
                    await self.page.mouse.move(intermediate_x, intermediate_y)
                    await self.page.wait_for_timeout(duration // steps)
            else:
                await self.page.mouse.move(end_x, end_y)
            await self.page.mouse.up()

            text_print(f"Swiped from {start_locator_name} to {end_locator_name}", 'green')

        except Exception as e:
            raise Exception(f"Error performing element to element swipe: {str(e)}")

    async def scroll_until_visible(self, selector: str, step: int = 300, max_scrolls: int = 10):
        locator_type, locator_value = self.get_locator(selector)
        locator_type = locator_type.lower()
        for i in range(max_scrolls):
            if await self.page.locator(locator_value).is_visible():
                print(f"✅ Element {locator_value} is now visible.")
                return
            print(f"🔁 Scroll attempt {i+1}")
            await self.page.evaluate(f"window.scrollBy(0, {step})")
            await self.page.wait_for_timeout(500)
        raise Exception(f"❌ Element {locator_value} not found after {max_scrolls} scrolls.")


    async def scroll_to_element(self, locator_name, timeout=10):
        """
        Scrolls the page to bring the specified element into view using Playwright.

        Args:
            locator_name (str): The locator name in the JSON file.
            timeout (int): Maximum time to wait for the element to be present (default 10 seconds).
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

            await locator.wait_for(state="attached", timeout=timeout * 1000)
            element_handle = await locator.element_handle()
            if element_handle:
                await element_handle.scroll_into_view_if_needed()
                print(f"✅ Scrolled to element '{locator_name}'")
            else:
                raise Exception(f"Element handle for '{locator_name}' not found.")
        except Exception as e:
            raise Exception(f"Error scrolling to element '{locator_name}': {str(e)}")


