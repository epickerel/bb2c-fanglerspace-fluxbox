# BB2C Fanglerspace Flux Capacitor Display

Code for a circuitpython-compatible microcontroller to drive a flux-capacitor-like display
with hooks for a colour-changing jump button. Designed for the BB2C Makerspace in Marietta, OH.

## Maker advice

If you're in the space and want to experiment, you should feel free to break and re-make it! This
art belongs to all fanglers[^1] present.

## Hardware

Presently, the board used for this project is an [https://learn.adafruit.com/adafruit-qt-py-2040](Adafruit QT-Py RP2040).
The pins used are A0, A1 and A2. A3 remains available for an additional device via the dangling
gray jumper wire. This board was chosen for the combination of its diminutive size and substantial power.
A replacement to this board should at least meet the present specs, but offer additional pins for input/output
and possibly bluetooth/wifi capabilities.

Pin assignment is done in `hardware.py`.

The "flow" bars are [https://www.amazon.com/gp/product/B09MLTPS95](144/m Neopixels), and are addressed via a shared data line
so that their animations are mirrored. The power requirements are greater than what a small microcontroller can provide, so
an external 5v power supply is connected (it shares a ground with the microcontroller to complete the data circuit).

The jump button is an [https://www.adafruit.com/product/4190](Adafruit triangle pushbutton) modified with a
[https://www.adafruit.com/product/1734](diffused through-hole Neopixel LED). And if you have ideas for a good housing for a
button this astoundingly chunky, please have at it! The button itself requires two pins: one for the button
functionality and one for its neopixel. Note the dangling blue wire: that is the neopixel data line, and you can connect more
pixels to the end of that!

## Code

This uses [https://circuitpython.org/](Circuitpython), which offers a fun and simple way to code
for supported microcontrollers. If you're just getting started, [https://codewith.mu/](Mu Editor) is
the tool you'll want to interact wit the board from your laptop.

Circuitpython boards automatically load `code.py`. In our case, this file simply imports (and runs)
the actual main code, which in this case is `fc_main.py`. A great way to experiment on the board and
easily revert back is to load a different `*_main.py` file from `code.py`.

The main code initialises the class FluxCapacitor, which connects to the devices which trigger and
display a "time travel" event and the idle time between. Its `travel()` method contains a script of
effect events; this is a great place to play around with different effects.

[^1]: “And in this doleful mood he ventured to wonder if they ever thought back to when things were just old-fangled or not fangled at all as against the modern day when fangled had reached its apogee. Fangling was indeed, he thought, here to stay. Then he wondered: had anyone ever thought of themselves as a fangler?” ― Terry Pratchett, Raising Steam

## Libraries

Some [https://circuitpython.org/libraries](Circuitpython libraries) are required for this, and should be placed in the `/lib` directory
on the board. These include:

- asyncio
- neopixel
- adafruit_led_animation
- adafruit_debouncer

One additional library is required: [https://cognitivegears.github.io/CircuitPython_Schedule/](circuitpython_schedule).
