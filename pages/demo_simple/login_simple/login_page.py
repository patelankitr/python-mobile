from pathlib import Path
from framework.mobile.wait import Wait
from framework.mobile.element import Element
from framework.mobile.verify import Verify
from framework.mobile.prints import text_print
from framework.mobile.device import Device
from framework.readers.fileReader import FileReader

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self._json_file_path = str(Path(__file__).parent.parent / "login_simple"/"login.json")
        self.element = Element(driver, self._json_file_path)
        self.wait = Wait(driver, self._json_file_path)
        self.verify = Verify(driver, self._json_file_path)
        self.device = Device(driver)


    def select_india_from_the_list(self):
        self.device.get_device_battery_level()
        #self.device.rotate_device('LANDSCAPE')
        self.element.start_screen_recording(quality='medium')
        self.element.take_element_screenshot('splash_screen_next_button','splash_screen_next_button.png')
        self.element.take_full_screenshot('home_screen_full.png')
        self.element.compare_full_screenshots('home_screen_full.png')
        self.element.compare_full_screenshots('splash_screen_next_button.png')
        self.element.compare_element_screenshots('splash_screen_next_button','splash_screen_next_button.png')
        self.element.tap_on_element('splash_screen_next_button')
        self.element.take_element_screenshot('get_started_button', 'get_started_button.png')
        self.element.tap_on_element('get_started_button')
        self.element.tap_on_element('agree_and_continue_button')
        self.verify.element_present('select_your_country_title')
        self.element.tap_on_element('india')
        self.element.stop_screen_recording('login_test_recording.mp4')
        self.element.get_device_logs()


    def select_basalt_clinic(self):
        self.element.tap_on_element('basalt')


    def enter_mobile_number(self):
        phone_to_enter = "9090909090"  # Default fallback
        sheetName = 'Sheet2'
        cellName = 'A3'
        cellValue = FileReader.get_cell_value_from_excel(sheetName, cellName)
        FileReader.set_cell_value_in_excel(sheetName, "A11", "Ritik")
       
       
        # Proceed with mobile app interaction
        self.element.multi_tap('next_button', 2)
        self.element.get_text('your_phone_number_title')
        self.verify.element_present('your_phone_number_title')
        self.element.long_press_element('phone_number_textbox', duration=5000)
        self.element.enter_text('phone_number_textbox', cellValue)
        self.wait.wait_for_seconds(5)
        self.element.clear_and_enter_text('phone_number_textbox', cellValue)
    

    def tap_on_next_button(self):
        self.element.tap_on_element('next_button')


    def enter_security_pin(self):
        self.element.enter_text('security_pin_textbox','0000')

    def verify_setting_icon(self):
        self.verify.element_present('profile_setting_menu_icon')

    def tap_setting_icon(self):
        self.element.tap_on_element('profile_setting_menu_icon')

    def tap_on_logout_button(self):
        self.element.tap_on_element('logout_button')
        self.element.tap_on_element('logout_yes_button')

