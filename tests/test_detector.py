import unittest

import numpy as np

from core.detector import BirdDetector


class FakeBox:
    def __init__(self, cls_id, conf, xyxy):
        self.cls = [cls_id]
        self.conf = [conf]
        self.xyxy = [xyxy]


class FakeResults:
    def __init__(self, boxes):
        self.boxes = boxes


class FakeModel:
    def __init__(self):
        self.names = {0: "bird"}

    def __call__(self, frame):
        return [FakeResults([FakeBox(0, 0.95, [10, 20, 80, 90])])]


class DetectorTests(unittest.TestCase):
    def test_detects_bird_boxes_when_model_reports_bird_class(self):
        detector = BirdDetector.__new__(BirdDetector)
        detector.model = FakeModel()
        detector.BIRD_CLASS_ID = 14
        detector.resolution = {"x": 640, "y": 480}

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        birds = detector.detect(frame)

        self.assertEqual(len(birds), 1)
        self.assertEqual(birds[0]["x"], 45)
        self.assertEqual(birds[0]["y"], 55)


if __name__ == "__main__":
    unittest.main()
