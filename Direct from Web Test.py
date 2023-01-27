from pyaxidraw import axidraw   # Import the module
ad = axidraw.AxiDraw()          # Create class instance
ad.plot_setup("C:\\Users\\Owner\\Documents\\Capstone\\fast test.svg")        # Load file & configure plot context
            # Plotting options can be set, here after plot_setup().
ad.options.pen_pos_up = 80
ad.plot_run()   

#pen_pos_down = 40 is very dainty, very light
#pen_pos_down = 25 is normal
