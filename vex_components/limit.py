from digitalio import DigitalInOut, Direction, Pull

class LimitSwitch():
    '''
    VEX Limit Switch 

    :param ~microcontroller.pin limit_pin: Input to read when a limit switch is
    pressed
    '''

    def __init__(
        self,
        limit_pin
    ):
        '''
        Initialize the Bumper Object
        '''
        self.btn = DigitalInOut(limit_pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP


    @property
    def pressed(self) -> bool:
        if not self.btn.value:
            return True
        else:
            return False