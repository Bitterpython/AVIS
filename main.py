from core.detector import BirdDetector
from core.tracker import Tracker
from core.camera import Camera
import cv2

# frame = cv2.imread("test.png")

camera = Camera()
detector = BirdDetector()
tracker = Tracker()

while True:
    frame = camera.get_frame()
    cv2.imshow("vogelerkennung", frame)

    frame_size = detector.resolution

    birds = detector.detect(frame)

    best_bird = tracker.track(birds, frame_size)

    print(best_bird)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()