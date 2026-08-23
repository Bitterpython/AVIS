import time
import Adafruit_PCA9685

class Hardware:
    def __init__(self):
        self.pwm = None
        self.PAN_CHANNEL = 0
        self.TILT_CHANNEL = 1
        self.PWM_FREQUENCY = 50
        self.MIN_PULSE = 150
        self.MAX_PULSE = 600
        self.DEFAULT_ANGLE = 90.0
        self._servo_positions = {
            self.PAN_CHANNEL: self.DEFAULT_ANGLE,
            self.TILT_CHANNEL: self.DEFAULT_ANGLE,
        }

    def reset_servos(self):
        """Reset both pan and tilt servos to their default angles."""
        self.move_servo("pan", 45)
        self.move_servo("tilt", 45)
        self.move_servo("pan", self.DEFAULT_ANGLE)
        self.move_servo("tilt", self.DEFAULT_ANGLE)
    
    def _init_pwm(self, address: int = 0x40, busnum: int | None = 1) -> None:
        if self.pwm is not None:
            return

        if busnum is not None:
            self.pwm = Adafruit_PCA9685.PCA9685(address=address, busnum=busnum)
        else:
            self.pwm = Adafruit_PCA9685.PCA9685(address=address)

        self.pwm.set_pwm_freq(self.PWM_FREQUENCY)

    def _angle_to_pwm(self, angle: float) -> int:
        """Convert an angle in degrees (0-180) to PCA9685 PWM ticks."""
        angle = max(0.0, min(180.0, angle))
        return int(self.MIN_PULSE + (angle / 180.0) * (self.MAX_PULSE - self.MIN_PULSE))

    def _servo_channel(self, servo: str | int) -> int:
        """Resolve a servo identifier to a PCA9685 channel."""
        if isinstance(servo, str):
            normalized = servo.strip().lower()
            if normalized == "pan":
                return self.PAN_CHANNEL
            if normalized == "tilt":
                return self.TILT_CHANNEL
            raise ValueError("Servo must be 'pan' or 'tilt', not '%s'" % servo)

        if isinstance(servo, int):
            return servo

        raise TypeError("Servo identifier must be a string or integer")

    def move_servo(self, servo: str | int, target_angle: float, step: float = 1.0, delay: float = 0.02) -> None:
        """Ease the requested servo to a target angle."""
        channel = self._servo_channel(servo)
        target_angle = max(0.0, min(180.0, target_angle))

        current_angle = self._servo_positions.get(channel, self.DEFAULT_ANGLE)
        if current_angle == target_angle:
            return

        self._init_pwm(busnum=1)

        step_value = int(max(1.0, abs(step)))
        start = int(round(current_angle))
        end = int(round(target_angle))

        if start < end:
            angle_iter = range(start, end + 1, step_value)
        else:
            angle_iter = range(start, end - 1, -step_value)

        for angle in angle_iter:
            self.pwm.set_pwm(channel, 0, self._angle_to_pwm(angle))
            time.sleep(delay)

        self.pwm.set_pwm(channel, 0, self._angle_to_pwm(target_angle))
        self._servo_positions[channel] = float(target_angle)
        
    def shoot(self):
        print("shooting bird")

if __name__ == "__main__":
    # Test the servos locally with hardware connected.
    hardware = Hardware()

    print("Initializing servo hardware...")
    hardware._init_pwm(busnum=1)

    print("Moving pan to 30 degrees")
    hardware.move_servo("pan", 30)
    time.sleep(1)

    print("Moving pan to 160 degrees")
    hardware.move_servo("pan", 90)
    time.sleep(1)

    print("Moving tilt to 10 degrees")
    hardware.move_servo("tilt", 10)
    time.sleep(1)

    print("Moving tilt to 45 degrees")
    hardware.move_servo("tilt", 90)
    time.sleep(1)

    print("Hardware test finished.")