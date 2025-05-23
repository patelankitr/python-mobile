from pathlib import Path
from framework.mobile.wait import Wait
from framework.mobile.element import Element
from framework.mobile.verify import Verify
from framework.mobile.prints import text_print

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self._json_file_path = str(Path(__file__).parent.parent / "login"/"login_page.json")
        text_print(f"JSON file_path: {self._json_file_path}")
        self.element = Element(driver, self._json_file_path)
        self.wait = Wait(driver, self._json_file_path)
        self.verify = Verify(driver, self._json_file_path)

    def enter_phone_number(self):
        self.element.tap_on_element('phone_email_textbox',5)
        self.element.enter_text('phone_email_textbox','8887775332')

    def tap_on_continue_button(self):
        self.element.tap_on_element('continue_text_ui_button',20)

    def enter_password(self):
        self.wait.wait_for_seconds(5)
        self.element.tap_on_element('password_textbox',5)
        self.element.enter_text('password_textbox','QA123456')

    def tap_on_login_button(self):
        self.element.tap_on_element('login_with_password_button')

    def verify_a_user_logged_in_successfully(self):
        self.wait.wait_for_seconds(5)
        self.verify.element_visible('profile_name')
        self.wait.wait_for_seconds(10)