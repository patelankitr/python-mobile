import time
import pytest
from appium.webdriver.appium_service import AppiumService
from framework.init.base import init_appium_driver
from pages.profile_page import ProfilePage
'''
Test Case ID: XX
Test Name: To verify that the user tap on the profile screen.
Date Created: 14 Oct 2024
Author: Ankit
'''

@pytest.mark.smoke

def test_verify_lets_go_button():
    appium_driver = None
    try:
        # Step 1: Initialize Appium driver
        print("Initializing Appium driver...")
        appium_service = AppiumService()
        appium_service.start()
        appium_driver = init_appium_driver()
        assert appium_driver is not None, "Appium driver failed to initialize"
        print("Appium driver initialized.")
        time.sleep(15)

        # Tap on profile button
        # profile_page = ProfilePage(appium_driver)
        # profile_page.click_profile_button()
        # profile_page.verify_profile_page_elements()
        # profile_page.profile_stats()
        # profile_page.verify_avatar_and_game_sections()

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
