import pytesseract
import cv2
from PIL import Image


# Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_image(image_path):

    try:

        # Read image using OpenCV
        image = cv2.imread(image_path)


        if image is None:
            return "Image not found"


        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )


        # Resize image for better OCR
        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )


        # Remove noise
        gray = cv2.GaussianBlur(
            gray,
            (5,5),
            0
        )


        # Threshold
        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )


        # OCR extraction
        text = pytesseract.image_to_string(
            thresh,
            config="--psm 6"
        )


        return text.strip()


    except Exception as e:

        return f"OCR Error: {str(e)}"