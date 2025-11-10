import time
from fastOCR import fast_ocr_simple
from safeOCR import AccurateOCRResult

def main():
  all_img_paths = ["./samples/page-14.png", "./samples/second_test.jpg", "./samples/test_3.jpg", "./samples/test_4.jpg", "./samples/test_5.jpg"]
  start_time = time.time()
  for img_path in all_img_paths:
      fast_ocr_simple(img_path)
  end_time = time.time()
  print(f"Fast OCR took {end_time - start_time} seconds")
  start_time = time.time()
  accurate_ocr = AccurateOCRResult()
  for img_path in all_img_paths:
      accurate_ocr.accurate_ocr_simple(img_path)
  end_time = time.time()
  print(f"Accurate OCR took {end_time - start_time} seconds")
if __name__ == "__main__":
    main()