import cv2
import pytesseract

# Load the image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def test_cv():
    image_path = "C:\\Users\\UNITY_105\\PycharmProjects\\PythonProject1\\images\\Actual_image\\full_screenshot.png"  # Change this to your image path
    image = cv2.imread(image_path)

    # Convert to grayscale (improves OCR accuracy)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Tesseract OCR with bounding box data
    custom_config = r'--oem 3 --psm 6'  # Use page segmentation mode 6 (Assumes a uniform block of text)
    data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)

    # Extract word-level information
    found = False
    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        if word.upper() == "POKER":  # Check for "POKER"
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            print(f"✅ 'POKER' found at coordinates: (x={x}, y={y}, width={w}, height={h})")
            found = True

            # Draw a bounding box around the detected text
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if not found:
        print("❌ 'POKER' not found in the image.")

    # Save the output image with bounding boxes
    output_path = "output_with_poker_box.png"
    cv2.imwrite(output_path, image)
    print(f"🔍 Result saved as: {output_path}")
