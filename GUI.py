import tkinter as tk
from pyaxidraw import axidraw
from tkinter.filedialog import askopenfilename, asksaveasfilename
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
import Drawing as dc

#global variables
file_name = ''
draw = dc.Drawing()

#Definition for getting the svg file
def get_svg(file):

    drawing = svg2rlg(file)
    renderPM.drawToFile(drawing, "temp.png", fmt="PNG")

    return

#Definition for making a new file
def new_file():

    canvas = tk.Canvas(frm_canvas, bg='white', width=736, height=900)
    canvas.grid(row=0, column=0, sticky='nesw')

    return

#Definition for opening a file
def open_file():

    global file_name
    
    #open the file picking box
    file_name = askopenfilename(
        filetypes = [
            ("Scalable Vector Graphics", ".svg"),
            ("Images", "*.png *.img *.bmp *.jpeg"),
            ("All files", "*.*")
            ]
        )

    temp_img = file_name
    
    #if .svg, save as image an then print
    if ".svg" in file_name:
        get_svg(file_name)
        temp_img = "temp.png"

    #print the image
    img = Image.open(temp_img)
    pimg = ImageTk.PhotoImage(img)
    label = tk.Label(frm_canvas, image=pimg)
    label.image = pimg
    label.grid(row=0, column=0, sticky='nesw')
    w.update()
    #frame = tk.Canvas(frm_canvas, width=size[0], height=size[1])
    #frame.pack()
    #frame.create_image(0, 0, anchor='nw',image=pimg)
    #print(file_name)

    return

#Definition for saving a file
def save_file():

    print(file_name)


    return

#Definition for plotting a file
def plot_file():

    global file_name

    print(file_name)

    ad = axidraw.AxiDraw()          # Create class instance
    #ad.interactive()                # Enter interactive context
    #if not ad.connect():            # Open serial port to AxiDraw;
    #    quit()   
    ad.plot_setup(file_name)        # Load file & configure plot context
            # Plotting options can be set, here after plot_setup().
    #ad.options.report_time = True
    #ad.options.preview = True
    ad.plot_run()

    #ad.disconnect()    

    return

#ALL PEN COMMANDS
def using_pen():

    global draw
    draw.medium = 'pen'

    return

def using_eraser():

    global draw
    draw.medium = 'eraser'

    return

def using_circle():

    global draw
    draw.medium = 'circle'

    return

def using_rectangle():

    global draw
    draw.medium = 'rectangle'

    return

def using_edit():

    global draw
    draw.medium = 'edit'

    return

#-----------------------------------------------------------------------
#GUI

#WINDOW
#make the initial display window
w = tk.Tk()
#format the window so the width and height are full screen
width = w.winfo_screenwidth()
height = w.winfo_screenwidth()
w.geometry("%dx%d" % (width, height))
#add a title
w.title("AxiDraw Assist")
#configure rows and columns
w.rowconfigure(0, minsize=20, weight=1)
w.columnconfigure(0, minsize=5, weight=1)

#MENU
#make the initial menu
menu = tk.Menu()
#file button
file_m = tk.Menu(menu, tearoff=0)
#add functions under the file button
file_m.add_command(label="New", command=new_file)
file_m.add_command(label="Open", command=open_file)
file_m.add_command(label="Save", command=save_file)
#add the file button to the menu
menu.add_cascade(label="File", menu=file_m)
#add the menu to the window
w.config(menu=menu)

#MAIN FRAME
#add a frame to contain the other frames
frm_main = tk.Frame(w)
#configure the frame rows and columns
frm_main.columnconfigure(0, weight=1)
frm_main.rowconfigure(0, weight=0)
frm_main.rowconfigure(1, weight=1)
frm_main.rowconfigure(2, weight=0)
#add to the window
frm_main.grid(row=0, column=0, sticky='nesw')

#TOOLS FRAME (frame for buttons regarding painting
frm_tools = tk.Frame(frm_main)
#configure with buttons
#pen button (right click for types of lines)
btn_pen = tk.Button(master=frm_tools, text="Pen", command = using_pen)
btn_pen.grid(row=0, column=0, sticky='ne')
#eraser button
btn_eraser = tk.Button(master=frm_tools, text="Eraser", command = using_eraser)
btn_eraser.grid(row=0, column=1, sticky='ne')
#circle button
btn_circle = tk.Button(master=frm_tools, text="Circle", command = using_circle)
btn_circle.grid(row=0, column=2, sticky='ne')
#square button
btn_rectangle = tk.Button(master=frm_tools, text="Rectangle", command = using_rectangle)
btn_rectangle.grid(row=0, column=3, sticky='ne')
#edit button
btn_edit = tk.Button(master=frm_tools, text="Edit", command = using_edit)
btn_edit.grid(row=0, column=4, sticky='ne')

#add to main frame
frm_tools.grid(row=0, column=0, sticky='nesw')

#CANVAS FRAME
frm_canvas = tk.Frame(frm_main)
#configure with a canvas

#add to main frame
frm_canvas.grid(row=1, column=0, sticky='nesw')

#PRINT FRAME
frm_print = tk.Frame(frm_main)
#configure with buttons for printing
#PRINT BUTTON
btn_print = tk.Button(master=frm_print, text='Plot', command = plot_file)
btn_print.grid(row=0, column=0, sticky='nesw')
#add to main frame
frm_print.grid(row=2, column=0, sticky='nesw')

#-----------------------------------------------------------------------

#make the program run
w.mainloop()
