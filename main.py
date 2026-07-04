from core.detector import BirdDetector
import cv2

frame = cv2.imread("test.png")

detector = BirdDetector()

birds = detector.detect(frame)

print(birds)