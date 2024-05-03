import pytesseract
from PIL import Image

from metrics import Analytics


def preprocess_image_for_ocr(original):
    Analytics.timeStart("preprocess_image")
    # Convert to grayscale first
    gray_scale_image = original.convert("L")  # "L" mode is for grayscale

    # Apply binary threshold
    binary_image = gray_scale_image.point(
        lambda p: 255 if p > 180 else 0, "1"
    )  # '1' mode is for binary (black and white)

    Analytics.timeEnd("preprocess_image")

    return binary_image


def image_to_byte_array(image: Image) -> bytes:
    import io

    byte_io = io.BytesIO()
    image.save(byte_io, format="TIFF")
    return byte_io.getvalue()


def extract_numbers_from_image(image):
    preprocessed = preprocess_image_for_ocr(image)

    custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789/"
    text = pytesseract.image_to_string(preprocessed, config=custom_config)

    return text.strip()


def extract_text_from_image(image):
    preprocessed = preprocess_image_for_ocr(image)

    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(preprocessed, config=custom_config)

    return text.strip()
