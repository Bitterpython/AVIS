import cv2
from ultralytics import YOLO

# 1. Import SAHI modules
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction


class BirdDetector:

    def __init__(self):
        # We need the underlying YOLO instance to fetch class names
        self.raw_yolo_model = YOLO("models/yolo11m_ncnn_model")  # Load the NCNN model for class name resolution

        # 2. Wrap the YOLO model into a SAHI AutoDetectionModel instance
        self.model = AutoDetectionModel.from_pretrained(
            model_type="ultralytics",
            model_path="models/yolo11m_ncnn_model",  # Path to the exported NCNN model
            device="cpu",  # Forces stable floating point accuracy on Raspberry Pi 5
            confidence_threshold=0.10,  # SAHI-level pre-filter threshold
        )

        self.resolution = {"x": 1920, "y": 1080}
        self.confidence_threshold = 0.4
        self.bird_class_ids = self._resolve_bird_class_ids()

    def _initialize(self):
        self.confidence_threshold = 0.4
        self.bird_class_ids = self._resolve_bird_class_ids()

    def _resolve_bird_class_ids(self):
        # Reference the raw_yolo_model to safely fetch names string attributes
        names = getattr(self.raw_yolo_model, "names", {}) or {}
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

        # 3. Replace traditional predict with SAHI Slicing Pipeline
        # We use 640x640 window slices with a 20% overlap matrix
        sahi_output = get_sliced_prediction(
            frame_proc,
            self.model,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.20,
            overlap_width_ratio=0.20,
            perform_standard_pred=False,  # Stops downsampling layout to protect small pixels
            verbose=0,  # Silences background log spamming during loops
        )

        birds = []

        # 4. Parse SAHI Object Prediction types back into your custom dictionary format
        for prediction in sahi_output.object_prediction_list:
            cls = int(prediction.category.id)
            conf = float(prediction.score.value)

            if conf < self.confidence_threshold:
                continue

            if cls not in self.bird_class_ids:
                continue

            # SAHI exposes bounding box tracking natively as [xmin, ymin, xmax, ymax]
            x1, y1, x2, y2 = map(int, prediction.bbox.to_xyxy())

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
