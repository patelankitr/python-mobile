import pytest
import allure
from framework.init.base import init_driver, cleanup_driver
from colorama import Fore

from pages.vehicleInfo.insurance_echallan_page import Vehicle_Challan
from pages.vehicleInfo.insurance_status_page import Insurance_Vehicle


@allure.title("Vehicles Insurance Status")
@pytest.fixture(scope="function")
def driver():
    print(Fore.GREEN + "\nSetting up test...")
    driver = init_driver()
    yield driver
    print(Fore.GREEN + "\nCleaning up test...")
    cleanup_driver()

@pytest.mark.challan
def test_vehicles_challan_types_and_convenience_fees(driver):
    iv = Insurance_Vehicle(driver)
    vc = Vehicle_Challan(driver)
    iv.tap_on_close_button_of_update_screen()
    iv.tap_on_lets_start_button()
    iv.tap_on_skip_button_on_popup()
    iv.tap_on_cancel_button()
    iv.tap_on_skip_button_for_skip_login()
    iv.tap_on_close_offer_popup_button()
    iv.tap_on_check_and_pay_challan()
    vehicle_numbers = [
        "DL1MA4514",
        "WB25N4228",
    ]
    vc.enter_vehicle_number_box_on_check_challan_screen(vehicle_numbers)