from ultralytics import YOLO
import cv2

class BirdDetector:
    def __init__(self):
        print("loaded model")
        self.model = YOLO("models/yolov8n.pt")
        
        self.BIRD_CLASS_ID = 14

    def detect(self, frame):
        frame = cv2.resize(frame, (900, 500))

        frame_proc = cv2.GaussianBlur(frame, (3, 3), 0)

        results = self.model(frame_proc)[0]

        birds = []
        
        for box in results.boxes:
            bird = {
                "x": 100,
                "y": 100,
                "confidence": 0.91
            }
            
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == self.BIRD_CLASS_ID:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                bird["x"] = cx
                bird["y"] = cy
                bird["confidence"] = conf
                
                birds.append(bird)
            
        return(birds)        