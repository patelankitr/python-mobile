import pytest
from framework.init.base import DriverFactory
from framework.web.verify import WebVerify

@pytest.mark.asyncio
async def test_google_title():
    """Test to verify Google page title"""
    driver_factory = DriverFactory()
    browser, context, page = await driver_factory.init_playwright_browser(url='https://www.google.com')
    
    try:
        
        # Get and verify the page title
       
        verify = WebVerify(page)
        await verify.verify_title('Google')
        print("Successfully verified Google page title")
        
    finally:
        # Cleanup
        await context.close()
        await browser.close()