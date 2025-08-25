import os
from pathlib import Path
from alttester import AltDriver
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.appium_service import AppiumService
from framework.readers.jsonReader import ConfigReader
from colorama import Fore, Back, Style
from framework.mobile.prints import text_print
import emoji
from appium.webdriver.common.appiumby import AppiumBy

# Define locator_map at module level
locator_map = {
    'xpath': AppiumBy.XPATH,
    'id': AppiumBy.ID,
    'path': AppiumBy.XPATH,
    'content': AppiumBy.ACCESSIBILITY_ID,
    'uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
    'class': AppiumBy.CLASS_NAME
}

class DriverFactory:
    def __init__(self):
        # Initialize services and drivers as None
        self.appium_service = None
        self.driver = None
        
        # Load configuration
        project_root = Path(__file__).resolve().parent.parent.parent
        config_path = project_root / "config" / "TestConfig.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {config_path}")
        # Initialize config reader with dynamic path
        self.config_reader = ConfigReader(str(config_path))
        self.run_type = self.config_reader.get_run_platform()
        self.platform_config = self.config_reader.get_platform_config()
        
        # Extract common values
        self.platform = self.platform_config.get("platform")
        self.app = self.platform_config.get("appPath/appPackage")
        self.platform_version = self.platform_config.get("platformVersion")
        self.device_name = self.platform_config.get("deviceName")
        self.automation_name = self.platform_config.get("automationName")
        self.activity = self.platform_config.get("appActivity")
        self.capabilities = self.platform_config.get("capabilities", {})

        text_print("\n📱 Device Info","green")
        text_print("------------------------")
        text_print(f"run_type : {self.run_type}","green")
        text_print(f"platform : {self.platform}", "green")
        text_print(f"platform_version : {self.platform_version}", "green")
        text_print(f"device_name : {self.device_name}", "green")
        text_print(f"app/appPackage : {self.app}", "green")
        text_print(f"automation_name : {self.automation_name}", "green")
        text_print("------------------------\n")

    def get_project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def get_app_path(self):
        """Get app path for mobile testing"""
        if self.run_type.lower() in ["lambdatest", "browserstack"]:
            return self.app
        
        root = self.get_project_root()
        app_directory = root.parent / "app"
        app_file_path = app_directory / self.app
        
        if not app_file_path.exists():
            raise FileNotFoundError(f"App file not found: {app_file_path}")
        return str(app_file_path.resolve())

    def get_capabilities(self):
        """Generate capabilities based on platform"""
        if self.run_type.lower() == "android":
            # Required capabilities
            caps = {
                'platformName': 'Android',
                'deviceName': self.device_name,
                'platformVersion': str(self.platform_version),
                'automationName': self.automation_name,
                'appActivity': self.activity
            }
            
            # Check if app path contains .apk
            if '.apk' in str(self.app).lower():
                caps['app'] = self.get_app_path()
            else:
                caps['appPackage'] = self.app


        elif self.run_type.lower() == "ios":
            # Required capabilities
            caps = {
                'platformName': 'iOS',
                'deviceName': self.device_name,
                'platformVersion': self.platform_version,
                'app': self.get_app_path(),
                'automationName': self.automation_name

            }
            
        elif self.run_type.lower() == "lambdatest":
            caps = {
                'platformName': self.platform,
                'deviceName': self.device_name,
                'platformVersion': self.platform_version,
                'isRealMobile': self.platform_config.get("isRealMobile", True),
                'app': self.app
            }
            
        elif self.run_type.lower() == "browserstack":
            caps = {
                'platform': self.platform,
                'browser': self.platform_config.get("browser"),
                'browserVersion': self.platform_config.get("browserVersion")
            }
        else:
            raise ValueError(f"Unsupported platform type: {self.run_type}")

        # Merge with optional capabilities from JSON config
        if self.capabilities:
            caps.update(self.capabilities)
            
        return caps

    def is_real_device(self):
        capabilities = self.driver.capabilities
        platform = capabilities.get("platformName", "").lower()

        if platform == "android":
            device_name = capabilities.get("deviceName", "").lower()
            avd = capabilities.get("avd")  # Present only on emulators
            is_real = not (device_name.startswith("emulator") or avd)

        elif platform == "ios":
            is_real = capabilities.get("isRealMobile")  # Default True if missing

        else:
            is_real = False

        print(f"Device Type : {'Real Device' if is_real else 'Emulator/Simulator'}")
        return is_real

    def get_server_url(self):
        """Get appropriate server URL based on platform"""
        if self.run_type.lower() == "lambdatest":
            username = os.getenv("LT_USERNAME")
            access_key = os.getenv("LT_ACCESS_KEY")
            if not (username and access_key):
                raise ValueError("LambdaTest credentials not found in environment variables")
            return f"https://{username}:{access_key}@mobile-hub.lambdatest.com/wd/hub"
            
        elif self.run_type.lower() == "browserstack":
            username = os.getenv("BS_USERNAME")
            access_key = os.getenv("BS_ACCESS_KEY")
            if not (username and access_key):
                raise ValueError("BrowserStack credentials not found in environment variables")
            return f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
            
        else:
            return "http://127.0.0.1:4723"

    def start_appium_service(self):
        """Start Appium service if not running"""
        try:
            print(Fore.GREEN +"Starting Appium service...")
            self.appium_service = AppiumService()
            self.appium_service.start()
            print(Fore.GREEN +"Appium service started successfully." +emoji.emojize("✅", language='alias'))
        except Exception as e:
            print(Fore.RED +f"Error starting Appium service: {e}")
            raise

    def init_driver(self):
        """Initialize appropriate driver based on platform"""
        try:
            # Start Appium service for local mobile testing
            if self.run_type.lower() in ["android", "ios"]:
                self.start_appium_service()

            final_capabilities = self.get_capabilities()
            server_url = self.get_server_url()

            print(Fore.GREEN +"Server URL:", server_url)
            print(Fore.YELLOW +"Final Capabilities:", final_capabilities)
            
            options = AppiumOptions()
            for key, value in final_capabilities.items():
                options.set_capability(key, value)

            self.driver = webdriver.Remote(
                command_executor=server_url,
                options=options
            )
            
            assert self.driver is not None, "Appium driver failed to initialize"
            print(Fore.GREEN +"Driver initialized successfully")
            self.is_real_device()
            return self.driver
            
        except Exception as e:
            print(Fore.RED +f"\nError initializing driver: {str(e)}")
            if self.appium_service:
                self.appium_service.stop()
            raise

    def cleanup(self):
        """Cleanup method to properly close the app and driver"""
        if self.driver:
            try:
                # Get the current package name (for Android)
                if self.run_type.lower() == "android":
                    current_package = self.driver.current_package
                    self.driver.terminate_app(current_package)
                
                # For iOS (if needed)
                elif self.run_type.lower() == "ios":
                    current_bundle = self.driver.current_package
                    self.driver.terminate_app(current_bundle)
                
            except Exception as e:
                print(Fore.RED +f"Error during app termination: {e}")
            
            finally:
                try:
                    self.driver.quit()
                except Exception as e:
                    print(Fore.RED +f"Error during driver quit: {e}")
                
                # Stop Appium service
                if self.appium_service:
                    try:
                        print(Fore.GREEN + "Stopping Appium service..." + emoji.emojize("⏹", language='alias'))
                        self.appium_service.stop()
                        print(Fore.GREEN + "Appium service stopped." + emoji.emojize("🔚", language='alias'))
                    except Exception as e:
                        print(Fore.RED +f"Error stopping Appium service: {e}")

