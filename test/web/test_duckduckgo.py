import pytest
from pages.web.duckduckgo_page import DuckDuckGoPage
from framework.init.base import async_init_web_driver, async_cleanup_web_driver_session
from colorama import Fore, Style

@pytest.fixture(scope="function")
async def page():
    """Fixture to set up and tear down the browser for each test"""
    print("\n🔧 Setting up test...")
    try:
        page = await async_init_web_driver()
        yield page
    finally:
        await async_cleanup_web_driver_session()
        print("✅ Test cleanup complete")

@pytest.mark.asyncio
async def test_duckduckgo_search(page):
    """Test DuckDuckGo search functionality"""
    print(f"\n{Style.BRIGHT}🔍 Starting DuckDuckGo search test...{Style.RESET_ALL}")
    
    try:
        # Initialize the page object
        duck_page = DuckDuckGoPage(page)
          # Step 1: Verify initial page state
        print("\n📋 Step 1: Verifying initial page state")
        await duck_page.verify_initial_state()
        
        # Step 2: Verify page elements
        print("\n📋 Step 2: Verifying page elements")
        await duck_page.verify_page_loaded()
        
        # Step 3: Perform search
        print("\n📋 Step 3: Performing search")
        search_query = "Playwright Python automation"
        await duck_page.search(search_query)
        
        # Step 4: Verify search results
        print("\n📋 Step 4: Verifying search results")
        await duck_page.verify_search_results()
        
        # Step 5: Get first result
        print("\n📋 Step 5: Getting first result")
        first_result = await duck_page.get_first_result_text()
        assert first_result, "First result should not be empty"
        
        print(f"\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise
