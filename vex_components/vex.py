from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from rotaryio import IncrementalEncoder
from pwmio import PWMOut
from adafruit_motor import servo
from adafruit_hcsr04 import HCSR04

class Switch():
    '''Reads the input from a VEX Bumper Switch or Limit Switch.

    :param switch_pin: Input to read when a switch is pressed.
    :type switch_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, switch_pin) -> None:
        '''Constructor method.   
        '''
        # Initialize the digital input
        self._switch = DigitalInOut(switch_pin)
        self._switch.direction = Direction.INPUT
        self._switch.pull = Pull.UP

    def pressed(self) -> bool:
        '''Returns whether the switch is pressed.

        :return: `True` if switch is pressed, `False` otherwise.
        :rtype: bool
        '''
        return not self._switch.value

class Led():
    '''Controls a single color LED.

    :param led_pin: Output to turn on and off the LED.
    :type led_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, led_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the digital output for the LED
        self._led = DigitalInOut(led_pin)
        self._led.direction = Direction.OUTPUT

    def turn_on(self) -> None:
        '''Turns on the LED.
        '''
        self._led.value = True

    def turn_off(self) -> None:
        '''Turns off the LED.
        '''
        self._led.value = False

    def toggle(self) -> None:
        '''Toggles the LED.  If the LED is on, then turns it off.  If the LED is off,
        then turns it on.
        '''
        self._led.value = not self._led.value

    def is_on(self) -> bool:
        '''Returns whether the LED is on.

        :return: `True` if LED is on, `False` otherwise.
        :rtype: bool
        '''
        return self._led.value

class Potentiometer():
    '''Reads the input from a VEX Potentiometer.

    :param pot_pin: Input to read the potentiometer value.
    :type pot_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, pot_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the analog input for the potentiometer
        self._potentiometer = AnalogIn(pot_pin)

    def value(self) -> int:
        '''Returns the value of the potentiometer between 0 and 65535 inclusive
        (16-bit).

        :return: Integer value between 0 and 65535 inclusive.
        :rtype: int
        '''
        return self._potentiometer.value

class Encoder():
    '''Reads the input from a VEX Encoder.

    :param pin_a: First pin to read pulses from.
    :type pin_a: class:`microcontroller.Pin`
    :param pin_b: Second pin to read pulses from.
    :type pin_b: class:`microcontroller.Pin`
    '''

    def __init__(self, pin_a, pin_b) -> None:
        '''Constructor method.
        '''
        # Initialize the incremental encoder
        self._encoder = IncrementalEncoder(pin_a, pin_b, divisor=1)

    def position(self) -> int:
        '''Returns the integer value of the current position in terms of pulses.

        :return: Integer value of the current position.
        :rtype: int
        '''
        return self._encoder.position

class Servo():
    '''Controls a VEX Servo to rotate between 0 and 180 degrees inclusive.

    
    :param servo_pin: Output pin to control the servo.
    :type servo_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, servo_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the pulse width modulation object
        pwm = PWMOut(servo_pin, duty_cycle=2 ** 15, frequency=50)
        # Initialize the servo
        self._servo = servo.Servo(pwm)

    def get_angle(self) -> int:
        '''Returns the angle of the servo in degrees.

        :return: Angle of the servo between 0 and 180 inclusive.
        :rtype: int
        '''
        return int(round(self._servo.angle, 0))

    def set_angle(self, angle) -> None:
        '''Sets the angle of the servo in degrees.

        :param angle: Angle to set the servo in degrees between 0 and 180 inclusive.
        :type angle: int
        '''
        # Limit the angle range to be between 0 and 180 degrees inclusive.
        angle = max(angle, 0)
        angle = min(angle, 180)
        self._servo.angle = angle

class Motor():
    '''Controls a VEX Motor via a Motor Controller.

    :param motor_pin: Output pin to motor controller.
    :type motor_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, motor_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the pulse width modulation object
        pwm = PWMOut(motor_pin, duty_cycle=2 ** 15, frequency=50)
        # Initialize the servo
        self._motor = servo.ContinuousServo(pwm)

    def get_throttle(self) -> float:
        '''Returns the throttle of the motor between -1.0 and 1.0 inclusive.

        :return: Throttle between -1.0 and 1.0 inclusive.
        :rtype: float
        '''
        return self._motor.throttle * 2

    def set_throttle(self, throttle) -> None:
        '''Sets the throttle of the motor between -1.0 and 1.0 inclusive.

        :param throttle: Throttle of the motor between -1.0 and 1.0 inclusive.
        :type throttle: int
        '''
        # Limit the throttle range to be between -1.0 and 1.0 inclusive.
        throttle = max(throttle, -1.0)
        throttle = min(throttle, 1.0)
        self._motor.throttle = throttle / 2

class Ultrasonic():
    '''Reads the input distance in mm from a VEX Ultrasonic Range Module.

    :param input_pin: Input pin to trigger the sound wave.
    :type input_pin: class:`microcontroller.Pin`
    :param output_pin: Output pin to send the echo distance.
    :type output_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, input_pin, output_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the ultrasonic sensor
        self._sonar = HCSR04(input_pin, output_pin)

    def distance(self) -> int:
        '''Returns the distance to an object from the sensor.

        :return: Integer distance measured by the sensor in mm.
        :rtype: int
        '''
        # Try to read the distance from the sensor
        try:
            dist = self._sonar.distance * 10
        # Set the distance to -1 if the sensor cannot be read
        except RuntimeError:
            dist = -1
        # Return the distance in mm
        return int(round(dist))

class LineTracker():
    '''Reads the input from a VEX Line Tracker.

    :param track_pin: Input to read the line tracker value.
    :type track_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, track_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the analog input for the potentiometer
        self._line_tracker = AnalogIn(track_pin)

    def value(self) -> int:
        '''Returns the value of the line tracker between 0 and 65535 inclusive
        (16-bit).

        :return: Integer value between 0 and 65535 inclusive.
        :rtype: int
        '''
        return self._line_tracker.value

class LightSensor():
    '''Reads the input from a VEX Light Sensor.

    :param light_pin: Input to read the light sensor value.
    :type light_pin: class:`microcontroller.Pin`
    '''

    def __init__(self, light_pin) -> None:
        '''Constructor method.
        '''
        # Initialize the analog input for the potentiometer
        self._light = AnalogIn(light_pin)

    def value(self) -> int:
        '''Returns the value of the light sensor between 0 and 65535 inclusive
        (16-bit).

        :return: Integer value between 0 and 65535 inclusive.
        :rtype: int
        '''
        return self._light.value
