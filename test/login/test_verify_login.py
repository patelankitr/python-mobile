import pytest
from framework.init.base import init_driver, cleanup_driver
from pages.login.login_page import *
from colorama import Fore

@pytest.fixture(scope="function")
def driver():
    print(Fore.GREEN +"\nSetting up test...")
    driver = init_driver()
    yield driver
    print(Fore.GREEN +"\nCleaning up test...")
    cleanup_driver()

@pytest.mark.login
def test_verify_login_functionality(driver):
    login = LoginPage(driver)

    login.enter_phone_number()
    login.tap_on_continue_button()
    login.enter_password()
    login.tap_on_login_button()
    login.verify_a_user_logged_in_successfully()


