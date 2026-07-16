import cv2

try:
    from picamzero import Camera as PiCameraZero
except ImportError:  # pragma: no cover - runtime fallback
    PiCameraZero = None


class Camera:
    def __init__(self):
        self._picam = None
        self._cap = None

        if PiCameraZero is not None:
            try:
                self._picam = PiCameraZero()
            except Exception as exc:  # pragma: no cover - depends on hardware
                print(f"PicamZero init failed, falling back to webcam/video: {exc}")

        if self._picam is None:
            self._cap = cv2.VideoCapture(0)
            if not self._cap.isOpened():
                self._cap = cv2.VideoCapture("/home/avis/AVIS/video1.mp4")

    def get_frame(self):
        if self._picam is not None:
            frame = self._picam.capture_array()
            if frame is None:
                return None
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if self._cap is not None:
            ret, frame = self._cap.read()
            if not ret:
                return None
            return frame

        return None

    def release(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None