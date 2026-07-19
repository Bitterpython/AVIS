from ultralytics import YOLO
import cv2

class BirdDetector:
    def __init__(self):
        self.model = YOLO("models/best.pt")
        self.resolution = {"x": 900, "y": 500}
        self.confidence_threshold = 0.6
        self.bird_class_ids = self._resolve_bird_class_ids()

    def _initialize(self):
        self.confidence_threshold = 0.6
        self.bird_class_ids = self._resolve_bird_class_ids()

    def _resolve_bird_class_ids(self):
        names = getattr(self.model, "names", {}) or {}
        if not names:
            return {0}

        bird_ids = {
            class_id
            for class_id, name in names.items()
            if isinstance(name, str) and "bird" in name.lower()
        }

        if bird_ids:
            return bird_ids

        return {0}

    def detect(self, frame):
        if frame is None:
            return []

        if not hasattr(self, "confidence_threshold"):
            self._initialize()

        frame_proc = cv2.GaussianBlur(frame, (3, 3), 0)

        results = self.model(frame_proc)[0]

        birds = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if conf < self.confidence_threshold:
                continue

            if cls not in self.bird_class_ids:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            width = max(1, x2 - x1)
            height = max(1, y2 - y1)

            birds.append(
                {
                    "x": cx,
                    "y": cy,
                    "width": width,
                    "height": height,
                    "confidence": conf,
                    "distance": None,
                }
            )

        return birds