from ultralytics import YOLO
import cv2

class BirdDetector:
    def __init__(self):
        self.model = YOLO("models/yolov8n.pt")
        
        self.BIRD_CLASS_ID = 14
        
        self.resolution = {
            "x": 900,
            "y": 500
        }
        
    def detect(self, frame):
        frame_proc = cv2.GaussianBlur(frame, (3, 3), 0)

        results = self.model(frame_proc)[0]

        birds = []
        
        for box in results.boxes:
            bird = {
                "x": 100,
                "y": 100,
                "width": 100,
                "height": 100,
                "confidence": 0.91,
                "distance": 100
            }
            
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == self.BIRD_CLASS_ID:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                
                width = x2 - x1
                height = y2 - y1

                bird["x"] = cx
                bird["y"] = cy
                bird["width"] = width
                bird["height"] = height
                bird["confidence"] = conf
                
                birds.append(bird)
            
        return(birds)        