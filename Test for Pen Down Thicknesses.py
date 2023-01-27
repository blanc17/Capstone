from pyaxidraw import axidraw

def raise_pen(ad):
    ad.moveto(ad.current_pos()[0], ad.current_pos()[1])
    return

ad = axidraw.AxiDraw()
ad.interactive()
ad.options.pen_pos_down = 10

if not ad.connect():            # Open serial port to AxiDraw;
    quit()

for x in range(1, 16):

    weight = x*5 + 5
    
    ad.options.pen_pos_down = weight
    ad.update()

    ad.moveto(x/2, 1)
    ad.lineto(x,2)

ad.moveto(0,0)
ad.disconnect()

