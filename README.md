
# HexEngine - Mobile Automation Solution

A comprehensive mobile automation framework built with Python, supporting cross-platform testing for Android and iOS applications. This framework provides a robust foundation for mobile test automation with support for local devices, cloud testing platforms, and comprehensive reporting.

## Features

- **Cross-Platform Support**: Test Android and iOS applications
- **Multiple Testing Environments**: Local devices, LambdaTest, BrowserStack
- **Comprehensive Element Interactions**: Tap, swipe, text input, and verification
- **Advanced Waiting Mechanisms**: Smart waits for element visibility and presence
- **Detailed Reporting**: Allure reports with screenshots and logs
- **Flexible Configuration**: JSON-based configuration for different environments
- **AI Integration**: OCR and smart element detection capabilities

## Tech Stack

### Core Technologies

- **Python**: Primary scripting language for automation logic and test implementation
- **Appium**: Mobile automation framework enabling cross-platform app testing
- **pytest**: Advanced testing framework with powerful fixtures and reporting capabilities

### Reporting & Analysis

- **Allure Report**: Comprehensive test reporting with detailed execution insights
- **Logging**: Structured logging for execution tracking and debugging
- **Screenshots**: Automatic capture on failures and key test steps

### DevOps Integration

- **CI/CD**: Jenkins and GitHub Actions integration for automated testing pipelines
- **Cloud Testing**: LambdaTest and BrowserStack support for scalable testing
- **Version Control**: Git-based workflow with automated test execution

## Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-mobile
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure test environment**
   - Update `config/TestConfig.json` with your device/platform settings
   - Place your app files in the `app/` directory

4. **Run tests**
   ```bash
   python run_tests.py
   ```

### Package Management

**Export current packages:**
```bash
pip freeze > requirements.txt
```

**Install from requirements:**
```bash
pip install -r requirements.txt
```

## Locator Usage

### Content Description Locators

For accessibility-based element identification:

![img.png](img.png)

**JSON Configuration:**
```json
{
  "continue_text_button": {
    "locator_type": "content",
    "locator": "CONTINUE"
  }
}
```

### Available Methods

**Element Interactions:**
- `tap_on_element` - Single tap on element
- `double_tap_on_element` - Double tap gesture
- `enter_text` - Text input into fields
- `long_press_element` - Long press gesture
- `multi_tap` - Multiple tap sequences

**Gestures & Navigation:**
- `swipe_element_to_element` - Swipe between elements
- `swipe_by_direction` - Directional swiping
- `swipe_by_coordinates` - Coordinate-based swiping

**Verification & Waiting:**
- `element_visible` - Check element visibility
- `element_not_visible` - Verify element invisibility
- `element_present` - Check DOM presence

**Utilities:**
- `text_print` - Colored console output

### Resources

