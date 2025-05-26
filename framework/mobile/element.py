import base64
import json
from pathlib import Path
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

class Element:


    def __init__(self, driver, file_path):
        text_print(f"\n Initializing Element class with file_path: {file_path}",'green')  # Debug log
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

    def tap_on_element(self, locator_name, timeout=10):
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

    
    def multi_tap(self, locator_name, tap_count=1, timeout=10):
        """
        Clicks on an element multiple times.

        Args:
            locator_name (str): Name of the locator in the JSON file
            tap_count (int): Number of times to click the element (default 1)
            timeout (int): Maximum time to wait for element presence (default 10 seconds)
        """
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
            
            # Perform multiple clicks
            for _ in range(tap_count):
                element.click()
            
            text_print(f"Clicked {tap_count} times on {locator_name}", 'green')
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not clickable after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error performing multiple clicks on '{locator_name}': {str(e)}")

    def long_press_element(self, locator_name, duration=1000, timeout=10):
        """
        Performs a long press on the specified element.

        Args:
            locator_name (str): Name of the locator in the JSON file
            duration (int): Duration to hold the press in milliseconds (default 1000ms)
            timeout (int): Maximum time to wait for element presence (default 10 seconds)
        """
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
            
            # Create touch action chain
            actions = ActionChains(self.driver)
            touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
            actions.w3c_actions = ActionBuilder(self.driver, mouse=touch_input)
            
            # Perform long press
            actions.w3c_actions.pointer_action.move_to(element)
            actions.w3c_actions.pointer_action.click_and_hold()
            actions.pause(duration / 1000)  # Convert milliseconds to seconds
            actions.release()
            actions.perform()
            
            text_print(f"Long pressed on {locator_name} for {duration}ms", 'green')
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not clickable after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error performing long press on '{locator_name}': {str(e)}")

    def enter_text(self, locator_name, text_to_enter, timeout=10):
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
            text_print(f"Entered text in {locator_name}: {text_to_enter}", 'green')
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error entering text in '{locator_name}': {str(e)}")
    def clear_and_enter_text(self, locator_name, text_to_enter, timeout=10):
            """
            Clears existing text and enters new text into the specified element.

            Args:
                locator_name (str): Name of the locator in the JSON file
                text_to_enter (str): Text to enter into the element
                timeout (int): Maximum time to wait for element presence (default 10 seconds)
            """
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
                
                # Clear existing text
                element.clear()
                text_print(f"Cleared text from {locator_name}", 'green')
                
                # Enter new text
                element.send_keys(text_to_enter)
                text_print(f"Entered new text in {locator_name}: {text_to_enter}", 'green')
                
            except TimeoutException:
                raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
            except Exception as e:
                raise Exception(f"Error in clear and enter text operation for '{locator_name}': {str(e)}")    
            
    def clear_text(self, locator_name, timeout=10):
        """
        Clears existing text and enters new text into the specified element.

        Args:
            locator_name (str): Name of the locator in the JSON file
            timeout (int): Maximum time to wait for element presence (default 10 seconds)
        """
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
            # Clear existing text
            element.clear()
            text_print(f"Cleared text from {locator_name}", 'green')

        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error in clear text operation for '{locator_name}': {str(e)}")        
    def enter_text_from_file(self, locator_name, file_name, cell_reference, sheet_name=None):
        """
        Reads a value from a file (CSV or Excel) and enters it into the specified element.

        Args:
            locator_name (str): Name of the locator in the JSON file.
            file_name (str): Name of the file to read the data from (.csv or .xlsx).
            cell_reference (str): Cell reference (e.g., 'A1' for Excel, or column name for CSV).
            sheet_name (str, optional): Name of the sheet (required for Excel files).

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

            # Check if value is None or empty
            if value is None or str(value).strip() == "":
                raise ValueError(f"No value found in file '{file_name}' at reference '{cell_reference}'")

            self.enter_text(locator_name, value)
            text_print(f"Entered text into '{locator_name}': {value}", 'green')

        except Exception as e:
            raise Exception(f"Error in enter_text_from_file: {str(e)}")


    # swipe from one element to another
    def swipe_element_to_element(self, start_locator_name, end_locator_name, duration=None, timeout=10):
        """
        Swipes from one element to another element.
        
        Args:
            start_locator_name (str): Name of the starting element locator
            end_locator_name (str): Name of the ending element locator
            duration (int, optional): Time in milliseconds for the swipe action
            timeout (int): Maximum time to wait for elements to be present (default 10 seconds)
            :param timeout:
            :param duration:
            :param end_locator_name:
            :param start_locator_name:
            :param self:
        """
        try:
            # Get start element locator and wait for presence
            start_locator = self.get_locator(start_locator_name)
            start_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    locator_map[start_locator.get("locator_type").lower()],
                    start_locator.get("locator")
                ))
            )
            
            # Get end element locator and wait for presence
            end_locator = self.get_locator(end_locator_name)
            end_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    locator_map[end_locator.get("locator_type").lower()],
                    end_locator.get("locator")
                ))
            )
            
            # Get element coordinates
            start_location = start_element.location
            end_location = end_element.location
            
            # Perform swipe
            action = self.driver.action()
            if duration:
                action.press(x=start_location['x'], y=start_location['y']) \
                    .wait(duration) \
                    .move_to(x=end_location['x'], y=end_location['y']) \
                    .release() \
                    .perform()
            else:
                action.press(x=start_location['x'], y=start_location['y']) \
                    .move_to(x=end_location['x'], y=end_location['y']) \
                    .release() \
                    .perform()
                
            text_print(f"Swiped from {start_locator_name} to {end_locator_name}", 'green')
            
        except TimeoutException:
            raise TimeoutException(f"Elements not found after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error performing element to element swipe: {str(e)}")

        # 1. Swipe from one element to another
        # element.swipe_element_to_element('start_button', 'end_button')
        # element.swipe_element_to_element('start_button', 'end_button', duration=500)  # with duration

    #swipe by direction
    def swipe_by_direction(self, direction, duration=None, percentage=0.75):
        """
        Swipes in the specified direction based on screen size.
        
        Args:
            direction (str): Direction to swipe ('left', 'right', 'up', 'down')
            duration (int, optional): Time in milliseconds for the swipe action
            percentage (float): Percentage of screen to swipe (0.0 to 1.0, default 0.75)
        """
        try:
            # Get screen dimensions
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            # Calculate swipe coordinates based on direction
            swipe_coords = {
                'left': {
                    'start_x': int(width * 0.8),
                    'start_y': int(height * 0.5),
                    'end_x': int(width * (1 - percentage)),
                    'end_y': int(height * 0.5)
                },
                'right': {
                    'start_x': int(width * 0.2),
                    'start_y': int(height * 0.5),
                    'end_x': int(width * percentage),
                    'end_y': int(height * 0.5)
                },
                'up': {
                    'start_x': int(width * 0.5),
                    'start_y': int(height * 0.7),
                    'end_x': int(width * 0.5),
                    'end_y': int(height * (1 - percentage))
                },
                'down': {
                    'start_x': int(width * 0.5),
                    'start_y': int(height * 0.3),
                    'end_x': int(width * 0.5),
                    'end_y': int(height * percentage)
                }
            }
            
            if direction.lower() not in swipe_coords:
                raise ValueError(f"Invalid direction: {direction}. Use 'left', 'right', 'up', or 'down'")
                
            coords = swipe_coords[direction.lower()]
            
            # Perform swipe
            action = self.driver.action()
            if duration:
                action.press(x=coords['start_x'], y=coords['start_y']) \
                    .wait(duration) \
                    .move_to(x=coords['end_x'], y=coords['end_y']) \
                    .release() \
                    .perform()
            else:
                action.press(x=coords['start_x'], y=coords['start_y']) \
                    .move_to(x=coords['end_x'], y=coords['end_y']) \
                    .release() \
                    .perform()
                
            text_print(f"Swiped {direction}", 'green')
            
        except Exception as e:
            raise Exception(f"Error performing directional swipe: {str(e)}")

        # Swipe by direction
        # element.swipe_by_direction('left')
        # element.swipe_by_direction('right', duration=300)
        # element.swipe_by_direction('up', percentage=0.5)  # swipe 50% of screen
        # element.swipe_by_direction('down', duration=500, percentage=0.8)

    def swipe_by_coordinates(self, start_x, start_y, end_x, end_y, duration=None):
        """
        Swipes from one coordinate to another.
        
        Args:
            start_x (int): Starting x coordinate
            start_y (int): Starting y coordinate
            end_x (int): Ending x coordinate
            end_y (int): Ending y coordinate
            duration (int, optional): Time in milliseconds for the swipe action
        """
        try:
            # Validate coordinates
            window_size = self.driver.get_window_size()
            max_x, max_y = window_size['width'], window_size['height']
            
            for coord, value, max_val, name in [
                ('start_x', start_x, max_x, 'width'),
                ('end_x', end_x, max_x, 'width'),
                ('start_y', start_y, max_y, 'height'),
                ('end_y', end_y, max_y, 'height')
            ]:
                if not 0 <= value <= max_val:
                    raise ValueError(
                        f"Invalid {coord}: {value}. Must be between 0 and {name} ({max_val})"
                    )
            
            # Perform swipe
            action = self.driver.action()
            if duration:
                action.press(x=start_x, y=start_y) \
                    .wait(duration) \
                    .move_to(x=end_x, y=end_y) \
                    .release() \
                    .perform()
            else:
                action.press(x=start_x, y=start_y) \
                    .move_to(x=end_x, y=end_y) \
                    .release() \
                    .perform()
                
            text_print(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})", 'green')
            
        except Exception as e:
            raise Exception(f"Error performing coordinate swipe: {str(e)}")
        
        # Swipe by coordinates
        # element.swipe_by_coordinates(500, 1000, 100, 1000)  # horizontal swipe
        # element.swipe_by_coordinates(250, 800, 250, 200)    # vertical swipe
        # element.swipe_by_coordinates(100, 100, 300, 500, duration=400)  # diagonal swipe

    def get_text(self, locator_name, timeout=10):
        """
        Gets text from the specified element.

        Args:
            locator_name (str): Name of the locator in the JSON file
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            str: Text content of the element
        """
        try:
            locator = self.get_locator(locator_name)
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
            element_text = element.text
            text_print(f"Text from {locator_name}: {element_text}", 'green')
            
            return element_text
            
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error getting text from '{locator_name}': {str(e)}")

    def get_attribute(self, locator_name, attribute_name, timeout=10):
        """
        Gets attribute value from the specified element.

        Args:
            locator_name (str): Name of the locator in the JSON file
            attribute_name (str): Name of the attribute to retrieve (e.g., 'value', 'class', 'id')
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            str: Attribute value of the element
        """
        try:
            locator = self.get_locator(locator_name)
            locator_type = locator.get("locator_type").lower()
            locator_value = locator.get("locator")
            
            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            
            # Wait for element to be present
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, locator_value))
            )
            
            # Get attribute value from element
            attribute_value = element.get_attribute(attribute_name)
            text_print(f"Attribute '{attribute_name}' from {locator_name}: {attribute_value}", 'green')
            
            return attribute_value
            
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error getting attribute '{attribute_name}' from '{locator_name}': {str(e)}")

    def take_element_screenshot(self, locator_name, filename=None, timeout=10):
        """
        Takes a screenshot of the specified element.

        Args:
            locator_name (str): Name of the locator in the JSON file
            filename (str, optional): Name for the screenshot file (default: element_name_timestamp.png)
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            str: Path to the saved screenshot file
        """
        try:
            from pathlib import Path
            
            # Create baseline_img directory if it doesn't exist
            baseline_dir = Path("baseline_img")
            baseline_dir.mkdir(exist_ok=True)
            
            locator = self.get_locator(locator_name)
            locator_type = locator.get("locator_type").lower()
            locator_value = locator.get("locator")
            
            by_type = locator_map.get(locator_type)
            if not by_type:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            
            # Wait for element to be present
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, locator_value))
            )
            
            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{locator_name}_{timestamp}.png"
            elif not filename.endswith('.png'):
                filename += '.png'
            
            # Create full path for the screenshot
            screenshot_path = baseline_dir / filename
            
            # Take screenshot
            element.screenshot(str(screenshot_path))
            text_print(f"Screenshot saved for {locator_name}: {screenshot_path}", 'green')
            
            return str(screenshot_path)
            
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not present after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error taking screenshot of '{locator_name}': {str(e)}")

    def compare_element_screenshots(self, locator_name, baseline_image, threshold=0.95, timeout=10):
        """
        Compares a current element screenshot with a baseline image from baseline_img folder.

        Args:
            locator_name (str): Name of the locator in the JSON file
            baseline_image (str): Name of the baseline image file in baseline_img folder
            threshold (float): Similarity threshold (0.0 to 1.0, default 0.95)
            timeout (int): Maximum time to wait for element presence (default 10 seconds)

        Returns:
            bool: True if images match within threshold, False otherwise
        """
        try:
            from PIL import Image
            import cv2
            import numpy as np
            from pathlib import Path

            # Create and get baseline directory path
            baseline_dir = Path("baseline_img")
            baseline_dir.mkdir(exist_ok=True)
            
            # Construct full path for baseline image
            if not baseline_image.endswith('.png'):
                baseline_image += '.png'
            baseline_path = baseline_dir / baseline_image

            # Take current screenshot
            current_screenshot = self.take_element_screenshot(locator_name, timeout=timeout)
            
            # Load images
            current_img = cv2.imread(current_screenshot)
            baseline_img = cv2.imread(str(baseline_path))
            
            # Verify baseline image exists
            if not baseline_path.exists():
                raise FileNotFoundError(f"Baseline image not found: {baseline_path}")
            
            # Resize images to same size for comparison
            baseline_img = cv2.resize(baseline_img, (current_img.shape[1], current_img.shape[0]))
            
            # Calculate similarity score
            similarity = cv2.matchTemplate(current_img, baseline_img, cv2.TM_CCOEFF_NORMED)[0][0]
            
            # Compare with threshold
            matches = similarity >= threshold
            
            if matches:
                text_print(f"Screenshots match for {locator_name} (similarity: {similarity:.2%})", 'green')
            else:
                text_print(f"Screenshots do not match for {locator_name} (similarity: {similarity:.2%})", 'red')
            
            # Clean up temporary screenshot
            Path(current_screenshot).unlink()
            
            return matches
            
        except Exception as e:
            raise Exception(f"Error comparing screenshots for '{locator_name}': {str(e)}")

    def take_full_screenshot(self, filename=None):
        """
        Takes a screenshot of the entire screen.

        Args:
            filename (str, optional): Name for the screenshot file (default: fullscreen_timestamp.png)

        Returns:
            str: Path to the saved screenshot file
        """
        try:
            from pathlib import Path
            
            # Create baseline_img directory if it doesn't exist
            baseline_dir = Path("baseline_img")
            baseline_dir.mkdir(exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"fullscreen_{timestamp}.png"
            elif not filename.endswith('.png'):
                filename += '.png'
            
            # Create full path for the screenshot
            screenshot_path = baseline_dir / filename
            
            # Take screenshot
            self.driver.save_screenshot(str(screenshot_path))
            text_print(f"Full screenshot saved: {screenshot_path}", 'green')
            
            return str(screenshot_path)
            
        except Exception as e:
            raise Exception(f"Error taking full screenshot: {str(e)}")

    def compare_full_screenshots(self, baseline_image, threshold=0.95):
        """
        Compares a current full screen screenshot with a baseline image from baseline_img folder.

        Args:
            baseline_image (str): Name of the baseline image file in baseline_img folder
            threshold (float): Similarity threshold (0.0 to 1.0, default 0.95)

        Returns:
            bool: True if images match within threshold, False otherwise
        """
        try:
            from PIL import Image
            import cv2
            import numpy as np
            from pathlib import Path

            # Create and get baseline directory path
            baseline_dir = Path("baseline_img")
            baseline_dir.mkdir(exist_ok=True)
            
            # Construct full path for baseline image
            if not baseline_image.endswith('.png'):
                baseline_image += '.png'
            baseline_path = baseline_dir / baseline_image

            # Take current screenshot
            current_screenshot = self.take_full_screenshot()
            
            # Load images
            current_img = cv2.imread(current_screenshot)
            baseline_img = cv2.imread(str(baseline_path))
            
            # Verify baseline image exists
            if not baseline_path.exists():
                raise FileNotFoundError(f"Baseline image not found: {baseline_path}")
            
            # Rest of the comparison logic remains the same
            baseline_img = cv2.resize(baseline_img, (current_img.shape[1], current_img.shape[0]))
            similarity = cv2.matchTemplate(current_img, baseline_img, cv2.TM_CCOEFF_NORMED)[0][0]
            matches = similarity >= threshold
            
            if matches:
                text_print(f"Full screenshots match (similarity: {similarity:.2%})", 'green')
            else:
                text_print(f"Full screenshots do not match (similarity: {similarity:.2%})", 'red')
            
            # Clean up temporary screenshot
            Path(current_screenshot).unlink()
            
            return matches
            
        except Exception as e:
            raise Exception(f"Error comparing full screenshots: {str(e)}")

    def start_screen_recording(self, quality='low'):
        """
        Starts screen recording on the mobile device.
        
        Args:
            quality (str): Recording quality - 'low', 'medium', or 'high'
                - low: 360p (640x360)
                - medium: 720p (1280x720)
                - high: 1080p (1920x1080)
        """
        try:
            from pathlib import Path
            
            # Create recordings directory if it doesn't exist
            recordings_dir = Path("recordings")
            recordings_dir.mkdir(exist_ok=True)
            
            # Quality settings mapping
            quality_settings = {
                'low': {
                    'videoSize': '640x360',
                    'bitRate': 1000000,  # 1 Mbps
                    'videoFps': 15
                },
                'medium': {
                    'videoSize': '1280x720',
                    'bitRate': 2000000,  # 2 Mbps
                    'videoFps': 24
                },
                'high': {
                    'videoSize': '1920x1080',
                    'bitRate': 4000000,  # 4 Mbps
                    'videoFps': 30
                }
            }
            
            # Get quality settings or default to medium
            settings = quality_settings.get(quality.lower(), quality_settings['medium'])
            
            # Configure recording options
            recording_options = {
                'forceRestart': True,
                **settings
            }
            
            self.driver.start_recording_screen(**recording_options)
            text_print(f"Screen recording started with {quality}", 'green')
            
        except Exception as e:
            raise Exception(f"Error starting screen recording: {str(e)}")

    def stop_screen_recording(self, filename=None):
        """
        Stops the screen recording and saves it.

        Args:
            filename (str, optional): Name for the recording file (default: recording_timestamp.mp4)

        Returns:
            str: Path to the saved recording file
        """
        try:
            import base64
            import os
            from pathlib import Path
            
            # Create recordings directory if it doesn't exist
            recordings_dir = Path("recordings")
            recordings_dir.mkdir(exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.mp4"
            elif not filename.endswith('.mp4'):
                filename += '.mp4'
            
            # Create full path for the recording
            recording_path = recordings_dir / filename
            
            # Stop recording and get base64 data
            base64_data = self.driver.stop_recording_screen()
            
            # Decode and save the recording
            with open(recording_path, "wb") as f:
                f.write(base64.b64decode(base64_data))
            
            text_print(f"Screen recording saved: {recording_path}", 'green')
            return str(recording_path)
            
        except Exception as e:
            raise Exception(f"Error stopping screen recording: {str(e)}")

    def get_device_logs(self, filename=None):
        """
        Gets device logs and saves them to a file.

        Args:
            filename (str, optional): Name for the log file (default: device_log_timestamp.txt)
        
        Returns:
            str: Path to the saved log file
        """
        try:
            from datetime import datetime
            from pathlib import Path
            
            # Create logs directory if it doesn't exist
            logs_dir = Path("device_logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"device_log_{timestamp}.txt"
            elif not filename.endswith('.txt'):
                filename += '.txt'
            
            # Create full path for the log file
            log_path = logs_dir / filename
            
            # Get device logs
            logs = self.driver.get_log('logcat')
            
            # Write logs to file
            with open(log_path, 'w', encoding='utf-8') as f:
                for log in logs:
                    f.write(f"{log['timestamp']} {log['level']} {log['message']}\n")
            
            text_print(f"Device logs saved: {log_path}", 'green')
            return str(log_path)
            
        except Exception as e:
            raise Exception(f"Error getting device logs: {str(e)}")

    def pinch_to_zoom(self, locator_name, scale_factor=2.0, duration=None, timeout=10):
        """
        Performs a pinch gesture to zoom in or out on an element.
        
        Args:
            locator_name (str): Name of the locator in the JSON file
            scale_factor (float): Scale factor for zoom (>1.0 for zoom in, <1.0 for zoom out, default 2.0)
            duration (int, optional): Time in milliseconds for the pinch action
            timeout (int): Maximum time to wait for element presence (default 10 seconds)
        """
        try:
            # Get element locator and wait for presence
            locator = self.get_locator(locator_name)
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    locator_map[locator.get("locator_type").lower()],
                    locator.get("locator")
                ))
            )
            
            # Get element location and size
            location = element.location
            size = element.size
            center_x = location['x'] + size['width'] / 2
            center_y = location['y'] + size['height'] / 2
            
            # Calculate pinch coordinates
            offset = min(size['width'], size['height']) / 4
            if scale_factor > 1.0:  # Zoom in
                start_offset = offset / 2
                end_offset = offset * scale_factor
            else:  # Zoom out
                start_offset = offset * (1/scale_factor)
                end_offset = offset / 2
            
            # Create touch actions for two fingers
            finger1 = PointerInput(interaction.POINTER_TOUCH, "finger1")
            finger2 = PointerInput(interaction.POINTER_TOUCH, "finger2")
            
            # Create action chains
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=finger1, keyboard=finger2)
            
            # Define pinch gesture
            if duration:
                duration_sec = duration / 1000  # Convert to seconds
            else:
                duration_sec = 0.5  # Default duration
            
            # Finger 1 movement (top-left to bottom-right)
            actions.w3c_actions.pointer_action.move_to_location(
                center_x - start_offset, center_y - start_offset
            )
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration_sec)
            actions.w3c_actions.pointer_action.move_to_location(
                center_x - end_offset, center_y - end_offset
            )
            actions.w3c_actions.pointer_action.release()
            
            # Finger 2 movement (bottom-right to top-left)
            actions.w3c_actions.key_action.move_to_location(
                center_x + start_offset, center_y + start_offset
            )
            actions.w3c_actions.key_action.pointer_down()
            actions.w3c_actions.key_action.pause(duration_sec)
            actions.w3c_actions.key_action.move_to_location(
                center_x + end_offset, center_y + end_offset
            )
            actions.w3c_actions.key_action.release()
            
            # Perform the pinch gesture
            actions.perform()
            
            zoom_type = "in" if scale_factor > 1.0 else "out"
            text_print(f"Pinched to zoom {zoom_type} on {locator_name} with scale factor {scale_factor}", 'green')
            
        except TimeoutException:
            raise TimeoutException(f"Element '{locator_name}' not found after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error performing pinch to zoom on '{locator_name}': {str(e)}")

        # Usage examples:
        # element.pinch_to_zoom('image_element')  # Default zoom in (scale_factor=2.0)
        # element.pinch_to_zoom('image_element', scale_factor=0.5)  # Zoom out
        # element.pinch_to_zoom('image_element', scale_factor=3.0, duration=1000)  # Slow zoom in



