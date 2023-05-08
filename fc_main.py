import time
from fluxcapacitor import FluxCapacitor
from jump_button import JumpButton
from hardware import hardware

button_pin = hardware['button_pin']
button_pixel_pin = hardware['button_pixel_pin']
fc = FluxCapacitor(hardware['flow_pin'], hardware['flow_pixel_order'])
last_jumped_forward = True

while True:
    jumpbutton.update()
    fc.update()
    time.sleep(.01)
