import pytest
# import pytest_wrapper
from framework.init.base import init_driver, cleanup_driver
from pages.demo_simple.login_simple.login_page import *
from colorama import Fore

@pytest.fixture(scope="function")
def driver():
    print(Fore.GREEN +"\nSetting up test...")
    driver = init_driver()
    yield driver
    print(Fore.GREEN +"\nCleaning up test...")
    cleanup_driver()

@pytest.mark.smokey
def test_verify_login_functionality(driver):
    login = LoginPage(driver)

    login.select_india_from_the_list() #com.google.android.apps.maps
    login.select_basalt_clinic()
    login.enter_mobile_number()
    login.tap_on_next_button()
    #login.enter_security_pin()
    #login.verify_setting_icon()
    #login.tap_setting_icon()
    #login.tap_on_logout_button()