###############################################################
# Rocket libs
#
# Send default commands to rocket launcher USB with usb.core
# You need also
###############################################################

import usb.core
import time
import random

# Default time step for movements
TIME_STEP = 0.05

# Actions byte codes
MOVEMENTS = {
    'right': [0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00],
    'left' : [0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00],
    'up'   : [0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00],
    'down' : [0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00],
    'stop' : [0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00],
    'fire' : [0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00]
}

class TuguuRocketLib:
    """
        Initializes rocket launcher USB and set a default
        target position (front in the middle). After that,
        you can send different instruction to play & fight!
    """
    dev = None

    def __init__(self, time_step = TIME_STEP):
        "Initializes rocket launcher with a default position"
        self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        self.duration = time_step
        if self.dev is None:
            raise ValueError('Launcher not found.')
        if self.dev.is_kernel_driver_active(0) is True:
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()
        self.set_default_target()

    def action(self, direction, duration=None):
        "Execute an action an wait for movement sync correlation"
        self.dev.ctrl_transfer(0x21,0x09,0,0, MOVEMENTS[direction])
        if direction not in ['stop', 'fire']:
            if not duration:
                duration = self.duration
            time.sleep(duration)
            self.dev.ctrl_transfer(0x21,0x09,0,0, MOVEMENTS['stop'])
        time.sleep(0.15)

    def set_default_target(self):
        "Set rocket launcher in his default position: front in the middle"
        # Initial to the left down
        self.action('right', 10)
        self.action('down', 4)
        # Set default target
        for i in range(7):
            self.action('up', 0.05)
        for i in range(28):
            self.action('left', 0.05)

    def lotery(self):
        "10% of the time will shoot them up"
        if random.random() < 0.1:
            self.action('right', random.randrange(800)/100.0)
            self.action('up', random.randrange(200)/100.0)
            self.action('down', random.randrange(200)/100.0)
            print "Fire!"
            for i in range(4):
                time.sleep(2)
                self.action('fire')
            self.set_default_target()

    def dummy(self):
        "Dummy movement from left to right, with a random shoot chance"
        self.action('left', 2)
        time.sleep(2)
        while True:
            self.lotery()
            for i in range(2):
                self.action('right', 1.8)
                time.sleep(0.5)
            for i in range(2):
                self.action('left', 2)
                time.sleep(0.5)


if __name__ == '__main__':
    # A dummy example
    tuguu_rocket = TuguuRocketLib()
    tuguu_rocket.dummy()
