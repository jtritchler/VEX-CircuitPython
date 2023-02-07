import pwmio
from adafruit_motor import servo

class VEXMotor:
    '''
    VEX 393 Motor controller to set the speed and direction of the motor.

    :param ~microcontroller.pin motor_pin: Output that causes the motor to spin
    '''

    def __init__(
        self,
        motor_pin,
    ):
        '''
        Initialize the DriveTrain Object
        '''

        # Initialize left motor object
        pwm = pwmio.PWMOut(motor_pin, frequency=50)
        self._motor = servo.ContinuousServo(pwm)

        # Initialize the motor throttle
        self._throttle = 0.5

    @property
    def throttle(self) -> float:
        '''
        Driving motor speed, ranging from -1.0 (full speed reverse) to
        0.0 (stopped) to 1.0 (full speed).
        '''
        return self._throttle

    @throttle.setter
    def throttle(self, value: float) -> None:
        if value > 1.0 or value < -1.0:
            raise ValueError("Throttle must be between -1.0 and 1.0")
        if value is None:
            raise ValueError("Continuous servos cannot spin freely")
        self._throttle = value
