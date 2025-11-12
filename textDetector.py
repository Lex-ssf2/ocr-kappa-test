import os
import cv2
import numpy as np
import pytesseract

class textOrientationDetection:
    def __init__(self):
        self.frontIMG = 0
        self.flippedIMG = 0
        self.allSideWaysImg = 0
        self.smallCuts = []

    def reset(self):
        self.frontIMG = 0
        self.flippedIMG = 0
        self.allSideWaysImg = 0
        self.smallCuts = []

    def detect_textBox(self, ruta_imagen):
        self.reset()
        self.allSideWaysImg = 0
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            print("Error: Could not load image.")
            return None

        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gris, (7, 7), 0)
        threshold = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        output = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        mser = cv2.MSER_create()
        mser.setMinArea(100)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        imgDilated = cv2.dilate(threshold, kernel, iterations=1)

        imgEdges = cv2.Canny(imgDilated, 127, 255)

        contours, _ = cv2.findContours(imgEdges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        imgRect = imagen.copy()

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(imgRect, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite('output_detected_text.png', imgRect)
        cv2.imwrite('output_threshold.png', threshold)
        cv2.imwrite('output_dilated.png', imgDilated)
        cv2.imwrite('output_edges.png', imgEdges)
        for i, cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            isSideWays = h > w

            if w < 15 or h < 15:
                continue
            recorte = output[y:y+h, x:x+w]
            if isSideWays:
                self.allSideWaysImg += 1
            whitePixels = cv2.countNonZero(recorte)
            ratio = whitePixels / recorte.size if recorte.size > 0 else 0
            if ratio < 0.2 or ratio > 0.6:
                continue
            self.smallCuts.append((w, h, recorte, isSideWays, i))
            # detect if folder exist if it doesnt make it
            if not os.path.exists('output'):
                os.makedirs('output')
            if not os.path.exists(f'output/{ruta_imagen.split("/")[-1].split(".")[0]}'):
                os.makedirs(f'output/{ruta_imagen.split("/")[-1].split(".")[0]}')
            cv2.imwrite(f'output/{ruta_imagen.split("/")[-1].split(".")[0]}/recorte_{i}.png', recorte)

    def detect_orientation(self):
        isVerticalText = self.allSideWaysImg / len(self.smallCuts) > 0.4
        whitelist_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        config_whitelist = r'--psm 8 -c tessedit_char_whitelist=' + whitelist_chars
        for i, (w, h, recorte, isSideWays, name) in enumerate(self.smallCuts):
            #print(f"Recorte {name}: Blancos: {whitePixels}, Negros: {blackPixels}, Ratio: {ratio:.2f}, Size: {recorte.shape}")
            imgData = {"top": {"white": 0, "points": 0},
                "bottom": {"white": 0, "points": 0}}
            actual_h = h
            if isVerticalText:
                actual_h = w
                recorte = cv2.rotate(recorte, cv2.ROTATE_90_CLOCKWISE)
            """
            topImage = recorte[:int(actual_h/2), :]
            bottomImage = recorte[int(actual_h/2):, :]
            maxWhiteRow = 0
            """

            # Check vertical difference by projecting onto the vertical axis from up to down
            for col in range(recorte.shape[1]):
                columnHasWhite = False
                blackCount = 0
                for row in range(recorte.shape[0]):
                    currentPixel = recorte[row, col]
                    if currentPixel == 0:
                        blackCount += 1
                    else:
                        columnHasWhite = True
                        break
                if columnHasWhite:
                    imgData["top"]["points"] += blackCount
                    
            # Check vertical difference by projecting onto the vertical axis from down to up
            for col in range(recorte.shape[1]):
                columnHasWhite = False
                blackCount = 0
                for row in range(recorte.shape[0]-1, -1, -1):
                    currentPixel = recorte[row, col]
                    if currentPixel == 0:
                        blackCount += 1
                    else:
                        columnHasWhite = True
                        break
                if columnHasWhite:
                    imgData["bottom"]["points"] += blackCount
            confirmed = True
            if imgData['top']['points']/max(imgData['bottom']['points'], 1) > 1.5 or imgData['top']['points']/max(imgData['bottom']['points'], 1) < 0.6:
                data = pytesseract.image_to_data(recorte, output_type=pytesseract.Output.DICT, config=config_whitelist)
                for i in range(len(data['level'])): 
                    if data['level'][i] == 5 and data['conf'][i] < 60:
                        confirmed = False
                        break
                
            if imgData["top"]["points"] > imgData["bottom"]["points"]:
                if confirmed:
                    self.frontIMG += 1
                else:
                    self.flippedIMG += 1
                    # recorte = cv2.rotate(recorte, cv2.ROTATE_180)
            elif imgData["top"]["points"] < imgData["bottom"]["points"]:
                if confirmed:
                    self.flippedIMG += 1
                    # recorte = cv2.rotate(recorte, cv2.ROTATE_180)
                else:
                    self.frontIMG += 1
            print(f"Recorte {name} ratio: {imgData['top']['points']/max(imgData['bottom']['points'], 1)}, confirmed: {confirmed}")
            """
            check horizontal difference
            for row in range(bottomImage.shape[0]//2):
                previousPixel = 0
                whiteCount = 0
                for col in range(bottomImage.shape[1]):
                    currentPixel = bottomImage[row, col]
                    imgData["bottom"]["white"] += 1
                    if (currentPixel == previousPixel) and currentPixel > 0:
                        whiteCount += 1
                    previousPixel = bottomImage[row, col]
                maxWhiteRow = max(maxWhiteRow, whiteCount)
            imgData["bottom"]["points"] = maxWhiteRow
            maxWhiteRow = 0
            for row in range(topImage.shape[0]//2):
                previousPixel = 0
                whiteCount = 0
                for col in range(topImage.shape[1]):
                    currentPixel = topImage[row, col]
                    imgData["top"]["white"] += 1
                    if (currentPixel == previousPixel) and currentPixel > 0:
                        whiteCount += 1
                    previousPixel = topImage[row, col]
                maxWhiteRow = max(maxWhiteRow, whiteCount)
            imgData["top"]["points"] = maxWhiteRow
            if(imgData["top"]["points"] > imgData["bottom"]["points"]):
            recorte = cv2.rotate(recorte, cv2.ROTATE_180)
            flippedIMG += 1
            elif(imgData["top"]["white"] >= imgData["bottom"]["white"] and imgData["top"]["points"] == imgData["bottom"]["points"]):
            recorte = cv2.rotate(recorte, cv2.ROTATE_180)
            flippedIMG += 1
            else:
            frontIMG += 1
            #print(f"Points Top: {imgData['top']['points']}, Points bottom: {imgData['bottom']['points']}")
            """

        if (isVerticalText):
            if self.flippedIMG > self.frontIMG:
                print("Image is rotated to the right")
                return 90
            else:
                print("Image is rotated to the left")
                return 270
        else:
            if self.flippedIMG < self.frontIMG:
                print("Image is normal")
                return 0
            else:
                print("Image is upside down")
                return 180