import time
from fastOCR import fast_ocr_simple
from safeOCR import AccurateOCRResult
import tkinter as tk
from tkinter import filedialog
import os

def main():

  root = tk.Tk()
  root.withdraw() 
  file_format = [
      ("Images", "*.png *.jpg *.jpeg *.tif *.tiff"),
      ("PNG Images", "*.png"),
      ("JPEG Images", "*.jpg *.jpeg")
  ]
  ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de imagen para OCR",
        initialdir=os.getcwd(),
        filetypes=file_format
    )
  
  all_img_paths = [ruta_archivo]
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