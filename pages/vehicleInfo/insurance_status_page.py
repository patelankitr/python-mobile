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


class Insurance_Vehicle:
    def __init__(self, driver):
        self.driver = driver
        self._json_file_path = str(Path(__file__).parent.parent / "vehicleInfo"/"insurance_status.json")
        text_print(f"JSON file_path: {self._json_file_path}")
        self.element = Element(driver, self._json_file_path)
        self.wait = Wait(driver, self._json_file_path)
        self.verify = Verify(driver, self._json_file_path)


    @allure.step("Tap on close button of update screen")
    def tap_on_close_button_of_update_screen(self):
        if self.verify.element_is_visible("close_button"):
            self.element.tap_on_element("close_button")
        else:
            text_print("close_button not visible")


    @allure.step("Tap on check price now button")
    def tap_on_check_price_now_button(self):
        self.element.tap_on_element("check_price_now_button")

    @allure.step("Tap on insurance button")
    def tap_on_insurance_button(self):
        self.element.start_screen_recording(quality='medium')
        self.wait.load_locators()
        self.element.tap_on_element("insurance_button")

    @allure.step("Tap on car history report")
    def tap_on_car_history_report(self):
        self.wait.load_locators()
        self.wait.wait_for_seconds(1)
        self.element.tap_on_element("car_history_report")

    @allure.step("Tap on check and pay challan")
    def tap_on_check_and_pay_challan(self):
        self.wait.load_locators()
        self.element.tap_on_element("check_and_pay_challan")

    @allure.step("Tap on get report button")
    def tap_on_get_report_button(self):
        self.element.tap_on_element("get_report_button")

    @allure.step("Verify report")
    def verify_report(self):
        if self.verify.element_is_visible("brand_screen_title"):
            assert self.verify.element_is_visible("brand_list"), "Brand list not visible"
            brand_list = self.element.get_all_texts("brand_name_list")
            print(f"Brand list: {brand_list}")

            if not brand_list:
                raise Exception("Brand list is empty")

            random_brand = random.choice(brand_list)
            print(f"Random brand selected: {random_brand}")

            self.driver.find_element(
                AppiumBy.XPATH,
                f'//android.widget.TextView[@text="{random_brand}"]'
            ).click()
            print(f"✅ Random brand clicked: {random_brand}")
            self.verify.element_is_visible("car_service_history_screen_title")
            self.tap_on_back_button()
            return  # 🔑 STOP further execution
        elif self.verify.element_is_visible("car_service_history_screen_title"):
            self.element.tap_on_element("pay_now_button")
            self.verify.element_is_visible("login_to_vehicle_info_popup")
            self.tap_on_skip_button_on_popup()
            self.tap_on_cancel_button()
            self.tap_on_close_button_of_access_your_car_service_report_popup()
            self.tap_on_back_button()
            return
        elif self.verify.element_is_visible("report_unavailable"):
            self.verify.element_visible("got_it_button")
            self.element.tap_on_element("got_it_button")
            return

        raise Exception("❌ None of the following are visible: the Brand screen, the Service History screen, or the “Report Unavailable” popup.")

    @allure.step("Tap on skip button on popup")
    def tap_on_skip_button_on_popup(self):
        if self.verify.element_is_visible("skip_button_on_popup"):
            self.element.tap_on_element("skip_button_on_popup")
        else:
            text_print("skip_button_on_popup not visible")

    @allure.step("Tap on cancel button")
    def tap_on_cancel_button(self):
        if self.verify.element_is_visible("cancel_button"):
            self.element.tap_on_element("cancel_button")
        else:
            text_print("cancel_button not visible")


    @allure.step("Tap on close button of access your car service report popup")
    def tap_on_close_button_of_access_your_car_service_report_popup(self):
        self.element.tap_on_element("close_button_of_access_your_car_service_report_popup")

    @allure.step("Tap on skip button for skip login")
    def tap_on_skip_button_for_skip_login(self):
        if self.verify.element_is_visible("skip_button"):
            self.element.tap_on_element("skip_button")
        else:
            text_print("skip_button not visible")


    @allure.step("Tap on close offer popup button")
    def tap_on_close_offer_popup_button(self):
        if self.verify.element_is_visible("close_offer_popup_button"):
            self.element.tap_on_element("close_offer_popup_button")
        else:
            text_print("close_offer_popup_button not visible")


    @allure.step("Enter vehicle number: {vehicle_number}")
    def enter_vehicle_number(self, vehicle_number):
        self.element.clear_and_enter_text('vehicle_number_box', vehicle_number, 20)

    @allure.step("Tap on back button")
    def tap_on_back_button(self):
        self.element.tap_on_element('back_button')

    @allure.step("Verify multiple vehicles insurance status")
    def verify_multiple_vehicles_insurance_status(self, vehicle_numbers):
        for vehicle_no in vehicle_numbers:
            print(f"\n🔍 Checking insurance for vehicle: {vehicle_no}")
            self.enter_vehicle_number(vehicle_no)
            self.tap_on_check_price_now_button()
            self.tap_on_cancel_button_for_close_choose_phone_number_popup()
            self.verify_insurance_status()
            self.tap_on_back_button()
            recording_path = self.element.stop_screen_recording("insurnance_status.mp4")
            if recording_path and Path(recording_path).exists():
                with open(recording_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="Screen recording",
                        attachment_type="video/mp4",
                    )

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
            self.element.tap_on_element("pay_now_button_for_pay_challan")
            challan_type = self.element.get_text("challan_type")
            if challan_type == "eCHALLAN":
                challan_amount_text = self.element.get_text("challan_amount")
                challan_amount = self.convert_amount_to_int(challan_amount_text)
                print(f"Challan Amount: {challan_amount}")
                self.element.tap_on_element("fees_info_icon")
                legal_fee_text = self.element.get_text("legal_fee_amount")
                legal_fee_amount = self.convert_amount_to_int(legal_fee_text)
                print(f"Legal Fee Amount: {legal_fee_amount}")

                if challan_amount > 1000:
                    self.wait.wait_for_seconds(10)
                    assert legal_fee_amount == 299, (
                        f"Expected legal fee 299 for challan > 1000, "
                        f"but got {legal_fee_amount}"
                    )
                    print("✅ Legal fee verified as 299 for challan amount > 1000")
                elif challan_amount > 500:
                    self.wait.wait_for_seconds(10)
                    assert legal_fee_amount == 299, (
                        f"Expected legal fee 299 for challan > 500, "
                        f"but got {legal_fee_amount}"
                    )
                    print("✅ Legal fee verified as 299 for challan amount > 500")
                elif challan_amount <= 500:
                    self.wait.wait_for_seconds(10)
                    assert legal_fee_amount == 149, (
                        f"Expected legal fee 139 for challan <= 500, "
                        f"but got {legal_fee_amount}"
                    )
                    print("✅ Legal fee verified as 139 for challan amount <= 500")

                self.element.tap_on_element("i_understand_link")
                self.tap_on_back_button()
                self.tap_on_back_button()
                self.tap_on_close_offer_popup_button()

    @allure.step("Enter vehicle number and get report")
    def enter_vehicle_number_then_get_report(self, vehicle_numbers):
        for vehicle_no in vehicle_numbers:
            print(f"\n🔍 Checking history for vehicle: {vehicle_no}")
            self.element.clear_and_enter_text('search_vehicle_number', vehicle_no, 20)
            self.tap_on_get_report_button()
            self.verify_report()

    @allure.step("Tap on lets start button")
    def tap_on_lets_start_button(self):
        self.wait.wait_until_element_is_visible('lets_start_button')
        self.element.tap_on_element('lets_start_button')
        self.wait.wait_for_seconds(5)

    @allure.step("Tap on cancel button for close choose phone number popup")
    def tap_on_cancel_button_for_close_choose_phone_number_popup(self):
        if self.verify.element_is_visible("cancel_button"):
            self.element.tap_on_element("cancel_button")
        else:
            text_print("cancel_button not visible")

    @allure.step("Verify insurance status")
    def verify_insurance_status(self):
        self.element.swipe_by_direction('up')
        actual_insurance_date_value = self.element.get_text("insurance_date_value")
        allure.step(f"Actual insurance date: {actual_insurance_date_value}")
        text_print("actual_insurance_date_value" + actual_insurance_date_value)

        today = date.today()
        text = actual_insurance_date_value.strip()
        self.element.swipe_by_direction('down')
        if text.lower().startswith("expired on"):
            expired_date_str = text.replace("Expired on", "").strip()
            expired_date = datetime.strptime(expired_date_str, "%d %b,%Y").date()
            allure.step(f"Actual insurance date: {actual_insurance_date_value} and expired date: {expired_date}")
            if expired_date >= today:
                raise AssertionError(
                    f"BUG: UI shows expired but date is not in past. "
                    f"Expired on: {expired_date}, Today: {today}"
                )
            self.wait.wait_for_seconds(10)
            self.verify.verify_element_text("insurance_status_message","Insurance Policy Expired")
            print(f"Insurance Policy Expired (Expired on {expired_date.strftime('%d %b,%Y')})")
            return

        match = re.search(r"\d{2} \w{3},\d{4}", text)
        if not match:
            raise ValueError("Invalid insurance date format")

        expiry_date = datetime.strptime(match.group(), "%d %b,%Y").date()
        days_left = (expiry_date - today).days
        print(f"days_left: {days_left}")


        if days_left > 365:
            self.wait.wait_for_seconds(10)
            self.verify.verify_element_text("insurance_status_message", "Your Vehicle Insurance is Protected")
            print("Your vehicle insurance is protected")
        elif days_left > 60:
            self.wait.wait_for_seconds(10)
            self.verify.verify_element_text("insurance_status_message", "Own Damage Policy Expiring?")
            print("Your vehicle insurance is protected")
        else:
            self.wait.wait_for_seconds(10)
            self.verify.verify_element_text("insurance_status_message", f"Insurance Expires in {days_left} Days!")
            print(f"Insurance will expire in {days_left} days")