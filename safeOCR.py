from paddleocr import PaddleOCR
# This script is to keep all the paddle ocr related methods

"""
TODO: Verify if the image is valid before processing like corrupted images, etc.
"""

class AccurateOCRResult:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to load model into memory
        self.rec_texts = []
        self.rec_scores = []
        self.rec_boxes = []
        print("Accurate OCR model loaded successfully.")

    """
    Attributes
    ----------
    image_path : str
        Path to the image to be processed.
    Returns
    ----------
    rec_texts : list
        List of recognized texts from the image.
    rec_scores : list
        List of confidence scores for each recognized text.
    rec_boxes : list
        List of bounding boxes for each recognized text.
    """
    def accurate_ocr_simple(self, image_path):
        if not image_path:
            print("Error: No image path provided.")
            return
        result = self.ocr.predict(image_path)
        if not result or len(result) == 0:
            print(f"Error: No OCR results for image at {image_path}")
            return
        # how many texts detected
        max_len = len(result[0]["rec_scores"])

        # Raw Data Output
        output_string = ""

        for i in range(max_len):
            output_string += f"{result[0]['rec_texts'][i]}\n"
            """
            print(f"Texto: {result[0]['rec_texts'][i]}, Score: {result[0]['rec_scores'][i]}")
            print(f"Box: {result[0]['rec_boxes'][i]}")
            """
        # result[0].save_to_img(save_path="./output/")
        # save the output string to a text file
        output_txt_path = "./output/" + image_path.split("/")[-1].split(".")[0] + "_safeOCR.txt"
        with open(output_txt_path, "w", encoding="utf-8") as text_file:
            text_file.write(output_string)
        self.rec_texts = result[0]['rec_texts']
        self.rec_scores = result[0]['rec_scores']
        self.rec_boxes = result[0]['rec_boxes']
        return
    
    # Getter methods

    def getRecognizedTexts(self):
        return self.rec_texts

    def getRecognizedScores(self):
        return self.rec_scores

    def getRecognizedBoxes(self):
        return self.rec_boxes