from pyaxidraw import axidraw

def raise_pen(ad):
    ad.moveto(ad.current_pos()[0], ad.current_pos()[1])
    return

ad = axidraw.AxiDraw()
ad.interactive()
ad.options.pen_pos_down = 40

if not ad.connect():            # Open serial port to AxiDraw;
    quit()
ad.moveto(1, 1)                 # Pen-up move to (1 inch, 1 inch)
ad.lineto(2, 1)                 # Pen-down move, to (2 inch, 1 inch)

ad.options.pen_pos_down = 20
ad.update() ####MUST USE UPDATE!!!!!!!
raise_pen(ad) #must move pen back 
ad.lineto(2,3)

ad.moveto(0, 0)                 # Pen-up move, back to origin.
ad.disconnect()  

