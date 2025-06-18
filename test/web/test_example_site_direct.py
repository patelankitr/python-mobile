import pytest
from playwright.async_api import async_playwright, Page
from pages.web.example_site import ExampleDotComPage
from colorama import Fore, Style


@pytest.fixture(scope="function")
async def page():
    """Fixture to initialize and clean up the browser for each test"""
    print(f"\n{Style.BRIGHT}🔧 Setting up test environment...{Style.RESET_ALL}")
    
    playwright = None
    browser = None
    context = None
    page = None
    
    try:
        # Start Playwright
        playwright = await async_playwright().start()
        print(Fore.CYAN + "✅ Playwright started")
        
        # Launch browser
        browser = await playwright.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        print(Fore.CYAN + "✅ Browser launched")
        
        # Create context with viewport settings
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        print(Fore.CYAN + "✅ Browser context created")
        
        # Create new page
        page = await context.new_page()
        print(Fore.CYAN + "✅ New page created")
        
        # Set timeouts
        page.set_default_timeout(30000)
        page.set_default_navigation_timeout(30000)
        
        yield page
        
    except Exception as e:
        print(Fore.RED + f"❌ Test setup failed: {str(e)}")
        raise
        
    finally:
        print(f"\n{Style.BRIGHT}🧹 Cleaning up...{Style.RESET_ALL}")
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        print(Fore.GREEN + "✅ Cleanup completed")


@pytest.mark.asyncio
async def test_example_site_content(page):
    """
    Test Case: Verify Example.com content and navigation
    
    Steps:
    1. Navigate to example.com
    2. Verify page is loaded and ready
    3. Verify main paragraph content
    4. Click More Information link
    5. Verify navigation to IANA website
    """
    print(f"\n{Style.BRIGHT}🚀 Starting Example.com content test{Style.RESET_ALL}")
    
    try:
        # Initialize page object
        example_page = ExampleDotComPage(page)
        
        # Step 1: Navigate to the website
        print("\n📋 Step 1: Navigating to example.com")
        await page.goto(
            "https://example.com",
            wait_until="networkidle",
            timeout=30000
        )
        print(Fore.GREEN + "✅ Navigation complete")
        
        # Step 2: Verify page is ready
        print("\n📋 Step 2: Verifying page readiness")
        await example_page.verify_page_ready()
        
        # Step 3: Verify paragraph content
        print("\n📋 Step 3: Checking main content")
        paragraph_text = await example_page.get_main_paragraph_text()
        assert "for use in illustrative examples" in paragraph_text.lower(), \
            f"Unexpected paragraph content: {paragraph_text}"
        print(Fore.GREEN + "✅ Content verified")
        
        # Step 4: Click More Information link
        print("\n📋 Step 4: Testing navigation")
        await example_page.click_more_information()
        
        # Step 5: Verify navigation
        print("\n📋 Step 5: Verifying navigation result")
        current_url = page.url
        assert "iana.org" in current_url, f"Unexpected URL after navigation: {current_url}"
        print(Fore.GREEN + "✅ Navigation successful")
        
        print(f"\n{Style.BRIGHT}✨ Test completed successfully{Style.RESET_ALL}")
        
    except AssertionError as ae:
        print(Fore.RED + f"\n❌ Assertion failed: {str(ae)}")
        # Take screenshot on failure
        if page:
            await page.screenshot(path="test-failure.png")
            print(Fore.YELLOW + "📸 Failure screenshot saved as 'test-failure.png'")
        raise
    except Exception as e:
        print(Fore.RED + f"\n❌ Test failed: {str(e)}")
        # Take screenshot on failure
        if page:
            await page.screenshot(path="test-failure.png")
            print(Fore.YELLOW + "📸 Failure screenshot saved as 'test-failure.png'")
        raise
