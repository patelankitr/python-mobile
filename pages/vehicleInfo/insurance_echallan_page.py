import random
import re
from datetime import date, datetime
from pathlib import Path

import allure
from appium.webdriver.common.appiumby import AppiumBy

from framework.mobile.wait import Wait
from framework.mobile.element import Element
from framework.mobile.verify import Verify
from framework.mobile.prints import text_print


class Vehicle_Challan:
    def __init__(self, driver):
        self.driver = driver
        self._json_file_path = str(Path(__file__).parent.parent / "vehicleInfo"/"insurance_status.json")
        text_print(f"JSON file_path: {self._json_file_path}")
        self.element = Element(driver, self._json_file_path)
        self.wait = Wait(driver, self._json_file_path)
        self.verify = Verify(driver, self._json_file_path)

    @allure.step("Tap on close offer popup button")
    def tap_on_close_offer_popup_button(self):
        if self.verify.element_is_visible("close_offer_popup_button"):
            self.element.tap_on_element("close_offer_popup_button")
        else:
            text_print("close_offer_popup_button not visible")

    @allure.step("Tap on back button")
    def tap_on_back_button(self):
        self.element.tap_on_element('back_button')

    def convert_amount_to_int(self, amount_text):
        return int(
            amount_text.replace("₹", "")
            .replace(",", "")
            .strip()
        )

    @allure.step("Enter vehicle numbers on check challan screen")
    def enter_vehicle_number_box_on_check_challan_screen(self, vehicle_numbers):
        for vehicle_no in vehicle_numbers:
            print(f"\n🔍 Checking eChallan for vehicle: {vehicle_no}")
            self.element.clear_and_enter_text('vehicle_number_box_on_check_challan_screen', vehicle_no, 20)
            self.element.tap_on_element('get_challan_details_button')
            # if self.verify.element_is_visible("pay_now_button_for_pay_challan"):
                # self.element.tap_on_element("pay_now_button_for_pay_challan")
            # else:
            self.element.swipe_by_direction('up')
            self.element.tap_on_element("pay_now_button_for_pay_challan")

            challan_type = self.element.get_text("challan_type")
            if challan_type == "eCHALLAN":
                challan_amount_text = self.element.get_text("challan_amount")
                challan_amount = self.convert_amount_to_int(challan_amount_text)
                with allure.step(f"Challan Amount from UI:-  {challan_amount}"):
                    pass
                print(f"Challan Amount: {challan_amount}")
                self.element.tap_on_element("fees_info_icon")
                legal_fee_text = self.element.get_text("legal_fee_amount")
                legal_fee_amount = self.convert_amount_to_int(legal_fee_text)
                with allure.step(f"Legal Fee Amount from UI:-  {legal_fee_amount}"):
                    pass
                print(f"Legal Fee Amount: {legal_fee_amount}")

                if challan_amount > 1000:
                    self.wait.wait_for_seconds(10)
                    with allure.step("Challan amount > 1000 → Legal fee should be 299"):
                        pass
                    assert legal_fee_amount == 299, (
                        f"Expected legal fee 299 for challan > 1000, "
                        f"but got {legal_fee_amount}"
                    )
                    with allure.step(f"Legal fee verified as 299"):
                        pass
                    print("✅ Legal fee verified as 299 for challan amount > 1000")
                elif challan_amount > 500:
                    with allure.step("Challan amount > 500 → Legal fee should be 249"):
                        pass
                    self.wait.wait_for_seconds(10)
                    assert legal_fee_amount == 249, (
                        f"Expected legal fee 249 for challan > 500, "
                        f"but got {legal_fee_amount}"
                    )
                    with allure.step(f"Legal fee verified as 249"):
                        pass
                    print("✅ Legal fee verified as 249 for challan amount > 500")
                elif challan_amount <= 500:
                    self.wait.wait_for_seconds(10)
                    with allure.step("Challan amount ≤ 500 → Legal fee should be 139"):
                        pass
                    assert legal_fee_amount == 139, (
                        f"Expected legal fee 139 for challan <= 500, "
                        f"but got {legal_fee_amount}"
                    )
                    with allure.step(f"Legal fee verified as 139"):
                        pass
                    print("✅ Legal fee verified as 139 for challan amount <= 500")

                self.element.tap_on_element("i_understand_link")
                self.tap_on_back_button()
                self.tap_on_back_button()
                self.tap_on_close_offer_popup_button()

