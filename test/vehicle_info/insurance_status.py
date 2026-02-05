import pytest
import allure
from framework.init.base import init_driver, cleanup_driver
from colorama import Fore


from pages.vehicleInfo.insurance_status_page import Insurance_Vehicle

@allure.title("Vehicles Insurance Status")
@pytest.fixture(scope="function")
def driver():
    print(Fore.GREEN +"\nSetting up test...")
    driver = init_driver()
    yield driver
    print(Fore.GREEN +"\nCleaning up test...")
    cleanup_driver()

@pytest.mark.insurance
def test_vehicles_insurance_status(driver):
    iv = Insurance_Vehicle(driver)
    iv.tap_on_close_button_of_update_screen()
    iv.tap_on_lets_start_button()
    iv.tap_on_skip_button_on_popup()
    iv.tap_on_cancel_button()
    iv.tap_on_skip_button_for_skip_login()
    iv.tap_on_close_offer_popup_button()
    iv.tap_on_insurance_button()
    
    vehicle_numbers = [
        # "GJ05RT4737",
        # "GJ05JK7893",
        # "GJ17CA3661",
        # "GJ05PD1408",
        # "GJ05TZ9196"
        "UP16BZ7668"
    ]
    iv.verify_multiple_vehicles_insurance_status(vehicle_numbers)


@pytest.mark.challan
def test_vehicles_challan_types_and_convenience_fees(driver):
    iv = Insurance_Vehicle(driver)
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
        "KL26L9823",
    ]
    iv.enter_vehicle_number_box_on_check_challan_screen(vehicle_numbers)


@pytest.mark.history
def test_vehicles_car_history_report(driver):
    iv = Insurance_Vehicle(driver)
    iv.tap_on_close_button_of_update_screen()
    iv.tap_on_lets_start_button()
    iv.tap_on_skip_button_on_popup()
    iv.tap_on_cancel_button()
    iv.tap_on_skip_button_for_skip_login()
    iv.tap_on_close_offer_popup_button()
    iv.tap_on_car_history_report()
    vehicle_numbers = [
        "GJ09BN0209",
        "GJ05JK7893",
        "GJ17CA3661",
        "GJ05PD1408",
        "GJ05TZ9196"
    ]
    iv.enter_vehicle_number_then_get_report(vehicle_numbers)
