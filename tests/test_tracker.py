import unittest

from core.tracker import Tracker


class TrackerTests(unittest.TestCase):
    def test_falls_back_to_closest_bird_when_none_are_within_max_distance(self):
        tracker = Tracker()
        tracker.target = {"x": 100, "y": 100}

        birds = [
            {"x": 1000, "y": 1000},
            {"x": 900, "y": 900},
        ]

        target = tracker.track(birds, {"x": 900, "y": 500})

        self.assertIsNotNone(target)
        self.assertEqual(target["x"], 900)
        self.assertEqual(target["y"], 900)

    def test_returns_none_when_no_birds_are_detected(self):
        tracker = Tracker()

        target = tracker.track([], {"x": 900, "y": 500})

        self.assertIsNone(target)

    def test_keeps_previous_target_during_a_short_detection_gap(self):
        tracker = Tracker()
        tracker.target = {"x": 100, "y": 100, "confidence": 0.95}

        target = tracker.track([], {"x": 900, "y": 500})

        self.assertIsNotNone(target)
        self.assertEqual(target["x"], 100)
        self.assertEqual(target["y"], 100)


if __name__ == "__main__":
    unittest.main()
