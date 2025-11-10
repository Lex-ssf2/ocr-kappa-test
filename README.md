# OCR Kappa Test
## Requeriments

[Python](https://www.python.org/)
[Tesseract](https://github.com/tesseract-ocr/tesseract?tab=readme-ov-file#installing-tesseract)
[Pytesseract](https://pypi.org/project/pytesseract/)
[OpenCV](https://pypi.org/project/opencv-python/#installation-and-usage)
[PaddleOCR](https://pypi.org/project/paddleocr/2.4/)
[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Installing dependencies
### Tesseract

```
sudo apt update
sudo apt install tesseract-ocr
```

### Pytesseract
```
- In case to be needed also install the language that you are looking for 
pip install pytesseract
```

### OpenCV
```
- Doesnt need the UI
pip install opencv-python-headless
```

### PaddleOCR

```
- No GPU
pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install "paddleocr>=2.0.1"
```

### Custom TKinter
```
pip install customtkinter
```