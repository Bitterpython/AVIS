import time
import json
import cv2
import numpy as np
import supervision as sv
from inference import get_model

MODEL_ID = "rfdetr-small"
CONFIDENCE = 0.35
FRAME_INTERVAL_SEC = 1.5

# Smaller slices improve tiny-bird recall, larger slices improve speed.
# Start here, then tune on the Pi.
SLICE_WH = (640, 640)

model = get_model(model_id=MODEL_ID)

def detect_birds_sahi(frame: np.ndarray):
    def callback(image_slice: np.ndarray) -> sv.Detections:
        result = model.infer(
            image_slice,
            confidence=CONFIDENCE,
            class_filter=["bird"],
            iou_threshold=0.3,
            max_detections=100,
        )[0]
        return sv.Detections.from_inference(result)

    slicer = sv.InferenceSlicer(
        callback=callback,
        slice_wh=SLICE_WH,
        overlap_filter=sv.OverlapFilter.NON_MAX_SUPPRESSION,
    )

    detections = slicer(frame)

    output = []
    for xyxy, confidence in zip(detections.xyxy, detections.confidence):
        x1, y1, x2, y2 = xyxy
        output.append({
            "x": float((x1 + x2) / 2),
            "y": float((y1 + y2) / 2),
            "width": float(x2 - x1),
            "height": float(y2 - y1),
            "confidence": float(confidence),
        })

    return output

cap = cv2.VideoCapture(0)

next_run = 0.0

while True:
    ok, frame = cap.read()
    if not ok:
        continue

    now = time.monotonic()
    if now < next_run:
        continue

    next_run = now + FRAME_INTERVAL_SEC

    birds = detect_birds_sahi(frame)
    print(json.dumps({
        "timestamp": time.time(),
        "birds": birds,
    }, indent=2))
