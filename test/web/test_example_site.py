import pytest
from pages.web.example_site import ExampleDotComPage
from framework.init.base import async_init_web_driver, async_cleanup_web_driver_session
from colorama import Fore, Style


@pytest.fixture(scope="function")
async def page():
    """Fixture to initialize and clean up the browser for each test"""
    print(f"\n{Style.BRIGHT}🔧 Setting up test environment...{Style.RESET_ALL}")
    try:
        # Initialize browser and get page object
        page = await async_init_web_driver()
        print(Fore.GREEN + "✅ Browser initialized successfully")
        yield page
    except Exception as e:
        print(Fore.RED + f"❌ Test setup failed: {str(e)}")
        raise
    finally:
        # Clean up after test
        print(f"\n{Style.BRIGHT}🧹 Cleaning up...{Style.RESET_ALL}")
        await async_cleanup_web_driver_session()
        print(Fore.GREEN + "✅ Cleanup completed")


@pytest.mark.asyncio
async def test_example_site_content(page):
    """
    Test Case: Verify Example.com content and navigation
    
    Steps:
    1. Verify page is loaded and ready
    2. Verify main paragraph content
    3. Click More Information link
    4. Verify navigation to IANA website
    """
    print(f"\n{Style.BRIGHT}🚀 Starting Example.com content test{Style.RESET_ALL}")
    
    try:
        # Initialize page object
        example_page = ExampleDotComPage(page)
        
        # Step 1: Verify page is ready
        print("\n📋 Step 1: Verifying page readiness")
        await example_page.verify_page_ready()
        
        # Step 2: Verify paragraph content
        print("\n📋 Step 2: Checking main content")
        paragraph_text = await example_page.get_main_paragraph_text()
        assert "for use in illustrative examples" in paragraph_text.lower(), \
            f"Unexpected paragraph content: {paragraph_text}"
        print(Fore.GREEN + "✅ Content verified")
        
        # Step 3: Click More Information link
        print("\n📋 Step 3: Testing navigation")
        await example_page.click_more_information()
        
        # Step 4: Verify navigation
        print("\n📋 Step 4: Verifying navigation result")
        current_url = page.url
        assert "iana.org" in current_url, f"Unexpected URL after navigation: {current_url}"
        print(Fore.GREEN + "✅ Navigation successful")
        
        print(f"\n{Style.BRIGHT}✨ Test completed successfully{Style.RESET_ALL}")
        
    except AssertionError as ae:
        print(Fore.RED + f"\n❌ Assertion failed: {str(ae)}")
        raise
    except Exception as e:
        print(Fore.RED + f"\n❌ Test failed: {str(e)}")
        raise
