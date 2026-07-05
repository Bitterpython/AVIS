from core.detector import BirdDetector
from core.tracker import Tracker
from core.camera import Camera
from core.visuals import Visuals

import cv2

# frame = cv2.imread("test.png")

camera = Camera()
detector = BirdDetector()
tracker = Tracker()
visuals = Visuals()

while True:
    frame = camera.get_frame()

    if frame is None:
        break

    frame = cv2.resize(frame, (detector.resolution["x"], detector.resolution["y"]))
    
    frame_size = detector.resolution

    birds = detector.detect(frame)

    best_bird = tracker.track(birds, frame_size)
    
    visuals.draw_birds(frame, birds)
    visuals.draw_target(frame, best_bird)
    visuals.draw_center(frame, frame_size)
    
    print(best_bird)
    
    cv2.imshow("vogelerkennung", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()