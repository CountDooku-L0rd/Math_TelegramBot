import os
import cv2
import base64
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY")

def preprocess_image(image_bytes: bytes) -> bytes:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    success, encoded_image = cv2.imencode(".jpg", image)
    if not success:
        raise ValueError("Ошибка при кодировании изображения")
    return encoded_image.tobytes()

def image_to_latex(image_bytes: bytes) -> str:
    processed_image = preprocess_image(image_bytes)
    headers = {
        "app_id": MATHPIX_APP_ID,
        "app_key": MATHPIX_APP_KEY,
        "Content-Type": "application/json"
    }

    img_str = base64.b64encode(processed_image).decode()

    data = {
        "src": f"data:image/jpeg;base64,{img_str}",
        "formats": ["latex_styled"],
        "ocr": ["math", "text"]
    }

    res = requests.post("https://api.mathpix.com/v3/text", headers=headers, json=data)
    res.raise_for_status()

    return res.json().get("latex_styled", "")

