from framework.web.elements import WebElementActions
from framework.web.verify import WebVerify

class SadakLoginPage:
    def __init__(self, page):
        self.page = page
        self.actions = WebElementActions(page)
        self.verify = WebVerify(page)

    async def login_and_verify(self, mobile, password, otp, dashboard_url):
        await self.actions.fill_textbox_by_placeholder("Mobile Number", mobile)
        await self.actions.fill_textbox_by_placeholder("Password", password)
        await self.actions.click_button_by_text("Login")
        await self.actions.fill_otp_fields(otp_value=otp)
        await self.actions.wait_for_url(dashboard_url)
        await self.verify.verify_url(dashboard_url)
