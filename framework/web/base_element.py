from playwright.async_api import expect

class Element:
    def __init__(self, page):
        self.page = page

    async def click(self, selector: str):
        await self.page.locator(selector).click()

    async def fill(self, selector: str, text: str):
        await self.page.locator(selector).fill(text)

    async def get_text(self, selector: str) -> str:
        return await self.page.locator(selector).inner_text()

    async def wait_until_visible(self, selector: str):
        await self.page.wait_for_selector(selector)

    async def assert_footer_present(self):
        footer = self.page.locator("footer")
        await expect(footer).to_be_visible()
        print("✅ Footer is visible")

    async def assert_global_logo_present(self):
        logo = self.page.locator("img[alt='Example']")  # Adjust as per app
        await expect(logo).to_be_visible()
        print("✅ Global logo is visible")    
    
    async def assert_header_title(self, expected_text):
        try:    
            # First wait for any loading to complete
            await self.page.wait_for_load_state("networkidle")
            
            # Locate the header and wait for it
            header = self.page.locator("h1")
            await header.wait_for(state="visible", timeout=5000)  # 5 seconds timeout
            
            # Use Playwright's built-in expect for better error messages
            await expect(header).to_be_visible()
            await expect(header).to_have_text(expected_text)
            
            print(f"✅ Header title matches: {expected_text}")
        except Exception as e:
            print(f"❌ Header title assertion failed: {str(e)}")
            raise
