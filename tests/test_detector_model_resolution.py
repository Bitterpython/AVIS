import os
import unittest

from core import detector


class DetectorModelResolutionTests(unittest.TestCase):
    def test_prefers_a_real_local_model_file(self):
        model_path = detector.resolve_model_path()

        self.assertTrue(os.path.exists(model_path), msg=f"Model path does not exist: {model_path}")
        self.assertTrue(model_path.endswith(".pt"), msg=f"Expected a PyTorch weights file, got: {model_path}")


if __name__ == "__main__":
    unittest.main()
