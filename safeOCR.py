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
        result = self.ocr.predict(image_path)

        # how many texts detected
        max_len = len(result[0]["rec_scores"])

        # Raw Data Output
        """
        for i in range(max_len):
            print(f"Texto: {result[0]['rec_texts'][i]}, Score: {result[0]['rec_scores'][i]}")
            print(f"Box: {result[0]['rec_boxes'][i]}")
        """
        result[0].save_to_img(save_path="./output/")
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