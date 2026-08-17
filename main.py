from core.detector import BirdDetector
from core.tracker import Tracker
#from core.camera import Camera
from core.test_cam import Camera
from core.visuals import Visuals
from core.servo import Servo
from core.hardware_manager import Hardware

import cv2

# frame = cv2.imread("test.png")

camera = Camera()
detector = BirdDetector()
tracker = Tracker()
visuals = Visuals()
servo = Servo()
hardware = Hardware()

frame_count = 0

while True:
    frame = camera.get_frame()

    if frame is None:
        break

    frame = cv2.resize(frame, (detector.resolution["x"], detector.resolution["y"]))
    
    frame_size = detector.resolution

    if frame_count % 30 == 0:
        birds = detector.detect(frame)

    best_bird = tracker.track(birds, frame_size)
    
    visuals.draw_birds(frame, birds)
    visuals.draw_target(frame, best_bird)
    visuals.draw_center(frame, frame_size)
    
    if best_bird is not None:
        angles = servo.calculateAngles(detector.resolution["x"], detector.resolution["y"], best_bird)
        hardware.move_servo("pan", angles["pan"])
        hardware.move_servo("tilt", angles["tilt"])
        hardware.shoot()
        print(angles)
        
    
    print(best_bird)
    frame_count += 1
    
    cv2.imshow("vogelerkennung", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()