import time
import random

import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@allure.title("Car History Report Without Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_car_history_without_login():
    with allure.step("Start browser and open Vehicle Info application"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(driver, 15)
        driver.get("https://staging.vehicleinfo.app/")
        driver.maximize_window()

    try:
        with allure.step("Click on 'Car History Report' from Home page"):
            click_on_element(driver, "//div[@aria-label='Check Service History Report']")

        vehicle_numbers = [
            "GJ09BN0209", # Brand selection screen
            "GJ05JK7893", # Report Unavailable popup
            "GJ17CA3661",  # Payment Summary Page
        ]
        allure.attach(
            "\n".join(vehicle_numbers),
            name="Vehicle Numbers Used",
            attachment_type=AttachmentType.TEXT
        )
        verify_car_history_report(driver, vehicle_numbers)

    finally:
        with allure.step("Close browser"):
            driver.quit()


def verify_car_history_report(driver, vehicle_numbers, timeout=5):
    wait = WebDriverWait(driver, 15)

    for vehicle_no in vehicle_numbers:
        with allure.step(f"Process vehicle number: {vehicle_no}"):

            vehicle_input = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@placeholder='Enter Vehicle Registration Number']")
                )
            )
            vehicle_input.clear()
            with allure.step(f"Enter Vehicle Number: {vehicle_no}"):
                vehicle_input.send_keys(vehicle_no)

            with allure.step("Click on Car Service History button"):
                click_on_element(driver, "//*[contains(text(),'Car ')]//parent::button")

            if is_element_visible(driver, "//button[contains(text(),'Change')]", "change button on payment summary page"):
                with allure.step("Change button on payment summary page is visible"):
                    is_element_visible(driver, "//button[contains(text(),'Change')]", 'change button on payment summary page')

            elif is_element_visible(driver, "//h1[normalize-space()='Which brand Of Car Do You Have?']","Title of Brand Selection Page"):
                with allure.step("Brand selection screen displayed"):
                    brand_texts = get_all_texts(driver, "//div[@class='cscard  ']//p")

                    allure.attach(
                        "\n".join(brand_texts),
                        name="Available Brands",
                        attachment_type=AttachmentType.TEXT
                    )

                    random_brand = random.choice(brand_texts)

                    allure.attach(
                        random_brand,
                        name="Selected Brand",
                        attachment_type=AttachmentType.TEXT
                    )

                    click_on_element(
                        driver,
                        "//div[@class='cscard  ']//p[contains(text(),'" + random_brand + "')]"
                    )

                    is_element_visible(driver, "//button[contains(text(),'Change')]",
                                       "change button on payment summary page")

                    click_on_element(driver, '//*[@alt="home page"]//parent::a[@aria-label="Home"]')
                    click_on_element(driver, "//div[@aria-label='Check Service History Report']")

            elif is_element_visible(driver, "//*[contains(text(),'Report Unavailable')]", "Report Unavailable popup"):
                with allure.step("Report Unavailable popup appeared"):
                    click_on_element(driver, "//button[contains(text(),'Got It')]")

            else:
                allure.attach(
                    "Unexpected screen appeared",
                    name="Unexpected State",
                    attachment_type=AttachmentType.TEXT
                )


@allure.step("Fetch all texts from elements")
def get_all_texts(driver, xpath, timeout=10):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    return [ele.text.strip() for ele in elements if ele.text.strip()]



def is_element_visible(driver, xpath,log, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        allure.description_html("Verified "+log+" is visible")
        return True
    except TimeoutException:
        allure.description_html("Verified " + log + " is not visible")
        return False


@allure.step("Click element: {xpath}")
def click_on_element(driver, xpath, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        return True
    except TimeoutException:
        allure.attach(
            xpath,
            name="Failed Click XPath",
            attachment_type=AttachmentType.TEXT
        )
        return False


if __name__ == "__main__":
    test_car_history_without_login()
