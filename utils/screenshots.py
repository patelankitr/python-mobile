from PIL import Image, ImageDraw
import io
import os
from datetime import datetime

def highlight_element(driver, element, label="tap"):
    location = element.location
    size = element.size

    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))

    draw = ImageDraw.Draw(image)
    draw.rectangle(
        [location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"]],
        outline="red", width=5
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{label}_{timestamp}.png"
    os.makedirs("screenshots", exist_ok=True)
    image.save(filename)
    print(f"📸 Highlighted screenshot saved to {filename}")
