import pytest
from framework.init.base import DriverFactory
from pages.web.sadad.sadad_invoice_page import SadadInvoicePage

async def test_sadad_pos_dashboard_invoice():
    """Test Sadad POS dashboard invoice flow with OTP verification."""
    driver_factory = DriverFactory()
    browser, context, page = await driver_factory.init_playwright_browser()

    invoice_page = SadadInvoicePage(page)
    await invoice_page.invoice_verify()

    # Cleanup
    await context.close()
    await browser.close()
