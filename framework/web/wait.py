from framework.web.elements import WebElementActions
import asyncio
from framework.mobile.prints import text_print

class WebWait:
    def __init__(self, page, json_path=None):
        self.page = page
        self.json_path = json_path
        self.actions = WebElementActions(self.page, self.json_path)

    async def wait_until_element_is_visible(self, locator_key, timeout=30):
        """
        Waits until the element specified by locator_key is visible on the page.
        Args:
            locator_key (str): Key in the JSON locator file
            timeout (int): Timeout in seconds (default: 30)
        Raises:
            TimeoutError: If the element is not visible after the timeout
        """

        locator_type, locator_value = self.actions.get_locator(locator_key)
        locator_type = locator_type.lower()
        # Map locator_type to Playwright locator method
        if locator_type == "css":
            locator = self.page.locator(locator_value)
        elif locator_type == "xpath":
            locator = self.page.locator(f"xpath={locator_value}")
        elif locator_type == "text":
            locator = self.page.get_by_text(locator_value)
        elif locator_type == "placeholder":
            locator = self.page.get_by_placeholder(locator_value)
        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")
        try:
            await locator.wait_for(state="visible", timeout=timeout * 1000)
        except Exception:
            raise TimeoutError(f"Element '{locator_key}' not visible after {timeout} seconds")

    async def wait_for_seconds(self, seconds):
        """
        Pauses the execution for the specified number of seconds (async).
        Args:
            seconds (int/float): The number of seconds to wait
        """
        await asyncio.sleep(seconds)
        text_print(f"Waited for {seconds} seconds", "green")
