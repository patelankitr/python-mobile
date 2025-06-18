from framework.web.base_element import Element
from playwright.async_api import expect

class DuckDuckGoPage(Element):
    # Locators
    SEARCH_INPUT = "[name='q']"
    SEARCH_BUTTON = "[type='submit']"
    FIRST_RESULT = ".result__title a"
    
    def __init__(self, page):
        super().__init__(page)
    async def verify_initial_state(self):
        """Verify the page's initial state after navigation"""
        print("🔍 Verifying initial page state...")
        try:
            print("⏳ Waiting for page load states...")
            
            # Wait for initial load with timeout
            try:
                await self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                print("✅ DOM content loaded")
            except Exception as e:
                print(f"⚠️ DOM content load timeout: {str(e)}")
            
            try:
                await self.page.wait_for_load_state("networkidle", timeout=10000)
                print("✅ Network idle")
            except Exception as e:
                print(f"⚠️ Network idle timeout: {str(e)}")
            
            # Get and verify URL
            print("🔍 Checking current URL...")
            current_url = await self.page.evaluate('window.location.href')
            print(f"📍 Current URL: {current_url}")
            assert "duckduckgo.com" in current_url, f"Unexpected URL: {current_url}"
            
            # Verify search box with explicit wait and timeout
            print("🔍 Waiting for search box...")
            try:
                search_box = self.page.locator(self.SEARCH_INPUT)
                await expect(search_box).to_be_visible(timeout=5000)
                print("✅ Search box is visible")
                
                # Additional verification that the search box is interactive
                await search_box.hover()
                print("✅ Search box is interactive")
                
            except Exception as e:
                print(f"❌ Search box verification failed: {str(e)}")
                # Get page content for debugging
                content = await self.page.content()
                print(f"📄 Page content preview: {content[:200]}...")
                raise
            
            print("✅ Initial state verified successfully")
            return True
            
        except Exception as e:
            print(f"❌ Initial state verification failed: {str(e)}")
            print("🔍 Debug information:")
            try:
                print(f"  - Current URL: {await self.page.evaluate('window.location.href')}")
                print(f"  - Page title: {await self.page.title()}")
                print(f"  - Ready state: {await self.page.evaluate('document.readyState')}")
            except:
                print("  - Unable to get debug information")
            raise
    
    async def verify_page_loaded(self):
        """Verify the page is loaded properly"""
        try:
            print("🔍 Verifying page load...")
            await self.page.wait_for_selector(self.SEARCH_INPUT, state="visible")
            print("✅ Page verified")
            return True
        except Exception as e:
            print(f"❌ Page verification failed: {str(e)}")
            raise
    
    async def search(self, query: str):
        """Perform a search"""
        try:
            print(f"🔎 Searching for: {query}")
            search_box = self.page.locator(self.SEARCH_INPUT)
            await search_box.fill(query)
            await self.page.locator(self.SEARCH_BUTTON).click()
            await self.page.wait_for_load_state("networkidle")
            print("✅ Search completed")
        except Exception as e:
            print(f"❌ Search failed: {str(e)}")
            raise
    
    async def verify_search_results(self):
        """Verify search results are present"""
        try:
            print("🔍 Verifying search results...")
            results = self.page.locator(self.FIRST_RESULT)
            await expect(results).to_be_visible(timeout=5000)
            count = await results.count()
            print(f"✅ Found {count} results")
            return True
        except Exception as e:
            print(f"❌ Results verification failed: {str(e)}")
            raise
    
    async def get_first_result_text(self) -> str:
        """Get the text of the first search result"""
        try:
            print("🔍 Getting first result...")
            first_result = self.page.locator(self.FIRST_RESULT).first
            text = await first_result.inner_text()
            print(f"✅ First result: {text}")
            return text
        except Exception as e:
            print(f"❌ Failed to get first result: {str(e)}")
            raise
