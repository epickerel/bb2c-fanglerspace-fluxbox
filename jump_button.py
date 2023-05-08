import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer
from rainbowio import colorwheel
import neopixel

class JumpButton:
    def __init__(self, btnPin, pixelPin) -> None:
        self.pixel = neopixel.NeoPixel(pixelPin, 1, auto_write=True, pixel_order=neopixel.RGBW, brightness=0.5)
        btn = DigitalInOut(btnPin)
        btn.direction = Direction.INPUT
        btn.pull = Pull.UP
        self._btn = btn
        self._switch = Debouncer(btn)
        self._wheelpos = 0
        self._wheelpos_last_update = time.monotonic()
        self.paused = False

    def update_wheelpos(self):
        self._wheelpos = self._wheelpos + 1 if self._wheelpos < 254 else 0
        self._wheelpos_last_update = time.monotonic()
        self.pixel.fill(colorwheel(self._wheelpos))

    def unpause(self):
        self.paused = False

    def _pressed(self):
        if (self.onPress):
            self.paused = True
            self.onPress(colorwheel(self._wheelpos), self.unpause)

    def update(self):
        if (self.paused):
            return
        if (time.monotonic() - self._wheelpos_last_update > .05):
            self.update_wheelpos()
        self._switch.update()
        if (self._switch.rose) :
            self._pressed()
