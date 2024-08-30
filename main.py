import cv2
import pytesseract

# If you are using Windows, set the tesseract executable path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_license_plate(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply some pre-processing to improve OCR accuracy
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Denoising
    edged = cv2.Canny(gray, 30, 200)              # Edge detection

    # Find contours based on edges detected
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    license_plate = None

    for contour in contours:
        # Approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)

        # If the contour has 4 vertices, it could be a license plate
        if len(approx) == 4:
            license_plate = approx
            break

    if license_plate is None:
        print("License plate not found")
        return None

    # Masking the part other than the license plate
    mask = cv2.drawContours(image, [license_plate], -1, (0, 255, 0), 3)
    cv2.imshow("License Plate", mask)

    # Cropping the region of interest (ROI)
    x, y, w, h = cv2.boundingRect(license_plate)
    roi = gray[y:y + h, x:x + w]

    # Use Tesseract to extract text from the ROI
    text = pytesseract.image_to_string(roi, config='--psm 8')
    print("Detected license plate Number is:", text.strip())

    # Display the image with detected contours
    cv2.imshow("Image with Detected License Plate", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return text.strip()

# Example usage:
image_path = 'img/img2.jpeg'
plate_number = detect_license_plate(image_path)
