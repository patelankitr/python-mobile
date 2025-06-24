from pathlib import Path
from framework.web.elements import WebElementActions
from framework.web.verify import WebVerify
from framework.web.wait import WebWait
from faker import Faker

class SadadInvoicePage:
    def __init__(self, page):
        self._json_file_path = str(Path(__file__).parent.parent / "sadad" / "sadad_invoice.json")
        self.page = page
        self.actions = WebElementActions(page, self._json_file_path)
        self.verify = WebVerify(page, self._json_file_path)
        self.wait = WebWait(page, self._json_file_path)

    async def invoice_verify(self):
        print(f"{self._json_file_path}")
        # Pause here for interactive debugging
        await self.actions.enter_text_from_file('login_mobile_number', 'fill-test-data.csv', 'A1', sheet_name='Sheet1')
        await self.actions.enter_text_from_file('login_password', 'fill-test-data.csv', 'B1', sheet_name='Sheet1')
        await self.actions.click_element("submit_button")
        await self.actions.fill_otp_by_locator("fill_otp", "111111")
        await self.page.wait_for_load_state("networkidle")
        # await self.wait.wait_until_element_is_visible("POS")
        
        await self.actions.select_dropdown_option_by_text("ng-dropdown", "Online Payment")
        await self.wait.wait_for_seconds(3)  # Waits for 3 seconds
        # await self.page.wait_for_load_state("networkidle")
        await self.verify.verify_url("https://aks-panel.sadad.qa/dashboard/online-payment-default")
        assert "online-payment-default" in self.page.url
        await self.actions.click_element("invoice_link")
        await self.wait.wait_for_seconds(3)  # Waits for 3 seconds
        # await self.page.wait_for_load_state("networkidle")
        await self.verify.verify_url("https://aks-panel.sadad.qa/merchantpanel/invoice")
        
        assert "invoice" in self.page.url
        # # await self.actions.click_element("submit_button")
        await self.wait.wait_until_element_is_visible('create_invoice')  # Waits for 2 seconds
        await self.actions.click_element("create_invoice")
          # Waits for 3 seconds

        get_country_code = await self.actions.get_text("verify-form-dial-code")
        await self.wait.wait_until_element_is_visible('form-mobile-number')  # Waits for 2 seconds
        await self.wait.wait_for_seconds(3)  # Waits for 2 seconds
        mobile_number = await self.actions.enter_text_from_file('form-mobile-number', 'fill-test-data.csv', 'H1', sheet_name='Sheet1')
        await self.wait.wait_for_seconds(3)  # Waits for 2 seconds
        completed_mobile_number = get_country_code + '-' + mobile_number
        print("mobile_number")
        print(completed_mobile_number)
        print("mobile_number")
        # await self.page.wait_for_load_state("networkidle")
        
        await self.wait.wait_until_element_is_visible('form-client-name')  # Waits for 2 seconds
        await self.wait.wait_for_seconds(3)  # Waits for 2 seconds
        await self.actions.enter_text_from_file('form-client-name', 'fill-test-data.csv', 'I1', sheet_name='Sheet1')
        await self.wait.wait_for_seconds(3)  # Waits for 2 seconds
        # await self.page.wait_for_load_state("networkidle")
        
        await self.wait.wait_until_element_is_visible('form-item-name')  # Waits for 2 seconds
        await self.actions.enter_text_from_file('form-item-name', 'fill-test-data.csv', 'J1', sheet_name='Sheet1')
        await self.wait.wait_until_element_is_visible('form-qty')  # Waits for 2 seconds
        await self.actions.enter_text_from_file('form-qty', 'fill-test-data.csv', 'K1', sheet_name='Sheet1')
        await self.wait.wait_until_element_is_visible('form-unit-price')  # Waits for 2 seconds
        await self.actions.enter_text_from_file('form-unit-price', 'fill-test-data.csv', 'L1', sheet_name='Sheet1')
        await self.wait.wait_until_element_is_visible('form-send-invoice-btn')  # Waits for 2 seconds
        # await self.page.pause()
        
        print("form-send-invoice-btn")
        # await self.actions.scroll_until_visible("form-send-invoice-btn")
        await self.actions.click_element("form-send-invoice-btn")
        print("form-send-invoice-btn")
        # await self.verify.verify_element_text("verify-form-invoice-status", "UNPAID")
        await self.verify.element_not_visible("heading-visible")
        # await self.wait.wait_for_seconds(10)  # Waits for 2 seconds
        await self.verify.verify_element_text("verify-form-invoice-status", "UNPAID", timeout=30)
        await self.verify.verify_element_text("verify-form-customer-name", "testo")
        await self.actions.get_text("verify-form-customer-mobile-number")

        await self.verify.verify_element_text("verify-form-customer-mobile-number", completed_mobile_number)