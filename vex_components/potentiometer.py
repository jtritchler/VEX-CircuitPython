from analogio import AnalogIn

class Potentiometer():
    '''
    VEX Potentiometer to read analog input

    :param ~microcontroller.pin potentiometer_pin: Input to read the value from a
    potentiometer
    '''

    def __init__(
        self,
        potentiometer_pin
    ):
        '''
        Initialize the Bumper Object
        '''
        self._potentiometer = AnalogIn(potentiometer_pin)

    @property
    def value(self) -> bool:
        return self._potentiometer.value
