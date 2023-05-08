import neopixel
import adafruit_led_animation.animation.chase as chase

class FluxFlow:
    def __init__(self, pin, colour=(255, 255, 255, 255), pixel_order=neopixel.RGBW, idle_speed=85, idle_brightness=0.15):
        self.to_the_future = True
        self.pixels = neopixel.NeoPixel(pin, 10, auto_write=False, pixel_order=pixel_order, brightness=idle_brightness)
        self.idle_speed = idle_speed
        self.idle_brightness = idle_brightness
        self.animation = chase.Chase(self.pixels, speed=self._normalise_speed(idle_speed), color=colour, size=4, spacing=1)
        self.start()

    # Converts a speed value from 0-100 to a value between 0.01 and 0.5, inverted
    def _normalise_speed(self, speed):
        return (0.5 - 0.49 * (speed / 100))
    
    def start(self):
        self.animation.animate()
    
    def update(self):
        self.animation.animate()
        self.pixels.show()

    def set_fluxflow_idle(self):
        self.setSpeed(self.idle_speed)
        self.setBrightness(self.idle_brightness)        

    def setTimeDirection(self, to_the_future):
        self.to_the_future = to_the_future
        self.animation.reverse = not to_the_future
    
    def setSpeed(self, speed):
        self.animation.speed = self._normalise_speed(speed)

    def setBrightness(self, brightness):
        self.pixels.brightness = brightness
        self.pixels.show()

    def fillAll(self):
        self.pixels.fill(self.animation.color)
        self.pixels.show()

    def setColour(self, colour):
        self.animation.color = colour
