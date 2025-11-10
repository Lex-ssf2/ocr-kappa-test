import time
from fastOCR import fast_ocr_simple
from safeOCR import AccurateOCRResult
from menu import MenuApp
     
def main():
    app = MenuApp()
    app.showMainMenu()
    app.mainloop()
    """
    start_time = time.time()
    for img_path in app.getAllImgPaths():
        fast_ocr_simple(img_path)
    end_time = time.time()
    print(f"Fast OCR took {end_time - start_time} seconds")
    start_time = time.time()
    accurate_ocr = AccurateOCRResult()
    for img_path in app.getAllImgPaths():
        accurate_ocr.accurate_ocr_simple(img_path)
    end_time = time.time()
    print(f"Accurate OCR took {end_time - start_time} seconds")
    """
if __name__ == "__main__":
     main()