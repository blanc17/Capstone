import sys

from pyaxidraw import axidraw

ad = axidraw.AxiDraw() # Initialize class

ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw

if not connected:
    sys.exit() # end script

ad.usb_command('S2,3,24000,6\r')

# version = ad.usb_query('S2,3,65535\r')

ad.disconnect()