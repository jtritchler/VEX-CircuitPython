import time
import rotaryio
import pwmio
from adafruit_motor import servo

FORWARD = "FORWARD"
REVERSE = "REVERSE"


class Drivetrain:
    """
    Drivetrain for VEX robot to mimic VEXcode VR robot function to drive and turn

    :param ~microcontroller.pin l_motor_pin: Output that causes left motor to spin
    :param ~microcontroller.pin r_motor_pin: Output that causes right motor to spin
    :param ~microcontroller.pin l_enc_a_pin: Input A to read left motor rotation
    :param ~microcontroller.pin l_enc_b_pin: Input B to read left motor rotation
    :param ~microcontroller.pin r_enc_a_pin: Input A to read right motor rotation
    :param ~microcontroller.pin r_enc_b_pin: Input B to read right motor rotation
    :param int wheel_diameter: Diameter of the drivetrain wheels
    :param float angular_speed_factor: Factor used to speed up (>1.0) or slow down
    (<1.0) the left motor to maintain the same speed as the right motor
    in millimeters
    """

    def __init__(
        self,
        l_motor_pin,
        r_motor_pin,
        l_enc_a_pin,
        l_enc_b_pin,
        r_enc_a_pin,
        r_enc_b_pin,
        wheel_diameter,
        angular_speed_factor,
    ):
        """
        Initialize the DriveTrain Object
        """

        # Initialize left motor object
        l_pwm = pwmio.PWMOut(l_motor_pin, frequency=50)
        self._l_motor = servo.ContinuousServo(l_pwm)

        # Initialize right motor object
        r_pwm = pwmio.PWMOut(r_motor_pin, frequency=50)
        self._r_motor = servo.ContinuousServo(r_pwm)

        # Initialize the left encoder object
        self._l_encoder = rotaryio.IncrementalEncoder(l_enc_a_pin, l_enc_b_pin)

        # Initialize the right encoder object
        self._r_encoder = rotaryio.IncrementalEncoder(r_enc_a_pin, r_enc_b_pin)

        # Initialize the wheel diameter
        self._wheel_diameter = wheel_diameter

        # Initialize the drive and turn velocities
        self._drive_velocity = 0.5
        self._turn_velocity = 0.5
        self._vel_factor = 2

        # Initialize the width of the robot from left wheel to right wheel
        # in millimeters
        self._bot_width = 440

        # Initialize the angular speed factor between the left and right motors
        self._angular_speed_factor = angular_speed_factor

    @property
    def l_encoder_position(self) -> int:
        """
        Left motor encoder position.
        """
        return self._l_encoder.position

    @property
    def r_encoder_position(self) -> int:
        """
        Right motor encoder position.
        """
        return self._r_encoder.position

    @property
    def drive_velocity(self) -> float:
        """
        Driving motor speed, ranging from 0.0 (stopped) to 1.0 (full speed).
        """
        return self._drive_velocity

    def set_drive_velocity(self, velocity):
        """
        Sets the velocity of the Drivetrain.

        :param float velocity: The velocity from 0.0 to 1.0
        """
        velocity = min(velocity, 1.0)
        velocity = max(velocity, 0.0)
        self._drive_velocity = velocity

    @property
    def turn_velocity(self) -> float:
        """
        Turning motor velocity, ranging from 0.0 (stopped) to 1.0 (full velocity).
        """
        return self._turn_velocity

    def set_turn_velocity(self, velocity) -> None:
        """
        Sets the velocity of the Drivetrain's turns.

        :param float velocity: The velocity from 0.0 to 1.0
        """
        velocity = min(velocity, 1.0)
        velocity = max(velocity, 0.0)
        self._turn_velocity = velocity

    def drive(self, direction) -> None:
        """
        Moves the Drivetrain forever in the direction specified inside the parenthesis.

        :param str direction: Direction to drive, which may be "FORWARD" or "REVERSE"
        """
        if direction == "REVERSE":
            self._l_motor.throttle = (
                self._drive_velocity * self._angular_speed_factor / self._vel_factor
            )
            self._r_motor.throttle = -1 * self._drive_velocity / self._vel_factor
        else:
            self._l_motor.throttle = (
                -1
                * self._drive_velocity
                * self._angular_speed_factor
                / self._vel_factor
            )
            self._r_motor.throttle = self._drive_velocity / self._vel_factor

    def stop(self) -> None:
        """
        Stops the Drivetrain.
        """
        self._l_motor.throttle = 0.0
        self._r_motor.throttle = 0.0

    def drive_for(self, direction, distance) -> None:
        """
        Moves the Drivetrain for a given distance.

        :param str direction: Direction to drive, which may be "FORWARD" or "REVERSE"
        :param int distance: Distance to drive in millimeters.
        """
        if direction == "REVERSE":
            # Calculate the final the encoder position if traveling reverse
            l_end_position = self._l_encoder.position - distance * 180 / (
                self._wheel_diameter * 3.14159
            )
            r_end_position = self._r_encoder.position - distance * 180 / (
                self._wheel_diameter * 3.14159
            )

            # Decrement the encoder until the drivetrain travels the specified distance
            while (
                self._l_encoder.position > l_end_position
                or self._r_encoder.position > r_end_position
            ):
                if self._l_encoder.position - self._r_encoder.position < -10:
                    self._l_motor.throttle = self._l_motor.throttle * 0.9
                    self._r_motor.throttle = -1 * self._drive_velocity / self._vel_factor
                elif self._l_encoder.position - self._r_encoder.position > 10:
                    self._l_motor.throttle = (
                        self._drive_velocity * self._angular_speed_factor / self._vel_factor
                    )
                    self._r_motor.throttle = self._r_motor.throttle * 0.9
                else:
                    self._l_motor.throttle = (
                        self._drive_velocity * self._angular_speed_factor / self._vel_factor
                    )
                    self._r_motor.throttle = -1 * self._drive_velocity / self._vel_factor
                time.sleep(0.05)
        else:
            # Calculate the final the encoder position if traveling forward
            l_end_position = self._l_encoder.position + distance * 180 / (
                self._wheel_diameter * 3.14159
            )
            r_end_position = self._r_encoder.position + distance * 180 / (
                self._wheel_diameter * 3.14159
            )

            # Increment the encoder until the drivetrain travels the specified distance
            while (
                self._l_encoder.position < l_end_position
                or self._r_encoder.position < r_end_position
            ):
                if self._l_encoder.position - self._r_encoder.position < -10:
                    self._l_motor.throttle = (
                        -1 * self._drive_velocity * self._angular_speed_factor / self._vel_factor
                    )
                    self._r_motor.throttle = self._r_motor.throttle * 0.9
                elif self._l_encoder.position - self._r_encoder.position > 10:
                    self._l_motor.throttle = self._l_motor.throttle * 0.9
                    self._r_motor.throttle = self._drive_velocity / self._vel_factor
                else:
                    self._l_motor.throttle = (
                        -1 * self._drive_velocity * self._angular_speed_factor / self._vel_factor
                    )
                    self._r_motor.throttle = self._drive_velocity / self._vel_factor
                time.sleep(0.05)

        self.stop()

    def turn_for(self, direction, angle):
        """
        Turns the Drivetrain to a specific angle of rotation.

        :param str direction: The direction of rotation, which may be "RIGHT" or "LEFT"
        :param int angle: The angle of rotation in degrees
        """

        # Calculate the arc length to travel for the specified angle
        arc_length = self._bot_width * angle / 360

        if direction == "RIGHT":

            # Calculate the final the encoder positions if turning right
            l_end_position = self._l_encoder.position + arc_length * 180 / (
                self._wheel_diameter * 3.14159
            )
            r_end_position = self._r_encoder.position - arc_length * 180 / (
                self._wheel_diameter * 3.14159
            )

            # Activate the drivetrain until it turns the specified angle
            while (
                self._l_encoder.position < l_end_position
                or self._r_encoder.position > r_end_position
            ):
                self._l_motor.throttle = -1 * self._drive_velocity / self._vel_factor
                self._r_motor.throttle = -1 * self._drive_velocity / self._vel_factor
                time.sleep(0.05)
        else:

            # Calculate the final the encoder positions if turning left
            l_end_position = self._l_encoder.position - arc_length * 180 / (
                self._wheel_diameter * 3.14159
            )
            r_end_position = self._r_encoder.position + arc_length * 180 / (
                self._wheel_diameter * 3.14159
            )

            # Increment the encoder until the drivetrain travels the specified distance
            while (
                self._l_encoder.position > l_end_position
                or self._r_encoder.position < r_end_position
            ):
                self._l_motor.throttle = self._drive_velocity / self._vel_factor
                self._r_motor.throttle = self._drive_velocity / self._vel_factor
                time.sleep(0.05)
        self.stop()
