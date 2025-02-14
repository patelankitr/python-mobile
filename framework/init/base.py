import os
from pathlib import Path
from alttester import AltDriver
from appium import webdriver
from appium.options.common import AppiumOptions
from framework.readers.jsonFileReader import ConfigReader  # Importing ConfigReader


# Load configuration
config_reader = ConfigReader("D:\\Projects\\python-mo-framework\\config\\TestConfig.json")
config = config_reader.get_config()

# Extract required values from JSON
platform = config.get("platform")
app = config.get("app")
platform_version = config.get("platformVersion")
deviceName = config.get("deviceName")

# Extract optional Appium capabilities (if present)
optional_capabilities = config.get("capabilities", {})

print(f"Platform: {platform}")
print(f"App: {app}")
print(f"Platform Version: {platform_version}")
print(f"Additional Capabilities: {optional_capabilities}")
print(f"Device Name: {deviceName}")


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def root_path():
    """Finds and returns the APK file path dynamically."""
    root = get_project_root()
    apk_directory = root.parent / "app"
    apk_file_path = apk_directory / app
    if not apk_file_path.exists():
        raise FileNotFoundError(f"APK file not found: {apk_file_path}")
    apk_file_path = apk_file_path.resolve()  # Convert to absolute path
    print(f"APK file found: {apk_file_path}")
    return str(apk_file_path)  # Return as string


# Base Appium Capabilities (always required)
base_capabilities = {
    'platformName': platform,
    'deviceName': deviceName,
    'platformVersion': platform_version,
    'app': root_path()
}
# Merge with optional capabilities from JSON
final_capabilities = {**base_capabilities, **optional_capabilities}

# Parameterized function to initialize Appium driver
def init_appium_driver():
    appium_driver = webdriver.Remote("http://127.0.0.1:4723", options=AppiumOptions().load_capabilities(final_capabilities))
    return appium_driver

# Function to initialize AltTester driver
def init_alt_tester_driver(host="127.0.0.1", port=13000, app_name="__default__"):
    alt_tester_driver = AltDriver(host=host, port=port, app_name=app_name)
    return alt_tester_driver

# Debugging output
print("Final Appium Capabilities:", final_capabilities)
