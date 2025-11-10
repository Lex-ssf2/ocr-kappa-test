import cv2
import pytesseract
from pytesseract import Output
from PIL import Image

# This script is to keep all the tesseract related methods

"""
Attributes
----------
imagen_cv2 : vec2 image
    The image to be processed.
angle : int
    The angle to rotate the image (in degrees).
Returns
----------
rotatedImg : vec2 image
    The rotated image.
"""
def rotate_img(imagen_cv2, angle):
    if angle == 0:
        return imagen_cv2

    (height, width) = imagen_cv2.shape[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedImg = cv2.warpAffine(imagen_cv2, M, (width, height))

    return rotatedImg

"""
Attributes
----------
image_path : str
    The path to the image to be processed.
Returns
----------
best_result : str
    The recognized text from the image.
best_angle : int
    The angle at which the best OCR result was obtained.
"""
def fast_ocr_simple(image_path):
  all_angles = [0, 90, 180, 270]
  best_case = -1
  best_result = ""
  best_angle = 0
  actual_img = None

  img = cv2.imread(image_path)
  for angle in all_angles:
    # preprocess the image
    rotatedImg = rotate_img(img, angle)
    gray = cv2.cvtColor(rotatedImg, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    threshold_img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # gets OCR data
    datos_ocr = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # only consider confidence > 50%
    valid_cases = [conf for conf in datos_ocr['conf'] if conf > 50]    
    if valid_cases:
        all_cases = sum(valid_cases)
        # Compares with the current best case
        if all_cases > best_case:
            best_case = all_cases
            best_angle = angle
            actual_img = threshold_img

  # saves the best image and prints the result
  # Mode 6 is to assume a single uniform block of text which what mostly receipts are
  config_final = r'-l fra+eng+es --psm 6'
  best_result = pytesseract.image_to_string(actual_img, config=config_final)
  print(f"Best angle: {best_angle}")
  print(best_result)
  return best_result,best_angle