import pytest
from framework.init.base import init_driver, cleanup_driver
from pages.login_with_google.login_with_google_page import LogInWithGoogle
from colorama import Fore
from framework.mobile.prints import text_print
from airtest.cli.parser import cli_setup
from airtest.core.api import *


@pytest.fixture(scope="function")
def poco_driver():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/b7eeffed?touch_method=MAXTOUCH&", ],
                   project_root="D:/Projects/python-mobile")
    start_app("best.bulbsmash.cash")
    sleep(5.0)


@pytest.mark.login
def test_verify_login_functionality(poco_driver):
    login = LogInWithGoogle()
    login.verify_facebook_login_button()
    login.verify_google_login_button()
    login.verify_sign_in_button()
    login.click_google_login_button()
    login.wait_for_google_email()
    login.verify_google_email_present()
    login.click_email_id()
    login.wait_for_burger_menu()
    login.click_burger_menu()
    login.verify_username_in_slider()
    login.click_settings_button()
    login.click_logout_button()
    text_print("Logged out successfully")
    login.verify_google_login_after_logout()