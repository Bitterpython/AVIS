import time
import Adafruit_PCA9685

pwm = None

# Update these channels if your hardware uses different PCA9685 outputs.
PAN_CHANNEL = 0
TILT_CHANNEL = 1
PWM_FREQUENCY = 50
MIN_PULSE = 150
MAX_PULSE = 600
DEFAULT_ANGLE = 90.0


def _init_pwm(address: int = 0x40, busnum: int | None = 1) -> None:
    global pwm
    if pwm is not None:
        return

    if busnum is not None:
        pwm = Adafruit_PCA9685.PCA9685(address=address, busnum=busnum)
    else:
        pwm = Adafruit_PCA9685.PCA9685(address=address)
    pwm.set_pwm_freq(PWM_FREQUENCY)


_servo_positions = {
    PAN_CHANNEL: DEFAULT_ANGLE,
    TILT_CHANNEL: DEFAULT_ANGLE,
}


def _angle_to_pwm(angle: float) -> int:
    """Convert an angle in degrees (0-180) to PCA9685 PWM ticks."""
    angle = max(0.0, min(180.0, angle))
    return int(MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE))


def _servo_channel(servo: str | int) -> int:
    """Resolve a servo identifier to a PCA9685 channel."""
    if isinstance(servo, str):
        normalized = servo.strip().lower()
        if normalized == "pan":
            return PAN_CHANNEL
        if normalized == "tilt":
            return TILT_CHANNEL
        raise ValueError("Servo must be 'pan' or 'tilt', not '%s'" % servo)

    if isinstance(servo, int):
        return servo

    raise TypeError("Servo identifier must be a string or integer")


def move_servo(servo: str | int, target_angle: float, step: float = 1.0, delay: float = 0.02) -> None:
    """Ease the requested servo to a target angle.

    Args:
        servo: 'pan' or 'tilt', or a PCA9685 channel index.
        target_angle: goal angle in degrees.
        step: degrees per intermediate move.
        delay: pause time between intermediate moves.
    """
    channel = _servo_channel(servo)
    target_angle = max(0.0, min(180.0, target_angle))

    current_angle = _servo_positions.get(channel, DEFAULT_ANGLE)
    if current_angle == target_angle:
        return

    _init_pwm(busnum=1)

    step_value = int(max(1.0, abs(step)))
    start = int(round(current_angle))
    end = int(round(target_angle))

    if start < end:
        angle_iter = range(start, end + 1, step_value)
    else:
        angle_iter = range(start, end - 1, -step_value)

    for angle in angle_iter:
        pwm.set_pwm(channel, 0, _angle_to_pwm(angle))
        time.sleep(delay)

    pwm.set_pwm(channel, 0, _angle_to_pwm(target_angle))
    _servo_positions[channel] = float(target_angle)


if __name__ == "__main__":
    # Test the servos locally with hardware connected.
    print("Initializing servo hardware...")
    _init_pwm(busnum=1)

    print("Moving pan to 30 degrees")
    move_servo("pan", 30)
    time.sleep(1)

    print("Moving pan to 160 degrees")
    move_servo("pan", 160)
    time.sleep(1)

    print("Moving tilt to 10 degrees")
    move_servo("tilt", 10)
    time.sleep(1)

    print("Moving tilt to 45 degrees")
    move_servo("tilt", 45)
    time.sleep(1)

    print("Hardware test finished.")