# Global instance of DriverFactory
_driver_factory = None

def init_driver():
    """Initialize driver using factory"""
    global _driver_factory
    _driver_factory = DriverFactory()
    return _driver_factory.init_driver()


def cleanup_driver():
    global _driver_factory
    if _driver_factory and hasattr(_driver_factory, "driver"):
        driver = _driver_factory.driver
        try:
            # Attempt to terminate the app before quitting the driver
            platform = driver.capabilities.get("platformName", "").lower()

            if platform == "android":
                current_package = driver.current_package
                driver.terminate_app(current_package)

            elif platform == "ios":
                # Try to get bundle ID from capabilities or active app
                bundle_id = driver.capabilities.get("bundleId")
                if not bundle_id:
                    try:
                        bundle_id = driver.execute_script("mobile: activeAppInfo").get("bundleId")
                    except Exception as info_err:
                        print(f"Could not retrieve active bundle ID: {info_err}")

                if bundle_id:
                    driver.terminate_app(bundle_id)

        except Exception as e:
            print(f"Error during app termination: {e}")

        finally:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error during driver quit: {e}")
            _driver_factory = None


def init_alt_tester_driver(host="127.0.0.1", port=13000, app_name="__default__"):
    """Initialize AltTester driver using factory"""
    driver_factory = DriverFactory()
    return driver_factory.init_alt_tester_driver(host, port, app_name)