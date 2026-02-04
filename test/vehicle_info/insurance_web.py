import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def test_car_history_without_login():
    print("\n🚀 Test Started: Car History Report Without Login")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)

    try:
        print("🌐 Opening application URL")
        driver.get("https://staging.vehicleinfo.app/")
        driver.maximize_window()

        print("🖱️ Clicking on 'Car History Report'")
        click_on_element(driver, "//div[@aria-label='Check Service History Report']")

        vehicle_numbers = [
          # "GJ09BN0209",
           # "GJ05JK7893",
           # "GJ17CA3661",
           # "GJ05PD1408",
            "GJ05TZ9196"
        ]

        verify_car_history_report(driver, vehicle_numbers)

    finally:
        print("🧹 Closing browser")
        driver.quit()
        print("✅ Test Completed\n")


def verify_car_history_report(driver, vehicle_numbers, timeout=5):
    wait = WebDriverWait(driver, 15)

    for vehicle_no in vehicle_numbers:
        print("\n🔁 -----------------------------------------")
        print(f"🚗 Processing vehicle number: {vehicle_no}")

        time.sleep(2)

        vehicle_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter Vehicle Registration Number']")
            )
        )
        vehicle_input.clear()
        vehicle_input.send_keys(vehicle_no)
        print(f"✍️ Entered vehicle number: {vehicle_no}")

        print("🖱️ Clicking on Get Report button")
        click_on_element(driver, "//*[contains(text(),'Car ')]//parent::button")

        if is_element_visible(driver, "//button[contains(text(),'Change')]"):
            print("✅ Pay Now / Change button is visible")

            click_on_element(driver, '//*[@alt="home page"]//parent::a[@aria-label="Home"]')
            print("🏠 Navigated back to Home")

            click_on_element(driver, "//div[@aria-label='Check Service History Report']")
            print("🔄 Opened Car History Report again")

        elif is_element_visible(driver, "//h1[normalize-space()='Which brand Of Car Do You Have?']"):
            print("✅ Brand Selection screen appeared")

            brand_texts = get_all_texts(driver, "//div[@class='cscard  ']//p")
            print(f"📋 Brand list found ({len(brand_texts)}): {brand_texts}")

            random_brand = random.choice(brand_texts)
            print(f"🎯 Random brand selected: {random_brand}")

            click_on_element(
                driver,
                "//div[@class='cscard  ']//p[contains(text(),'" + random_brand + "')]"
            )
            print(f"🖱️ Clicked on brand: {random_brand}")

            is_element_visible(driver, "//button[contains(text(),'Change')]")

            click_on_element(driver, '//*[@alt="home page"]//parent::a[@aria-label="Home"]')
            print("🏠 Navigated back to Home")

            click_on_element(driver, "//div[@aria-label='Check Service History Report']")
            print("🔄 Opened Car History Report again")

        elif is_element_visible(driver, "//*[contains(text(),'Report Unavailable')]"):
            print("⚠️ Report Unavailable popup is visible")

            click_on_element(driver, "//button[contains(text(),'Got It')]")
            print("🖱️ Clicked on Got It button")

        else:
            print("❌ None of the expected screens appeared")
            time.sleep(3)


def get_all_texts(driver, xpath, timeout=10):
    print(f"🔍 Fetching all texts from xpath: {xpath}")
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    texts = [ele.text.strip() for ele in elements if ele.text.strip()]
    print(f"✅ Extracted texts: {texts}")
    return texts


def is_element_visible(driver, xpath, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        print(f"👁️ Element visible: {xpath}")
        return True
    except TimeoutException:
        print(f"🚫 Element NOT visible: {xpath}")
        return False


def click_on_element(driver, xpath, timeout=5):
    wait = WebDriverWait(driver, 15)
    try:
        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        print(f"🖱️ Clicked element: {xpath}")
        return True
    except TimeoutException:
        print(f"❌ Failed to click element: {xpath}")
        return False


if __name__ == "__main__":
    test_car_history_without_login()
