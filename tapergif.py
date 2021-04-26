# convert -delay 15 -loop 0 out/*.png -delay 1000 $(FINAL_FRAME) -strip -coalesce -layers Optimize out/$(GIF)
#

import itertools
import sys

cmd = ["convert", "-loop", "0"]

START_DELAY = 50
END_DELAY = 10
DELTA_DELAY = 2

delays = itertools.chain(
    itertools.repeat(START_DELAY, 5),
    range(START_DELAY, END_DELAY, -DELTA_DELAY),
    itertools.repeat(END_DELAY)
)

lastdelay = -1
for delay, png in zip(delays, sys.argv[2:]):
    if delay != lastdelay:
        cmd.extend(["-delay", str(delay)])
        lastdelay = delay
    cmd.extend([png])

cmd.extend(["-delay", "2000", sys.argv[-1]])
cmd.extend(["-strip", "-coalesce", "-layers", "Optimize", sys.argv[1]])
print(" ".join(cmd))
