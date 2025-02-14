import time
import pytest
from appium.webdriver.appium_service import AppiumService
from config import init_appium_driver, device_config
from pages.profile_page import ProfilePage
from pages.common_page import Login
from pages.common_page import astro_app_launch


'''
Test Case ID: 
Test Name: To verify when user login into Astrocade app.
Date Created: 15 Oct 2024
Author: Avinash Oza
'''

@pytest.mark.smoke
def test_verify_lets_go_button():
    appium_driver = None
    try:
        # Fetch device configuration from config_page
        device_name = device_config['device_name']
        platform_version = device_config['platform_version']
        app_path = device_config['app_path']

        # Step 1: Initialize Appium driver
        print("Initializing Appium driver...")
        appium_service = AppiumService()
        appium_service.start()

        appium_driver = init_appium_driver(device_name, platform_version, app_path)
        assert appium_driver is not None, "Appium driver failed to initialize"
        print("Appium driver initialized.")
        time.sleep(15)

        login = Login(appium_driver)
        #login.clear_app_data()
        profile_page = ProfilePage(appium_driver)
        profile_page.click_profile_button()
        login.sign_in_with_google()


    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")
    finally:
        # Ensure the drivers are closed after execution
        try:
            if appium_driver:
                appium_driver.quit()
                print("Appium driver closed.")
        except Exception as e:
            print(f"Failed to close Appium driver: {e}")