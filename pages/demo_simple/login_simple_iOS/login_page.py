from pathlib import Path
from framework.mobile.wait import Wait
from framework.mobile.element import Element
from framework.mobile.verify import Verify
from framework.mobile.prints import text_print
from framework.mobile.device import Device

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self._json_file_path = str(Path(__file__).parent.parent / "login_simple_iOS"/"login.json")
        self.element = Element(driver, self._json_file_path)
        self.wait = Wait(driver, self._json_file_path)
        self.verify = Verify(driver, self._json_file_path)
        self.device = Device(driver)


    def calculate_the_value(self):
        self.device.get_device_battery_level()
        #self.device.rotate_device('LANDSCAPE')
        self.element.start_screen_recording(quality='medium')
        self.element.enter_text('first_textbox','10')
        self.element.enter_text('second_textbox', '20')
        self.element.tap_on_element('sum_button')
        self.element.take_element_screenshot('sum_value','sum_value.png')
        #self.element.take_full_screenshot('home_screen_full.png')
        self.element.compare_full_screenshots('home_screen_full.png')
        self.element.compare_element_screenshots('sum_value','sum_value.png')
        self.element.stop_screen_recording('calculate_the_value.mp4')




