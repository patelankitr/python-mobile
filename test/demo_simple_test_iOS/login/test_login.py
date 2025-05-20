import pytest
from framework.init.base import init_driver, cleanup_driver
from pages.demo_simple.login_simple_iOS.login_page import *
from colorama import Fore

@pytest.fixture(scope="function")
def driver():
    print(Fore.GREEN +"\nSetting up test...")
    driver = init_driver()
    yield driver
    print(Fore.GREEN +"\nCleaning up test...")
    cleanup_driver()

@pytest.mark.login
def test_verify_calculation_functionality(driver):
    login = LoginPage(driver)

    login.calculate_the_value() #com.google.android.apps.maps

