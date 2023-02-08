import time
import board
from bumper import Bumper

left_bumper = Bumper(board.D2)

while True:

    if left_bumper.pressed():
        print('pressed')
    else:
        continue

    time.sleep(0.05)
