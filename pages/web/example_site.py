from framework.web.base_element import Element
from playwright.async_api import expect
from colorama import Fore

class ExampleDotComPage(Element):
    """Page object for example.com - a simple website to demonstrate test structure"""
    
    def __init__(self, page):
        super().__init__(page)
        # Define locators
        self.MAIN_HEADING = "h1"
        self.MORE_INFO_LINK = "a[href='https://www.iana.org/domains/reserved']"
        self.PARAGRAPH = "p"
        
    async def verify_page_ready(self):
        """Verify the page is loaded and ready for interaction"""
        try:
            print(Fore.CYAN + "🔍 Verifying page readiness...")
            
            # Wait for network and DOM to be ready
            await self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            
            # Verify title
            title = await self.page.title()
            print(Fore.CYAN + f"📑 Page title: {title}")
            assert "Example Domain" in title, f"Unexpected title: {title}"
            
            # Verify main heading is visible
            heading = self.page.locator(self.MAIN_HEADING)
            await expect(heading).to_be_visible(timeout=5000)
            heading_text = await heading.inner_text()
            assert heading_text == "Example Domain", f"Unexpected heading: {heading_text}"
            
            print(Fore.GREEN + "✅ Page is ready for testing")
            return True
            
        except Exception as e:
            print(Fore.RED + f"❌ Page readiness check failed: {str(e)}")
            raise
            
    async def get_main_paragraph_text(self) -> str:
        """Get the text of the main paragraph"""
        try:
            paragraph = self.page.locator(self.PARAGRAPH)
            await expect(paragraph).to_be_visible(timeout=5000)
            return await paragraph.inner_text()
        except Exception as e:
            print(Fore.RED + f"❌ Failed to get paragraph text: {str(e)}")
            raise
            
    async def click_more_information(self):
        """Click the 'More information' link"""
        try:
            print(Fore.CYAN + "🖱️ Clicking 'More information' link...")
            link = self.page.locator(self.MORE_INFO_LINK)
            await expect(link).to_be_visible(timeout=5000)
            
            # Hover first to ensure interactivity
            await link.hover()
            await link.click()
            
            # Wait for navigation
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            print(Fore.GREEN + "✅ Clicked successfully")
            
        except Exception as e:
            print(Fore.RED + f"❌ Failed to click link: {str(e)}")
            raise
