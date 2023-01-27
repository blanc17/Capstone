from pyaxidraw import axidraw   # import module
ad = axidraw.AxiDraw()          # Initialize class
ad.interactive()                # Enter interactive context
if not ad.connect():            # Open serial port to AxiDraw;
    quit()                      #   Exit, if no connection.
ad.moveto(1, 1)                 # Pen-up move to (1, 1) inch
ad.options.units = 1            # set working units to cm.
ad.options.speed_pendown = 10   # set pen-down speed to 10%
ad.update()                     # Process changes to options 
ad.move(5.08, 5.08)             # Relative move: (2, 2) inches
ad.moveto(0,0)                  # Pen-up move, back to origin.
ad.disconnect()                 # Close serial port to AxiDraw