- **Emoji Reference**: [Emoji Cheat Sheet](https://www.webfx.com/tools/emoji-cheat-sheet)
- **Appium Documentation**: [Official Appium Docs](https://appium.io/docs/)
- **pytest Guide**: [pytest Documentation](https://docs.pytest.org/)

## Device Class Documentation

The `Device` class provides essential device management functionality for mobile testing automation.

### Device(driver)
**Description:** Initialize Device class with Appium driver
**Parameters:**
- `driver`: Appium WebDriver instance (required)
**Raises:**
- `ValueError`: If driver is None
**Example:**
```python
from framework.mobile.device import Device
device = Device(driver)
```

### get_device_battery_level()
**Description:** Gets the current battery level of the device
**Parameters:** None
**Returns:** int - Battery level percentage (0-100)
**Raises:**
- `Exception`: If unable to retrieve battery information
**Example:**
```python
# Get current battery level
battery_level = device.get_device_battery_level()
print(f"Current battery: {battery_level}%")

# Use in test conditions
if battery_level < 20:
    print("Warning: Low battery detected")
```

### rotate_device(orientation)
**Description:** Rotates the device to the specified orientation
**Parameters:**
- `orientation` (str): Desired orientation ('PORTRAIT', 'LANDSCAPE', 'PORTRAIT_REVERSE', 'LANDSCAPE_REVERSE')
**Raises:**
- `ValueError`: If orientation is invalid
- `Exception`: If rotation fails
**Example:**
```python
# Rotate to landscape for video playback
device.rotate_device('LANDSCAPE')

# Test app behavior in different orientations
device.rotate_device('PORTRAIT')
device.rotate_device('LANDSCAPE_REVERSE')
```

### lock_device(duration=None)
**Description:** Locks the device for a specified duration or indefinitely
**Parameters:**
- `duration` (int, optional): Duration in seconds to keep device locked. If None, device stays locked until unlock_device is called
**Raises:**
- `Exception`: If locking fails
**Example:**
```python
# Lock device indefinitely
device.lock_device()

# Lock device for 5 seconds (auto-unlock)
device.lock_device(duration=5)

# Test app behavior when returning from locked state
device.lock_device(duration=3)
# App should handle the lock/unlock cycle gracefully
```

### unlock_device(password=None)
**Description:** Unlocks the device with optional password/PIN entry
**Parameters:**
- `password` (str, optional): Password/PIN to unlock the device (numeric only)
**Raises:**
- `Exception`: If unlocking fails
**Example:**
```python
# Unlock device without password
device.unlock_device()

# Unlock device with PIN
device.unlock_device(password="1234")

# Test secure unlock flow
device.lock_device()
device.unlock_device(password="0000")
```

## Element Class Documentation

The `Element` class provides comprehensive element interaction functionality for mobile testing automation.

### Element(driver, file_path)
**Description:** Initializes the Element class with a WebDriver instance and locators file path for element interactions.
**Parameters:**
- `driver`: WebDriver instance (required)
- `file_path` (str): Path to JSON file containing element locators (required)
**Raises:**
- `ValueError`: If driver or file_path is None
**Examples:**
```python
element = Element(driver, "locators/login_page.json")
```

### tap_on_element(locator_name, timeout=10)
**Description:** Clicks on the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not clickable after timeout
- `ValueError`: If unsupported locator type
**Examples:**
```python
element.tap_on_element("login_button")
element.tap_on_element("submit_btn", timeout=15)
```

### multi_tap(locator_name, tap_count=1, timeout=10)
**Description:** Clicks on an element multiple times.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `tap_count` (int): Number of times to click (default: 1)
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not clickable after timeout
**Examples:**
```python
element.multi_tap("increment_button", tap_count=5)
element.multi_tap("like_button", tap_count=2, timeout=15)
```

### long_press_element(locator_name, duration=1000, timeout=10)
**Description:** Performs a long press on the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `duration` (int): Duration to hold press in milliseconds (default: 1000ms)
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not clickable after timeout
**Examples:**
```python
element.long_press_element("context_menu_item")
element.long_press_element("image", duration=2000)
```

### enter_text(locator_name, text_to_enter, timeout=10)
**Description:** Enters text into the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `text_to_enter` (str): Text to enter into the element
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
element.enter_text("username_field", "john.doe@example.com")
element.enter_text("password_field", "mypassword123")
```

### clear_and_enter_text(locator_name, text_to_enter, timeout=10)
**Description:** Clears existing text and enters new text into the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `text_to_enter` (str): Text to enter into the element
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
element.clear_and_enter_text("search_field", "new search term")
```

### clear_text(locator_name, timeout=10)
**Description:** Clears existing text from the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
element.clear_text("input_field")
```

### enter_text_from_file(locator_name, file_name, cell_reference, sheet_name=None)
**Description:** Reads a value from a file (CSV or Excel) and enters it into the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `file_name` (str): Name of the file to read data from (.csv or .xlsx)
- `cell_reference` (str): Cell reference (e.g., 'A1' for Excel, column name for CSV)
- `sheet_name` (str, optional): Sheet name (required for Excel files)
**Raises:**
- `ValueError`: If value is empty or file type unsupported
**Examples:**
```python
element.enter_text_from_file("username_field", "test_data.xlsx", "A1", "Sheet1")
element.enter_text_from_file("email_field", "users.csv", "email")
```

### swipe_element_to_element(start_locator_name, end_locator_name, duration=500, timeout=10)
**Description:** Swipes from one element to another.
**Parameters:**
- `start_locator_name` (str): Locator name for start element
- `end_locator_name` (str): Locator name for end element
- `duration` (int): Duration in milliseconds (default: 500ms)
- `timeout` (int): Wait timeout for elements (default: 10 seconds)
**Raises:**
- `Exception`: If swipe operation fails
**Examples:**
```python
element.swipe_element_to_element("item1", "item5")
element.swipe_element_to_element("start_point", "end_point", duration=1000)
```

### swipe_by_direction(direction, duration=None, percentage=0.75)
**Description:** Swipes in the specified direction based on screen size.
**Parameters:**
- `direction` (str): Direction to swipe ('left', 'right', 'up', 'down')
- `duration` (int, optional): Time in milliseconds for swipe action
- `percentage` (float): Percentage of screen to swipe (0.0 to 1.0, default: 0.75)
**Raises:**
- `ValueError`: If direction is invalid
**Examples:**
```python
element.swipe_by_direction('left')
element.swipe_by_direction('up', duration=300, percentage=0.5)
```

### swipe_by_coordinates(start_x, start_y, end_x, end_y, duration=500)
**Description:** Swipes from one coordinate to another.
**Parameters:**
- `start_x` (int): Starting x coordinate
- `start_y` (int): Starting y coordinate
- `end_x` (int): Ending x coordinate
- `end_y` (int): Ending y coordinate
- `duration` (int): Duration in milliseconds (default: 500ms)
**Raises:**
- `Exception`: If swipe operation fails
**Examples:**
```python
element.swipe_by_coordinates(100, 200, 300, 400)
element.swipe_by_coordinates(0, 500, 400, 500, duration=1000)
```

### get_text(locator_name, timeout=10)
**Description:** Gets text from the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
text = element.get_text("status_label")
print(f"Status: {text}")
```

### get_attribute(locator_name, attribute_name, timeout=10)
**Description:** Gets attribute value from the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `attribute_name` (str): Name of the attribute to retrieve
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
value = element.get_attribute("input_field", "value")
class_name = element.get_attribute("button", "class")
```

### take_element_screenshot(locator_name, filename=None, timeout=10)
**Description:** Takes a screenshot of the specified element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `filename` (str, optional): Name for screenshot file
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
path = element.take_element_screenshot("error_message")
path = element.take_element_screenshot("chart", "chart_screenshot.png")
```

### compare_element_screenshots(locator_name, baseline_image, threshold=0.95, timeout=10)
**Description:** Compares current element screenshot with baseline image.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `baseline_image` (str): Name of baseline image file in baseline_img folder
- `threshold` (float): Similarity threshold (0.0 to 1.0, default: 0.95)
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `FileNotFoundError`: If baseline image not found
**Examples:**
```python
matches = element.compare_element_screenshots("logo", "baseline_logo.png")
matches = element.compare_element_screenshots("chart", "expected_chart", threshold=0.90)
```

### take_full_screenshot(filename=None)
**Description:** Takes a screenshot of the entire screen.
**Parameters:**
- `filename` (str, optional): Name for screenshot file
**Raises:**
- `Exception`: If screenshot operation fails
**Examples:**
```python
path = element.take_full_screenshot()
path = element.take_full_screenshot("full_page_screenshot.png")
```

### compare_full_screenshots(baseline_image, threshold=0.95)
**Description:** Compares current full screen screenshot with baseline image.
**Parameters:**
- `baseline_image` (str): Name of baseline image file in baseline_img folder
- `threshold` (float): Similarity threshold (0.0 to 1.0, default: 0.95)
**Raises:**
- `FileNotFoundError`: If baseline image not found
**Examples:**
```python
matches = element.compare_full_screenshots("baseline_page.png")
matches = element.compare_full_screenshots("expected_screen", threshold=0.90)
```

### start_screen_recording(quality='low')
**Description:** Starts screen recording on the mobile device.
**Parameters:**
- `quality` (str): Recording quality - 'low', 'medium', or 'high' (default: 'low')
**Raises:**
- `Exception`: If recording start fails
**Examples:**
```python
element.start_screen_recording()
element.start_screen_recording(quality='high')
```

### stop_screen_recording(filename=None)
**Description:** Stops screen recording and saves it.
**Parameters:**
- `filename` (str, optional): Name for recording file
**Raises:**
- `Exception`: If recording stop fails
**Examples:**
```python
path = element.stop_screen_recording()
path = element.stop_screen_recording("test_recording.mp4")
```

### get_device_logs(filename=None)
**Description:** Gets device logs and saves them to a file.
**Parameters:**
- `filename` (str, optional): Name for log file
**Raises:**
- `Exception`: If log retrieval fails
**Examples:**
```python
path = element.get_device_logs()
path = element.get_device_logs("test_logs.txt")
```

### pinch_to_zoom(locator_name, scale_factor=2.0, duration=None, timeout=10)
**Description:** Performs a pinch gesture to zoom in or out on an element.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `scale_factor` (float): Scale factor for zoom (>1.0 zoom in, <1.0 zoom out, default: 2.0)
- `duration` (int, optional): Time in milliseconds for pinch action
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
**Raises:**
- `TimeoutException`: If element not found after timeout
**Examples:**
```python
element.pinch_to_zoom('image_element')  # Zoom in
element.pinch_to_zoom('map', scale_factor=0.5)  # Zoom out
element.pinch_to_zoom('photo', scale_factor=3.0, duration=1000)
```

### scroll_page(direction="down", amount=300)
**Description:** Scrolls the page in the given direction.
**Parameters:**
- `direction` (str): 'up' or 'down' (default: 'down')
- `amount` (int): Amount to scroll in pixels (default: 300)
**Raises:**
- `ValueError`: If direction is invalid
**Examples:**
```python
element.scroll_page()
element.scroll_page(direction="up", amount=500)
```

### scroll_until_visible(locator_name, direction="down", max_attempts=20, timeout=5)
**Description:** Scrolls until the element becomes visible.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `direction` (str): Scroll direction (default: 'down')
- `max_attempts` (int): Maximum scroll attempts (default: 20)
- `timeout` (int): Wait time after each scroll (default: 5 seconds)
**Raises:**
- `TimeoutException`: If element not visible after max attempts
**Examples:**
```python
element.scroll_until_visible("footer_link")
element.scroll_until_visible("item", direction="up", max_attempts=10)
```

### hide_keyboard()
**Description:** Hides the on-screen keyboard if open.
**Parameters:** None
**Raises:** None (logs error if fails)
**Examples:**
```python
element.hide_keyboard()
```

### show_keyboard()
**Description:** Attempts to show the on-screen keyboard (Android only).
**Parameters:** None
**Raises:** None (logs error if fails)
**Examples:**
```python
element.show_keyboard()
```

### press_number_keys(numbers)
**Description:** Presses number keys on the device.
**Parameters:**
- `numbers`: String of numbers (e.g., "123") or list of integers
**Raises:**
- `ValueError`: If invalid number provided
**Examples:**
```python
element.press_number_keys("123")
element.press_number_keys([1, 2, 3, 4])
```

### open_url_in_chrome(url, wait_time=10)
**Description:** Launches Chrome and navigates to specified URL.
**Parameters:**
- `url` (str): URL to open
- `wait_time` (int): Seconds to wait for Chrome address bar (default: 10)
**Raises:**
- `Exception`: If Chrome launch or navigation fails
**Examples:**
```python
element.open_url_in_chrome("https://www.example.com")
element.open_url_in_chrome("https://google.com", wait_time=15)
```

### scroll_by_coordinates(start_x, start_y, end_x, end_y, duration=500)
**Description:** Scrolls from one coordinate to another.
**Parameters:**
- `start_x` (int): Starting x coordinate
- `start_y` (int): Starting y coordinate
- `end_x` (int): Ending x coordinate
- `end_y` (int): Ending y coordinate
- `duration` (int): Duration in milliseconds (default: 500ms)
**Raises:**
- `Exception`: If scroll operation fails
**Examples:**
```python
element.scroll_by_coordinates(100, 200, 100, 600)
element.scroll_by_coordinates(200, 300, 200, 100, duration=1000)
```

### tap_and_get_clipboard_text(locator_name, timeout=10, pause_after_click=1)
**Description:** Taps on element and retrieves clipboard text.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element (default: 10 seconds)
- `pause_after_click` (int): Seconds to wait after click (default: 1)
**Raises:**
- `TimeoutException`: If element not clickable after timeout
**Examples:**
```python
clipboard_text = element.tap_and_get_clipboard_text("copy_button")
text = element.tap_and_get_clipboard_text("share_link", pause_after_click=2)
```

## Prints Module Documentation

The `prints` module provides colored text output functionality for enhanced console logging in mobile testing automation.

### text_print(text, color="CYAN")
**Description:** Prints text in the specified color using colorama for cross-platform colored terminal output.
**Parameters:**
- `text` (str): The message to print (required)
- `color` (str): The color name for text output (default: "CYAN")
**Available Colors:**
- "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "BLACK"
**Returns:** None
**Examples:**
```python
from framework.mobile.prints import text_print

# Print success message in green
text_print("Test passed successfully", "GREEN")

# Print error message in red
text_print("Test failed with error", "RED")

# Print info message with default cyan color
text_print("Starting test execution")

# Print warning in yellow
text_print("Warning: Low battery detected", "YELLOW")
```

## Verify Class Documentation

The `Verify` class provides element verification functionality for mobile testing automation, allowing you to validate element states and properties.

### Verify(driver, file_path)
**Description:** Initializes the Verify class with a WebDriver instance and locators file path for element verification operations.
**Parameters:**
- `driver`: WebDriver instance (required)
- `file_path` (str): Path to JSON file containing element locators (required)
**Raises:**
- `FileNotFoundError`: If locator file not found
- `ValueError`: If JSON format is invalid
**Examples:**
```python
from framework.mobile.verify import Verify
verify = Verify(driver, "locators/login_page.json")
```

### element_visible(locator_name, timeout=10)
**Description:** Verifies if an element is visible on the screen.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element visibility (default: 10 seconds)
**Returns:** bool - True if element is visible
**Raises:**
- `ValueError`: If locator is invalid or missing
- `TimeoutException`: If element not visible after timeout
**Examples:**
```python
verify.element_visible("login_button")
verify.element_visible("error_message", timeout=15)
```

### element_not_visible(locator_name, timeout=10)
**Description:** Verifies if an element is not visible on the screen.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element invisibility (default: 10 seconds)
**Returns:** bool - True if element is not visible
**Raises:**
- `ValueError`: If locator is invalid or missing
- `TimeoutException`: If element still visible after timeout
**Examples:**
```python
verify.element_not_visible("loading_spinner")
verify.element_not_visible("popup_dialog", timeout=20)
```

### element_present(locator_name, timeout=10)
**Description:** Verifies if an element is present in the DOM (may not be visible).
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `timeout` (int): Maximum time to wait for element presence (default: 10 seconds)
**Returns:** bool - True if element is present
**Raises:**
- `ValueError`: If locator is invalid or missing
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
verify.element_present("hidden_field")
verify.element_present("dynamic_content", timeout=25)
```

### verify_element_text(locator_name, expected_text, contains=False, case_sensitive=True, timeout=10)
**Description:** Gets text from element and verifies it against expected text with various comparison options.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
- `expected_text` (str): Text to verify against
- `contains` (bool): If True, checks if element text contains expected text; if False, checks for exact match (default: False)
- `case_sensitive` (bool): If True, performs case-sensitive comparison (default: True)
- `timeout` (int): Maximum time to wait for element presence (default: 10 seconds)
**Returns:** bool - True if verification passes, False otherwise
**Raises:**
- `ValueError`: If locator is invalid or missing
- `TimeoutException`: If element not present after timeout
**Examples:**
```python
# Exact match verification
verify.verify_element_text("status_label", "Success")

# Contains verification
verify.verify_element_text("error_message", "failed", contains=True)

# Case-insensitive verification
verify.verify_element_text("title", "welcome", case_sensitive=False)

# Combined options
verify.verify_element_text("description", "test", contains=True, case_sensitive=False, timeout=15)
```

## Wait Class Documentation

The `Wait` class provides waiting functionality for mobile testing automation, allowing you to wait for elements and add delays in test execution.

### Wait(driver, file_path)
**Description:** Initializes the Wait class with a WebDriver instance and locators file path for waiting operations.
**Parameters:**
- `driver`: WebDriver instance (required)
- `file_path` (str): Path to JSON file containing element locators (required)
**Raises:**
- `FileNotFoundError`: If locator file not found
- `ValueError`: If JSON format is invalid
**Examples:**
```python
from framework.mobile.wait import Wait
wait = Wait(driver, "locators/login_page.json")
```

### wait_until_element_is_visible(locator_name)
**Description:** Waits until the specified element becomes visible on the screen with a 30-second timeout.
**Parameters:**
- `locator_name` (str): Name of the locator in the JSON file
**Returns:** None
**Raises:**
- `ValueError`: If locator is invalid, missing, or unsupported locator type
- `TimeoutException`: If element not visible after 30 seconds
**Supported Locator Types:** xpath, id, path, content, uiautomator, class
**Examples:**
```python
wait.wait_until_element_is_visible("login_button")
wait.wait_until_element_is_visible("dashboard_header")
```

### wait_for_seconds(seconds)
**Description:** Pauses the execution for the specified number of seconds and prints a confirmation message.
**Parameters:**
- `seconds` (int/float): The number of seconds to wait
**Returns:** None
**Examples:**
```python
# Wait for 3 seconds
wait.wait_for_seconds(3)

# Wait for 1.5 seconds
wait.wait_for_seconds(1.5)

# Wait for 10 seconds
wait.wait_for_seconds(10)
```

## Configuration Documentation

The `TestConfig.json` file contains the configuration settings for the mobile automation framework, supporting multiple platforms and testing environments.

### Configuration Structure

**File Location:** `config/TestConfig.json`

**Main Configuration Properties:**
- `run` (str): Specifies which platform configuration to use ("android", "iOS", "lambdaTest", "browserStack")
- `config` (object): Contains platform-specific configurations and global settings

### Platform Configurations

#### Android Configuration
```json
"android": {
  "platform": "android",
  "appPath/appPackage": "org-simple-clinic.apk",
  "platformVersion": "13",
  "deviceName": "0e191f93bb13",
  "automationName": "UiAutomator2",
  "capabilities": {
    "appWaitDuration": 30000,
    "newCommandTimeout": 60,
    "noReset": true,
    "autoGrantPermissions": true
  }
}
```

**Android Properties:**
- `platform`: Target platform ("android")
- `appPath/appPackage`: Path to APK file or package name
- `platformVersion`: Android OS version
- `deviceName`: Device identifier or name
- `automationName`: Automation engine ("UiAutomator2")
- `capabilities`: Additional Appium capabilities

#### iOS Configuration
```json
"iOS": {
  "platform": "iOS",
  "deviceName": "iPhone 15",
  "appPath/appPackage": "TestApp.app",
  "platformVersion": "18.4",
  "automationName": "XCUITest",
  "capabilities": {
    "appWaitDuration": 30000,
    "newCommandTimeout": 60,
    "noReset": true,
    "showXcodeLog": true
  }
}
```

**iOS Properties:**
- `platform`: Target platform ("iOS")
- `deviceName`: iOS device name or simulator
- `appPath/appPackage`: Path to .app bundle
- `platformVersion`: iOS version
- `automationName`: Automation engine ("XCUITest")
- `capabilities`: iOS-specific capabilities

#### LambdaTest Cloud Configuration
```json
"lambdaTest": {
  "platform": "Android",
  "deviceName": "Galaxy S21",
  "app": "lt://APP_ID",
  "platformVersion": "12.0",
  "automationName": "UiAutomator2",
  "isRealMobile": true,
  "capabilities": {
    "appWaitDuration": 30000,
    "newCommandTimeout": 60,
    "noReset": true,
    "network": true,
    "console": true
  }
}
```

**LambdaTest Properties:**
- `app`: LambdaTest app identifier ("lt://APP_ID")
- `isRealMobile`: Use real device instead of emulator
- `network`: Enable network logs
- `console`: Enable console logs

#### BrowserStack Configuration
```json
"browserStack": {
  "platform": "web",
  "browser": "chrome",
  "browserVersion": "latest"
}
```

**BrowserStack Properties:**
- `platform`: Platform type ("web")
- `browser`: Browser name
- `browserVersion`: Browser version

### Global Settings

- `report` (bool): Enable/disable test reporting (default: false)
- `hightlight_element` (bool): Enable/disable element highlighting during tests (default: false)

### Common Capabilities

**Standard Capabilities:**
- `appWaitDuration`: Maximum time to wait for app launch (milliseconds)
- `newCommandTimeout`: Timeout for new commands (seconds)
- `noReset`: Prevent app reset between sessions
- `autoGrantPermissions`: Automatically grant app permissions (Android)
- `showXcodeLog`: Display Xcode logs (iOS)

### Usage Examples

**Switching Platforms:**
```json
{
  "run": "android",  // Use Android configuration
  "config": { ... }
}
```

**Enabling Reports:**
```json
{
  "run": "iOS",
  "config": {
    "report": true,
    "hightlight_element": true
  }
}
```

## Android TV
```
    "androidTV": {
      "platform": "android",
      "appPath/appPackage": "com.google.android.apps.tv.launcherx",
      "platformVersion": "11",
      "deviceName": "Smart TV",
      "automationName": "UiAutomator2",
      "appActivity": "com.google.android.apps.tv.launcherx.home.HomeActivity",
      "capabilities": {
        "appWaitDuration": 30000,
        "newCommandTimeout": 60,
        "noReset": true,
        "autoGrantPermissions": true,
        "dontStopAppOnReset": true
      }
    }
```

