from pages.click_page import ClickPage

def test_click_button(page):
    page.goto("https://example.com")  # Replace with real or mock page with "Click Me"
    click_page = ClickPage(page)
    click_page.click_button()
    # Optional: assert something changes after the click
