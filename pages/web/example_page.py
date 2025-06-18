from framework.web.base_element import Element
from playwright.async_api import async_playwright, expect
from colorama import Fore
import asyncio

class ExamplePage(Element):
    def __init__(self, page):
        super().__init__(page)    
        
    async def verify_page_ui(self):
        try:
            # Wait for page to be ready
            print("⏳ Waiting for page to be ready...")
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_load_state("networkidle")
            print("✅ Page is ready")

            # Check header title with direct locator
            print("🔍 Checking header title...")
            header = self.page.locator('h1')
            await expect(header).to_be_visible(timeout=5000)
            await expect(header).to_have_text("Example Domain", timeout=5000)
            print("✅ Header title verified")

            # Check footer with specific wait
            print("🔍 Checking footer...")
            footer = self.page.locator('footer')
            await expect(footer).to_be_visible(timeout=5000)
            print("✅ Footer verified")

            # Check logo with retry
            print("🔍 Checking global logo...")
            logo = self.page.locator('img[alt="Example"]')
            await expect(logo).to_be_visible(timeout=5000)
            print("✅ Global logo verified")

            print("✅ All UI elements verified successfully")
            
        except Exception as e:
            print(f"❌ Error during UI verification: {str(e)}")
            # Take screenshot on failure
            await self.page.screenshot(path="error-screenshot.png")
            raise    async def verify_loaded_state(self):
        """Verify that the page is properly loaded and ready for testing"""
        try:
            print("🔍 Verifying page loaded state...")
            
            # Wait for network to be idle first
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            
            # Get URL using evaluate
            current_url = await self.page.evaluate('window.location.href')
            print(f"📍 Current URL: {current_url}")
            
            # Wait for document to be ready
            await self.page.wait_for_load_state("domcontentloaded")
            
            # Verify page state
            state = await self.page.evaluate('document.readyState')
            print(f"📋 Page state: {state}")
            
            if state != 'complete':
                raise Exception("Page is not fully loaded")
                
            # Wait for main content to be visible
            await self.page.wait_for_selector("h1", state="visible", timeout=5000)
            
            print("✅ Page is fully loaded and ready")
            return True
            
        except Exception as e:
            print(f"❌ Page state verification failed: {str(e)}")
            print(f"🔍 Debug info:")
            try:
                print(f"  - Current state: {await self.page.evaluate('document.readyState')}")
                print(f"  - Title: {await self.page.title()}")
            except:
                print("  - Unable to get debug info")
            raise

    async def click_more_info_link(self):
        more_info = self.page.locator("a", has_text="More information")
        await expect(more_info).to_be_visible()
        await more_info.click()
        await self.page.wait_for_load_state("load")