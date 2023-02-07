from digitalio import DigitalInOut, Direction, Pull

class Bumper():
    '''
    VEX Bumper Switch

    :param ~microcontroller.pin bumper_pin: Input to read when a bumper switch is
    pressed
    '''

    def __init__(
        self,
        bumper_pin
    ):
        '''
        Initialize the Bumper Object
        '''
        self.btn = DigitalInOut(bumper_pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP


    @property
    def pressed(self) -> bool:
        if not self.btn.value:
            return True
        else:
            return False