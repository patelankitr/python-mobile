import pytest
from framework.init.base import DriverFactory
from pages.web.sadak_login_page import SadakLoginPage

async def test_sadad_pos_dashboard_login_async():
    """Test Sadad POS dashboard login flow with OTP verification."""
    driver_factory = DriverFactory()
    browser, context, page = await driver_factory.init_playwright_browser()

    login_page = SadakLoginPage(page)
    await login_page.login_and_verify(
        mobile="54260065",
        password="SadadPass@123@",
        otp="111111",
        dashboard_url="https://aks-panel.sadad.qa/dashboard/pos-default"
    )

    # Cleanup
    await context.close()
    await browser.close()
