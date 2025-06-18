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
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from playwright.sync_api import sync_playwright, Page # Added Page import
from playwright.async_api import async_playwright
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
        self.playwright = None # Playwright instance
        self.browser = None    # Browser instance
        self.context = None    # Context instance
        self.page = None       # Page instance

        # Load configuration
        project_root = Path(__file__).resolve().parent.parent.parent
        config_path = project_root / "config" / "TestConfig.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {config_path}")
        # Initialize config reader with dynamic path
        self.config_reader = ConfigReader(str(config_path))
        self.run_type = self.config_reader.get_run_platform()
        self.platform_config = self.config_reader.get_platform_config()
        print(f"platform_config : {self.platform_config}", "green")
        # exit()
        # Extract common values
        self.platform = self.platform_config.get("platform")
        self.app = self.platform_config.get("appPath/appPackage")
        self.platform_version = self.platform_config.get("platformVersion")
        self.device_name = self.platform_config.get("deviceName")
        self.automation_name = self.platform_config.get("automationName")
        self.activity = self.platform_config.get("appActivity")
        self.capabilities = self.platform_config.get("capabilities", {})
        self.browser = self.platform_config.get("browser")
        self.base_url = self.platform_config.get("base_url")
        self.headless = self.platform_config.get("headless")   

        text_print("\n📱 Device Info","green")
        text_print("------------------------")
        text_print(f"run_type : {self.run_type}","green")
        text_print(f"platform : {self.platform}", "green")
        # Only print mobile-specific info if relevant
        if self.run_type.lower() in ["android", "ios", "lambdatest"]:
            text_print(f"platform_version : {self.platform_version}", "green")
            text_print(f"device_name : {self.device_name}", "green")
            text_print(f"app/appPackage : {self.app}", "green")
            text_print(f"automation_name : {self.automation_name}", "green")
        elif self.run_type.lower() == "web":
            text_print(f"browser : {self.platform_config.get('browser')}", "green")
            text_print(f"headless : {self.platform_config.get('headless')}", "green")
            text_print(f"base_url : {self.platform_config.get('base_url')}", "green")
        text_print("------------------------\n")

    def get_project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent

    async def async_init_web_driver_page(self) -> Page:
        """Initializes Playwright asynchronously and returns a Page object."""
        self.playwright = await async_playwright().start()

        if self.browser == "chromium":
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
        elif self.browser == "firefox":
            self.browser = await self.playwright.firefox.launch(headless=self.headless)
        elif self.browser == "webkit":
            self.browser = await self.playwright.webkit.launch(headless=self.headless)
        else:
            print(Fore.YELLOW + f"Unsupported or unspecified browser: {self.browser}, defaulting to chromium.")
            self.browser = await self.playwright.chromium.launch(headless=self.headless)

        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        if self.base_url:
            print(Fore.CYAN + f"🌐 Navigating to base_url: {self.base_url}")
            await self.page.goto(self.base_url)
        else:
            print(Fore.YELLOW + "⚠️ No base_url configured. Page will not navigate initially.")

        return self.page

    async def async_cleanup_web_driver_session(self):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ Playwright and browser cleaned up.")


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
        # elif self.run_type.lower() == "web":
        #     init_web_driver(self.base_url)
            
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

    def start(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self.page

    def stop(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


    def init_alt_tester_driver(self, host="127.0.0.1", port=13000, app_name="__default__"):
        """Initialize AltTester driver"""
        return AltDriver(host=host, port=port, app_name=app_name)        
    def init_web_driver_page(self) -> Page:
        """Initializes Playwright and returns a Page object."""
        print(Fore.CYAN + "🔧 Initializing web driver...")
        
        try:
            browser_name = self.browser
            self.playwright = sync_playwright().start()
            
            # Launch browser with proper configuration
            browser_options = {
                "headless": self.headless,
                "args": ["--start-maximized"],
                "viewport": {"width": 1920, "height": 1080}
            }
            
            if browser_name == "chromium":
                self.browser = self.playwright.chromium.launch(**browser_options)
            elif browser_name == "firefox":
                self.browser = self.playwright.firefox.launch(**browser_options)
            elif browser_name == "webkit":
                self.browser = self.playwright.webkit.launch(**browser_options)
            else:
                print(Fore.YELLOW + f"Unsupported or unspecified browser: {browser_name}, defaulting to chromium.")
                self.browser = self.playwright.chromium.launch(**browser_options)
                
            # Create context with viewport settings
            self.context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
            self.page = self.context.new_page()
            
            # Configure timeouts
            self.page.set_default_timeout(30000)  # 30 seconds
            self.page.set_default_navigation_timeout(30000)
            
            # Initial navigation if base_url is configured
            if self.base_url:
                print(Fore.CYAN + f"🌐 Navigating to: {self.base_url}")
                response = self.page.goto(
                    self.base_url,
                    wait_until="networkidle",
                    timeout=30000
                )
                
                if response and response.ok:
                    print(Fore.GREEN + "✅ Page loaded successfully")
                    # Wait for page to be fully loaded
                    self.page.wait_for_load_state("domcontentloaded")
                    self.page.wait_for_load_state("networkidle")
                else:
                    print(Fore.RED + f"⚠️ Page load returned status: {response.status if response else 'unknown'}")
            else:
                print(Fore.YELLOW + "⚠️ No base_url configured. Page will not navigate initially.")
                
            print(Fore.GREEN + "✅ Web driver initialized successfully")
            return self.page
            
        except Exception as e:
            print(Fore.RED + f"❌ Failed to initialize web driver: {str(e)}")
            if hasattr(self, 'page') and self.page:
                self.page.close()
            if hasattr(self, 'context') and self.context:
                self.context.close()
            if hasattr(self, 'browser') and self.browser:
                self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                self.playwright.stop()
            raise

    def cleanup_web_driver(self):
        """Cleans up Playwright resources."""
        if self.page:
            try:
                self.page.close()
            except Exception as e:
                print(Fore.RED + f"Error closing Playwright page: {e}")
        if self.context:
            try:
                self.context.close()
            except Exception as e:
                print(Fore.RED + f"Error closing Playwright context: {e}")
        if self.browser:
            try:
                self.browser.close()
            except Exception as e:
                print(Fore.RED + f"Error closing Playwright browser: {e}")
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception as e:
                print(Fore.RED + f"Error stopping Playwright: {e}")

# Global instance of DriverFactory
_driver_factory = None
_page_factory = None # Retain for web

def init_driver():
    """Initialize driver using factory"""
    global _driver_factory
    _driver_factory = DriverFactory()
    return _driver_factory.init_driver()


def cleanup_driver():
    global _driver_factory
    if _driver_factory and hasattr(_driver_factory, "driver") and _driver_factory.driver:
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

# Updated global init_web_driver function
def init_web_driver() -> Page:
    """Initializes Playwright page using factory and returns a Page object."""
    global _page_factory
    if _page_factory is None:
        _page_factory = DriverFactory() # Ensure it's initialized if not already
    return _page_factory.init_web_driver_page()

# Global cleanup for web driver, to be called from conftest.py or similar
def cleanup_web_driver_session():
    global _page_factory
    if _page_factory:
        _page_factory.cleanup_web_driver()
        _page_factory = None

# Global method to initialize Playwright and return Page
async def async_init_web_driver() -> Page:
    global _page_factory
    if _page_factory is None:
        _page_factory = DriverFactory()
    return await _page_factory.async_init_web_driver_page()

# Global method to cleanup
async def async_cleanup_web_driver_session():
    global _page_factory
    if _page_factory:
        await _page_factory.async_cleanup_web_driver_session()
        _page_factory = None        