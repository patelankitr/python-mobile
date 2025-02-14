import time

from alttester import By, AltReversePortForwarding
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def verify_element_is_present_on_screen(alt_driver, locator_type, locator_value, comment, wait):
    # Set the condition to choose By.PATH or By.ID based on the provided locator_type
    if locator_type == 'PATH':
        element = alt_driver.wait_for_object(By.PATH, locator_value, timeout=wait)
    elif locator_type == 'ID':
        element = alt_driver.wait_for_object(By.ID, locator_value, timeout=wait)
    else:
        raise ValueError(f"Unsupported locator_type: {locator_type}. Use 'PATH' or 'ID'.")

    # Check if the element is present
    if element is not None:
        print(f"Print: '{comment}' is present on screen")
    else:
        print(f"Print: '{comment}' is NOT present on screen")

def tap_on_the_element(alt_driver, locator_type, locator_value, wait=None,comment=None ):
    # Set the condition to choose By.PATH or By.ID based on the provided locator_type
    if locator_type == 'PATH':
        element = alt_driver.wait_for_object(By.PATH, locator_value, timeout=wait)
    elif locator_type == 'ID':
        element = alt_driver.wait_for_object(By.ID, locator_value, timeout=wait)
    else:
        raise ValueError(f"Unsupported locator_type: {locator_type}. Use 'PATH' or 'ID'.")
    # Tap on the located element
    element.tap()
    if comment:
        print(f"Tapped on element: {comment}")
    else:
        print("Tapped on element")

def verify_element_contains(alt_driver, locator_type, locator_value, wait, expected_text):
    # Set the condition to choose By.PATH or By.ID based on the provided locator_type
    if locator_type == 'PATH':
        element_text = alt_driver.wait_for_object(By.PATH, locator_value, timeout=wait).get_text()
    elif locator_type == 'ID':
        element_text = alt_driver.wait_for_object(By.ID, locator_value, timeout=wait).get_text()
    else:
        raise ValueError(f"Unsupported locator_type: {locator_type}. Use 'PATH' or 'ID'.")

    # Assertion to verify the text
    assert element_text == expected_text, f"Expected '{expected_text}', but found '{element_text}'"
    print(f"Parameter: '{expected_text}' is found in the element located by {locator_type}.")

def access_appium_drive():
    print("Port forwarding to native element")
    AltReversePortForwarding.remove_reverse_port_forwarding_android()
    print("Port forwarded to native element")

def access_alt_tester_drive():
    time.sleep(15)
    print("Reverse port forwarding android")
    AltReversePortForwarding.reverse_port_forwarding_android()
    print("Port Reversed to unity element")



def click_on_the_element(appium_driver,locator_type, locator_value, wait=None,comment=None ):
    wait = WebDriverWait(appium_driver, wait)
    if locator_type == 'PATH':
        element = wait.until(ec.element_to_be_clickable((By.XPATH, locator_value)))
    elif locator_type == 'ID':
        element = wait.until(ec.element_to_be_clickable((By.ID, locator_value)))
    else:
        raise ValueError(f"Unsupported locator_type: {locator_type}. Use 'XPATH' or 'ID'.")
    # Tap on the located element
    element.click()
    if comment:
        print(f"Tapped on element: {comment}")
    else:
        print("Tapped on element")

    def verify_native_element_is_visible(driver, locator_type, locator_value, comment=None, wait_time=None):
        # Create a WebDriverWait instance
        wait = WebDriverWait(driver, wait_time)

        try:
            # Set the condition to choose By.XPATH or By.ID based on the provided locator_type
            if locator_type == 'XPATH':
                # Wait for the visibility of the element using By.XPATH
                element = wait.until(ec.visibility_of_element_located((By.XPATH, locator_value)))
            elif locator_type == 'ID':
                # Wait for the visibility of the element using By.ID
                element = wait.until(ec.visibility_of_element_located((By.ID, locator_value)))
            else:
                raise ValueError(f"Unsupported locator_type: {locator_type}. Use 'XPATH' or 'ID'.")

            # If the element is visible, print a success message
            print(f"Print: '{comment}' is visible on screen.")
        except Exception as e:
            # If any exception occurs (e.g., timeout), print a failure message
            print(f"Print: '{comment}' is NOT visible on screen. Exception: {str(e)}")