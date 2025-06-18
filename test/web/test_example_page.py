import pytest
import asyncio
from pages.web.example_page import ExamplePage
from framework.init.base import async_cleanup_web_driver_session, async_cleanup_web_driver_session # Added cleanup_web_driver_session
from colorama import Fore

@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def page():
    print(Fore.GREEN + "\nSetting up web test (async)...")
    page = await async_cleanup_web_driver_session()
    yield page
    print(Fore.GREEN + "\nWeb test cleanup (async)...")
    await async_cleanup_web_driver_session()

@pytest.mark.asyncio
async def test_page_title(page):
    page = await ExamplePage().launch_browser()
    title = await page.get_title()
    assert title == "Example Domain"
    await page.close_browser()
