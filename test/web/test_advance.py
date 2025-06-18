import pytest
import asyncio
from pages.web.example_page import ExamplePage
from framework.init.base import async_init_web_driver, async_cleanup_web_driver_session
from colorama import Fore, Style


@pytest.fixture(scope="function")
async def page():
    print("\n🔧 DEBUG: Setting up test fixture...")
    try:
        print("⏳ Initializing web driver...")
        page = await async_init_web_driver()
        print("✅ Web driver initialized successfully")
        yield page
    except Exception as e:
        print(f"❌ Web driver initialization failed: {str(e)}")
        raise
    finally:
        print("\n🧹 Cleaning up web driver session...")
        await async_cleanup_web_driver_session()
        print("✅ Cleanup completed")

@pytest.mark.asyncio
async def test_example_ui_elements(page):
    print(f"\n{Style.BRIGHT}🔍 DEBUG: Starting test execution...{Style.RESET_ALL}")
    
    try:
        # Step 1: Initialize page object and verify page load
        print("\n📋 Step 1: Initializing page object")
        example_page = ExamplePage(page)
        
        # Step 2: Verify page is loaded properly
        print("\n📋 Step 2: Verifying page state")
        await example_page.verify_loaded_state()
        
        # Step 3: Perform UI verifications
        print("\n📋 Step 3: Verifying UI elements")
        await example_page.verify_page_ui()
        example_page = ExamplePage(page)
        print("✅ Page object initialized")

        # Step 2: Navigate to homepage
        print("\n🌐 Step 2: Navigating to homepage")
        await example_page.navigate_to_homepage()
        print("✅ Navigation completed")

        # Step 3: Verify UI elements
        print("\n🔍 Step 3: Starting UI verification")
        await example_page.verify_page_ui()
        print("✅ UI verification completed")

        print(f"\n{Style.BRIGHT}✅ Test completed successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Style.BRIGHT}❌ Test failed: {str(e)}{Style.RESET_ALL}")
        # Take screenshot on failure
        await page.screenshot(path=f"test-failure-{asyncio.get_event_loop().time()}.png")
        raise
        example_page = ExamplePage(page)
        print("✅ Page object created successfully")
    except Exception as e:
        print(f"❌ Page object creation failed: {str(e)}")
        raise
    
    # # Step 2: Navigation
    # print("\n📋 Step 2: Starting navigation")
    # try:
    #     print("⏳ Attempting to navigate to homepage...")
    #     await example_page.navigate_to_homepage()
    #     current_url = page.url
    #     print(f"🌐 Current URL: {current_url}")
    #     print("✅ Navigation successful")
    # except Exception as e:
    #     print(f"❌ Navigation failed: {str(e)}")
    #     print(f"🔍 Last known URL: {page.url}")
    #     raise
    
    # Step 3: Verify UI Elements
    print("\n📋 Step 3: Starting UI verification")
    try:
        print("\n🔍 Starting page UI verification...")
        await example_page.verify_page_ui()
        print(f"{Style.BRIGHT}✅ All UI verifications completed successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"❌ UI verification failed: {str(e)}")
        print(f"🔍 Last known page state: {page.url}")
        # Take screenshot on failure
        try:
            timestamp = asyncio.get_event_loop().time()
            await page.screenshot(path=f"debug_screenshot_{timestamp}.png")
            print(f"📸 Debug screenshot saved as debug_screenshot_{timestamp}.png")
        except Exception as screenshot_error:
            print(f"❌ Failed to take debug screenshot: {str(screenshot_error)}")
        raise
