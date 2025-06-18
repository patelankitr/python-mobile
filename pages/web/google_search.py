from pathlib import Path
from framework.web.element import Element
from framework.readers.fileReader import FileReader

class GoogleSearch:

    def __init__(self, page):
        self.page = page
        self._json_file_path = str(Path(__file__).parent /"google_search.json")
        self.element = Element(self._json_file_path, self.page)

    def click_store_from_the_menu(self):
        print("\nSetting up test...")
        self.element.click_element('store_link')
