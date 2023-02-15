from digitalio import DigitalInOut, Direction, Pull

class Switch():
    '''
    VEX Bumper or Limit Switch

    :param ~microcontroller.pin switch_pin: Input to read when a switch is pressed
    '''

    def __init__(
        self,
        switch_pin
    ):
        '''
        Initialize the Switch Object
        '''
        self._switch = DigitalInOut(switch_pin)
        self._switch.direction = Direction.INPUT
        self._switch.pull = Pull.UP

    def pressed(self) -> bool:
        if not self._switch.value:
            return True
        else:
            return False
