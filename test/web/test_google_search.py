import pytest  
import re  
# from playwright.sync_api import Page, expect  
from framework.init.base import init_web_driver, cleanup_web_driver_session # Added cleanup_web_driver_session
from pages.web.google_search import *
from colorama import Fore

@pytest.fixture(scope="function") # Ensure function scope for page fixture
def page():
    print(Fore.GREEN + "\nSetting up web test...")
    # init_web_driver now returns a Page object directly
    playwright_page = init_web_driver() 
    yield playwright_page
    # Cleanup is handled by a session-scoped fixture in conftest.py
    print(Fore.GREEN +"\nWeb test cleanup (individual test)...")
    # No direct cleanup here; session fixture will handle it.

def test_google_search(page):
    googleSearch = GoogleSearch(page)
    
    # print("page2")
    # print(page)
    # print("page2")
    googleSearch.click_store_from_the_menu()
    # assert "Google" in page.title()
# @pytest.mark.basic
# def test_has_title(driver):  
#     page.goto("https://playwright.dev/")  
  
#     # Expect a title "to contain" a substring.  
#     expect(page).to_have_title(re.compile("Playwright"))  
  
  
# @pytest.mark.basic  
# def test_get_started_link():
#     # Click the get started link.  
#     page.get_by_role("link", name="Get started").click()  
  
#     # Expects page to have a heading with the name of Installation.  
#     expect(page.get_by_role("heading", name="Installation")).to_be_visible()



# import pytest
# from playwright.sync_api import sync_playwright, expect
# from colorama import Fore


# @pytest.fixture(scope="function")
# def driver():
#     print(Fore.GREEN + "\nSetting up browser...")

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         yield page
#         print(Fore.GREEN + "\nTearing down browser...")
#         context.close()
#         browser.close()

# @pytest.mark.basic
# def test_has_title(driver):
#     driver.goto("https://playwright.dev/")
#     expect(page).to_have_title(re.compile("Playwright"))