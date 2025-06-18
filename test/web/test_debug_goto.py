# tests/test_debug_goto.py
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_minimal_goto():
    print("🚀 Launching Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("🌐 Navigating to example.com")
            await page.goto("https://example.com", timeout=10000, wait_until="domcontentloaded")
            print("✅ Page loaded.")
        except Exception as e:
            print(f"❌ Exception: {e}")
        finally:
            await browser.close()
