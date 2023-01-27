from pyaxidraw import axidraw   # import module
ad = axidraw.AxiDraw()          # Initialize class
ad.interactive()                # Enter interactive context
if not ad.connect():            # Open serial port to AxiDraw;
    quit()                      #   Exit, if no connection.

ad.options.units = 0
ad.interactive()

                                # Absolute moves follow:
ad.moveto(1, 1)                 # Pen-up move to (1 inch, 1 inch)
ad.lineto(2, 1)                 # Pen-down move, to (2 inch, 1 inch)
ad.lineto(2,3)
ad.moveto(2,3)
ad.options.pen_pos_down = 20 #Test negative positions
ad.lineto(1,3)
ad.moveto(1,3)
ad.options.pen_pos_down = 100
ad.lineto(1,1)
ad.moveto(0, 0)                 # Pen-up move, back to origin.
ad.disconnect()                 # Close serial port to AxiDraw

#from pyaxidraw import axidraw   # Import the module
#ad = axidraw.AxiDraw()          # Create class instance
#ad.plot_setup("C:\\Users\\Owner\\Documents\\Capstone\\drawing.svg")        # Load file & configure plot context
            # Plotting options can be set, here after plot_setup().
#ad.options.report_time = True
#ad.options.preview = True
#ad.plot_run()   
#print(ad.time_estimate)
