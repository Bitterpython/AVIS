class Servo:
    def __init__(self, invert_pan=True, invert_tilt=True):
        self.horizontal_fov = 62.2
        self.vertical_fov = 48.8
        self.current_pan = 90
        self.current_tilt = 90
        self.invert_pan = invert_pan
        self.invert_tilt = invert_tilt

    def setAngles(self, pan, tilt):
        self.current_pan = pan
        self.current_tilt = tilt

    def set_inversion(self, invert_pan=None, invert_tilt=None):
        if invert_pan is not None:
            self.invert_pan = invert_pan
        if invert_tilt is not None:
            self.invert_tilt = invert_tilt

    def calculateAngles(self, width, height, target):
        center = {
            "x": width / 2,
            "y": height / 2
        }

        nx = (target["x"] - center["x"]) / center["x"]
        ny = (target["y"] - center["y"]) / center["y"]

        pan_offset = nx * (self.horizontal_fov / 2)
        tilt_offset = ny * (self.vertical_fov / 2)

        if self.invert_pan:
            pan_offset *= -1
        if self.invert_tilt:
            tilt_offset *= -1

        pan = self.current_pan + pan_offset
        tilt = self.current_tilt - tilt_offset

        angles = {
            "pan": int(pan),
            "tilt": int(tilt)
        }

        return angles