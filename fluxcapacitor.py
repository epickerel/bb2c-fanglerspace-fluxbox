import time
import asyncio
# Note: schedule was used in an early version of this for convenience. It should be retired at some point in favour of asyncio.
import circuitpython_schedule as schedule
from fluxflow import FluxFlow

OLD_LACE = (253, 245, 230)

class asyncrange:
    class __asyncrange:
        def __init__(self, *args):
            self.__iter_range = iter(range(*args))

        async def __anext__(self):
            try:
                return next(self.__iter_range)           
            except StopIteration as e:
                raise StopAsyncIteration(str(e))

    def __init__(self, *args):
        self.__args = args

    def __aiter__(self):
        return self.__asyncrange(*self.__args)

class FluxCapacitor:
    def __init__(self, flow_pin, flow_pixel_order, jumpbutton=None, buzzer=None, idleColour=OLD_LACE, periodic_jump_interval=300):
        self.travelling = False
        self._last_travelled_direction_forward = True
        self._fluxflow = FluxFlow(flow_pin, idleColour, flow_pixel_order)
        self._buzzer1 = buzzer
        self._jumpbutton = jumpbutton
        self._idleColour = idleColour
        self._periodic_jump_interval = periodic_jump_interval
        if (self._jumpbutton):
            self._jumpbutton.onPress = self.make_a_jump
        self.schedule_periodic_jump()

    def schedule_periodic_jump(self):
        self._periodic_jump_task = schedule.every(self._periodic_jump_interval).seconds.do(self.periodic_jump)

    def periodic_jump(self):
        print("Periodic jump")
        self.make_a_jump(self._idleColour)

    def make_a_jump(self, color=None, unpause=None):
        if (color):
            self._fluxflow.setColour(color)
        years = -30 if self._last_travelled_direction_forward else 30
        asyncio.run(self.travel(years))
        if (unpause):
            unpause()

    # The years param is mostly a placeholder; for now, only the positive or negative sign is used to determine the direction of travel
    async def travel(self, years):
        # Pause the periodic jump so that the interval restarts after the jump
        schedule.cancel_job(self._periodic_jump_task)
        if self.travelling:
            return;
        print("Travelling " + str(years) + " years")
        self.travelling = True
        self._last_travelled_direction_forward = years > 0
        self._fluxflow.setTimeDirection(self._last_travelled_direction_forward)

        # This emulates the speed ramp-up before travel commences
        duration = 12 # seconds
        sleep = 0.02
        steps = int(duration / sleep)
        async for i in asyncrange(0, steps):
            proportion = i / steps
            self._fluxflow.setSpeed(proportion * 99.9)
            self._fluxflow.setBrightness(proportion)
            self._fluxflow.update()
            await asyncio.sleep(sleep)
        print("Initial travel complete")

        # Flash three times
        self._fluxflow.fillAll()
        space_between_flashes = 0.3
        self._fluxflow.setBrightness(0)
        await asyncio.sleep(space_between_flashes)
        print("First flash")
        self._fluxflow.setBrightness(100)
        await asyncio.sleep(space_between_flashes)
        self._fluxflow.setBrightness(0)
        await asyncio.sleep(space_between_flashes)
        self._fluxflow.setBrightness(100)
        await asyncio.sleep(space_between_flashes)
        self._fluxflow.setBrightness(0)
        await asyncio.sleep(space_between_flashes)
        self._fluxflow.setBrightness(100)
        await asyncio.sleep(2)

        # Pause for a bit
        self._fluxflow.setBrightness(0)
        await asyncio.sleep(2)

        # Go back into idle, in the present colour
        self._fluxflow.set_fluxflow_idle()    
        self.travelling = False
        self.schedule_periodic_jump()

    def update(self):
        schedule.run_pending()
        if not self.travelling:
            self._fluxflow.update()
