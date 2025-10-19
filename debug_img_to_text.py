import cv2
import paddleocr

image = cv2.imread('debug_career_detect.png')

engine = paddleocr.PaddleOCR(lang='en')

text = engine.ocr(image)

print(text)