class WebElementActions:
    """
    Reusable actions for web elements using Playwright.
    """
    def __init__(self, page):
        self.page = page

    async def fill_textbox_by_placeholder(self, placeholder_text, value):
        """
        Fill a textbox by its placeholder text.
        Args:
            placeholder_text: str, the placeholder text to search for
            value: str, the value to fill in
        """
        await self.page.get_by_placeholder(placeholder_text).fill(value)

    async def click_button_by_text(self, button_text):
        """
        Click a button by its visible text.
        Args:
            button_text: str, the text of the button to click
        """
        await self.page.get_by_text(button_text).click()

    async def fill_otp_fields(self, otp_value="123456", first_otp_selector='input[name="otp1"]', timeout=60000, delay=300):
        """
        Fill OTP fields by focusing the first input and typing the OTP digits.
        Args:
            otp_value: str, the full OTP value to type (e.g., "123456")
            timeout: int, max wait for first OTP input (ms)
            delay: int, delay between keystrokes (ms)
            first_otp_selector: str, selector for the first OTP input (default: 'input[name="otp1"]')
        """
        otp_input = await self.page.wait_for_selector(first_otp_selector, timeout=timeout)
        await otp_input.focus()
        for digit in otp_value:
            await self.page.keyboard.type(digit)
            await self.page.wait_for_timeout(delay)

    async def wait_for_url(self, url: str, timeout: int = 30000):
        """
        Wait for the page to navigate to a specific URL.
        Args:
            url: str, the URL to wait for
            timeout: int, timeout in ms (default: 30000)
        """
        await self.page.wait_for_url(url, timeout=timeout)
