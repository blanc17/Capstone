from PIL import Image, ImageTk, ImageGrab
from pyaxidraw import axidraw
import os
import re
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import time
import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
import webbrowser

#import sys
#from colorutils import Color

#change the recursion limit
#sys.setrecursionlimit(1000000)

#definition for getting the svg file
def get_svg(file:str):
    svg = svg2rlg(file)
    renderPM.drawToFile(svg, 'temp.png', fmt='PNG')

#class for GUI window
class windows(tk.Tk):
    #initialize
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #add a title
        self.wm_title('AxiDraw Assist')
        #resize the window
        self.wm_state('zoomed')

        #special variables
        self.medium = 'Pen'
        self.color = 'black'
        self.background = 'white'
        self.width = 1
        self.fill = tk.IntVar()
        self.file = ''
        self.bmp = ''
        self.svg = ''
        self.image = ''

        
        #creating a menu for the main window
        self.make_menu()

        #create a toolbar for the main window
        self.tools = {}
        self.make_toolbar()

        #create a large generic frame for the main window
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both',expand=True)
        self.canvas = Drawing(self.container, self)
        self.canvas.pack(side='top', fill='both',expand=True)

        #create a button for packing
        self.btn_plot = Draw_Button(self)
        self.btn_plot.pack(side='bottom', anchor='se')

    def reset_files(self):
        self.file = ''
        self.svg = ''
        self.image = ''

    def make_menu(self):
        
        menu = tk.Menu()

        #add a file button
        file = tk.Menu(menu, tearoff=0)
        for M in (New, Open, Save):
            M(file, self)
        menu.add_cascade(label='File', menu=file)

        #add edit button
        edit = tk.Menu(menu, tearoff=0)
        for M in (Undo, Redo):
            M(edit, self)
        menu.add_cascade(label='Edit', menu=edit)

        #add the menu to the window
        self.config(menu=menu)

    def make_toolbar(self):
        tools = tk.Frame(self)
        #for B in (Pen, Eraser, Circle, Rectangle, Edit, Color, Width):
        for B in (Pen, Eraser, Circle, Rectangle, Fill, Color, Width):
            button = B(tools,self)
            self.tools[B] = button
        tools.pack(anchor='n',fill='x')

    def set_medium(self, medium):
        self.medium = medium
        print(self.medium)

    def set_color(self):
        color = colorchooser.askcolor(title='Choose color')[1]
        self.color = "#" + color.partition("#")[2]

    def set_width(self, event:tk.Event, entry:tk.Entry):

        #remove letters
        num = re.sub("[^0-9]", "", entry.get())
        #set width
        if num == '' or num == '0':
            num = '1'
        self.width = int(num)
        #update entry
        entry.delete(0, tk.END)
        entry.insert(0, num)

    def draw_file(self):
        #if already a .svg file, print
        if '.svg' in self.file:
            ad = axidraw.AxiDraw()
            ad.plot_setup(self.file)
            ad.plot_run()

    def set_file(self):
        file = os.path.realpath(os.path.dirname(__file__)) + '/temp.png'
        #change the file name
        file = file.replace('\\', '/')

        #get the coordinate
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        #delay for one second
        time.sleep(1)
        #TODO: consider making an error pop-up for non-supported files (svg, img)
        ImageGrab.grab().crop((x, y, x1, y1)).save(file)
        self.file = file

    def set_bmp(self):
        file = os.path.realpath(os.path.dirname(__file__)) + '/temp.bmp'
        #change the file name
        file = file.replace('\\', '/')

        #get the coordinate
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        #delay for one second
        time.sleep(1)
        #TODO: consider making an error pop-up for non-supported files (svg, img)
        ImageGrab.grab().crop((x, y, x1, y1)).save(file)
        self.bmp = file
          
#Classes for file menu
class New():
    def __init__(self, button:tk.Menu, parent:windows):
        button.add_command(label='New', command= lambda:self.new_file(parent))
    def new_file(self, main:windows):
        main.container=Drawing(main)
        main.file = ''
class Open():
    def __init__(self, button:tk.Menu, parent:windows):
        button.add_command(label='Open', command=lambda:self.open_file(parent))
    def open_file(self, main:windows):

        #reset all of the files
        main.reset_files()

        #get the file 
        main.file = askopenfilename(
            filetypes=[
                ('Scalabale Vector Graphics', '*.svg'),
                ('Images', '*.png *.img *.bmp *.jpeg'),
                ('All Files', '*.*')
            ]
        )

        if not main.file:
            return

        #set the image
        if '.svg' in main.file:
            #if .svg, get the file and then set the image
            get_svg(main.file)
            main.svg = main.file
            main.image = 'temp.png'
        else:
            main.image = main.file
    
        #plot the image
        img = Image.open(main.image)
        pimg = ImageTk.PhotoImage(img)

        #with canvas
        main.canvas.create_image(0,0,anchor=tk.NW, image=pimg)
        main.canvas.image = pimg
class Save():
    def __init__(self, button:tk.Menu, parent:windows):
        button.add_command(label='Save', command=lambda:self.save_file(parent))
    def save_file(self, main:windows):
        # filename = os.path.realpath(os.path.dirname(__file__)) + '/temp.png'
        # #change the file name
        # filename = filename.replace('\\', '/')

        #get the file 
        file = asksaveasfilename(
            filetypes=[
                ('PNG', '*.png'),
                ('Bitmap', '*.bmp'),
                ('JPEG', '*.jpeg'),
                ('All Files', '*.*')
            ]
        )

        if not file:
            return
        print(file)

        #ATTEMPT USING IMAGEGRAB
        #IT WORKS
        x = main.canvas.winfo_rootx()
        y = main.canvas.winfo_rooty()
        x1 = x + main.canvas.winfo_width()
        y1 = y + main.canvas.winfo_height()

        #delay for one second
        time.sleep(1)
        #TODO: consider making an error pop-up for non-supported files (svg, img)
        ImageGrab.grab().crop((x, y, x1, y1)).save(file)
        #set the main file
        main.file = file

#Undo and redo for file
class Undo():
    def __init__(self, button:tk.Menu, parent:windows):
        button.add_command(label='Undo', command =lambda:self.undo_action(parent))
    def undo_action(self, parent:windows):
        if len(parent.canvas.shapes) > 0:
            #Get the last action and remove it from the list
            last_action = parent.canvas.shapes.pop(-1)

            #Make a copy of the last action and add it to the redo list
            parent.canvas.redo.append(last_action)

            #delete the image from the canvas
            for l in last_action.lines:
                parent.canvas.delete(l)
class Redo():
    def __init__(self, button:tk.Menu, parent:windows):
        button.add_command(label='Redo', command=lambda:self.redo_action(parent))
    def redo_action(self, parent:windows):
        if len(parent.canvas.redo) > 0:
            #get the last action and remove it from the list
            last_action = parent.canvas.redo.pop(-1)

            #make a copy of the last action and add it to the undo list
            parent.canvas.shapes.append(last_action)

            #add the image to the canvas
            #TODO: work it out so that all types of shapes can be added
            # if type(last_action) == Line:
            #     last_action.remake(parent.canvas)
            last_action.remake(parent.canvas)

#Class for canvas frame
class Drawing(tk.Canvas):
    def __init__(self, parent:tk.Frame, main:windows):
        tk.Canvas.__init__(self, parent)
        self.configure(bg=main.background)
        self.shapes = []
        self.redo = []
        self.bind('<Button-1>', lambda event: self.make_shape(event, main))
        self.bind('<B1-Motion>', lambda event: self.paint(event, main))
        self.bind('<ButtonRelease-1>',lambda event: self.end_shape(event, main))
        #self.bind('<Motion>',lambda event: self.get_color(event, main))
    
    def make_shape(self, event:tk.Event, main:windows):
        #delete redo list
        self.redo = []

        if main.medium == 'Pen':
            #If pen is selected, make a line
            line = Line()
            self.shapes.append(line)
            print(self.shapes)
        elif main.medium == 'Eraser':
            #If Eraser is seleceted, erase lines
            eraser = Erase()
            self.shapes.append(eraser)
            print(self.shapes)
        elif main.medium == 'Circle':
            #If circle, then make an oval
            oval = Oval(main, event.x, event.y)
            self.shapes.append(oval)
            print(self.shapes)
        elif main.medium == 'Rectangle':
            #If square, then make a rectangle
            rect = Rect(main, event.x, event.y)
            self.shapes.append(rect)
            print(self.shapes)

    #fix painting so it is continuous
    def paint(self, event:tk.Event, parent:windows):
        x1, y1 = (event.x-1),(event.y-1)
        x2, y2 = (event.x+1),(event.y+1)
        if len(self.shapes) > 0 :
            #see if the shape has ended
            if self.shapes[-1].end == True:
                #make the shape instead
                self.make_shape(event, parent)
            else:
                if type(self.shapes[-1]) == Erase:
                    self.shapes[-1].add_point(event.x, event.y, self, parent)
                elif type(self.shapes[-1]) == Line:
                    self.shapes[-1].add_point(event.x, event.y, self, parent)
                elif type(self.shapes[-1]) == Oval:
                    self.shapes[-1].make_oval(event.x, event.y, self, parent)
                elif type(self.shapes[-1]) == Rect:
                    self.shapes[-1].make_rect(event.x, event.y, self, parent)

    def end_shape(self, event:tk.Event, parent:windows):
        if type(self.shapes[-1]) == Erase:
            self.shapes[-1].end = True
        elif type(self.shapes[-1]) == Line:
            self.shapes[-1].end = True

#Classes for toolbar menu
class Pen():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Pen', command = lambda: window.set_medium('Pen'))
        m.pack(side='left',fill='none')
class Eraser():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Eraser', command= lambda: window.set_medium('Eraser'))
        m.pack(side='left',fill='none')
class Circle():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Circle', command = lambda: window.set_medium('Circle'))
        m.pack(side='left',fill='none')
class Rectangle():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Rectangle', command = lambda: window.set_medium('Rectangle'))
        m.pack(side='left',fill='none')
class Fill():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Checkbutton(parent, text='Fill', variable=window.fill, onvalue=1, offvalue=0)
        m.pack(side='left', fill='none')
class Edit():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Edit', command = lambda: window.set_medium('Edit'))
        m.pack(side='left',fill='none')
class Color():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Color', command = lambda: self.set_color(window))
        m.pack(side='left',fill='none')
        self.color_view = tk.Entry(parent, bg = window.color, width=2)
        self.color_view.pack(side='left', fill='none')
    def set_color(self, main:windows):
        #set the main color
        color = colorchooser.askcolor(title='Choose color')[1]
        main.color = "#" + color.partition("#")[2]
        #set the background
        self.color_view.configure(bg = main.color)       
class Width():
    def __init__(self, parent:tk.Frame, main:windows):
        frame = tk.Frame(parent)
        word = tk.Label(frame, text='Width:')
        word.pack(side='left', fill='none')
        m = tk.Entry(frame)
        m.pack(side='left', fill='none')
        m.bind('<KeyRelease>', lambda event: main.set_width(event, m))
        m.insert(0, '1')
        frame.pack(side='left',fill='none')

#classes for shapes drawn
class Line():
    def __init__(self):
        self.points = []
        self.lines = []
        self.width = 1
        self.color = 'black'
        self.end = False

    def add_point(self, x, y, canvas: Drawing, main:windows):
        #make the line
        if len(self.points) != 0:
            x0, y0 = self.points[-1]['x'], self.points[-1]['y']
            line = canvas.create_line(x0, y0, x, y, fill=main.color, width=main.width)
            #update color and width
            self.width = main.width
            self.color = main.color
            #line = canvas.create_arc(x, y, x0, y0, fill=main.color, width=main.width, style=tk.ARC)

            self.lines.append(line)

        self.points.append({'x': x, 'y': y})

    def remake(self, canvas:Drawing):
        #get the first points
        x, y = self.points[0]['x'], self.points[0]['y']

        #iterate over all of the points and make a line for each
        for i in self.points[1:]:
            x0, y0 = i['x'], i['y']
            #create the line
            line = canvas.create_line(x0, y0, x, y, fill=self.color, width=self.width)
            #Update the intitial x and y
            x, y = x0, y0

            self.lines.append(line)
class Erase():
    def __init__(self):
        self.points = []
        self.lines = []
        self.width = 1
        self.end = False

    def add_point(self, x, y, canvas: Drawing, main:windows):
        #make the line
        if len(self.points) != 0:
            x0, y0 = self.points[-1]['x'], self.points[-1]['y']
            line = canvas.create_line(x0, y0, x, y, fill=self.background, width=main.width)
            self.width = main.width
            self.lines.append(line)

        self.points.append({'x': x, 'y': y})

    def remake(self, canvas:Drawing):
        #get the first points
        x, y = self.points[0]['x'], self.points[0]['y']

        #iterate over all of the points and make a line for each
        for i in self.points[1:]:
            x0, y0 = i['x'], i['y']
            #create the line
            line = canvas.create_line(x0, y0, x, y, fill=self.background, width=self.width)
            #Update the intitial x and y
            x, y = x0, y0

            self.lines.append(line)
class Oval():
    def __init__(self, main:windows, x:int, y:int):
        self.start = {'x':x, 'y':y}
        self.lines = []
        self.end = {'x':x, 'y':y}
        self.color = main.color
        self.width = main.width
        self.fill = main.fill.get()

    def make_oval(self, x, y, canvas: Drawing, main:windows):
        #delete current line
        if self.lines is not []:
            canvas.delete(self.lines)
            self.lines = []
        x0, y0 = self.start['x'], self.start['y']
        oval = 0
        if self.fill == 0:
            oval = canvas.create_oval(x0, y0, x, y, outline=self.color, width=self.width)
        else:
            oval = canvas.create_oval(x0, y0, x, y, outline=self.color, width=self.width, fill = self.color)


        self.lines.append(oval)

        self.end['x'], self.end['y'] = x, y

    def remake(self, canvas:Drawing):
        x, y = self.start['x'], self.start['y']
        x0, y0 = self.end['x'], self.end['y']
        if self.fill == 0:
            oval = canvas.create_oval(x0, y0, x, y, outline=self.color, width=self.width)
        else:
            oval = canvas.create_oval(x0, y0, x, y, outline=self.color, width=self.width, fill = self.color)

        self.lines.append(oval)
class Rect():
    def __init__(self, main:windows, x:int, y:int):
        self.start = {'x':x, 'y':y}
        self.lines = []
        self.end = {'x':x, 'y':y}
        self.color = main.color
        self.width = main.width
        self.fill = main.fill.get()

    def make_rect(self, x, y, canvas: Drawing, main:windows):
        #delete current line
        if self.lines is not []:
            canvas.delete(self.lines)
            self.lines = []
        x0, y0 = self.start['x'], self.start['y']
        if self.fill == 0:
            rect = canvas.create_rectangle(x0, y0, x, y, outline=self.color, width=self.width)
        else:
            rect = canvas.create_rectangle(x0, y0, x, y, outline=self.color, width=self.width, fill = self.color)


        self.lines.append(rect)

        self.end['x'], self.end['y'] = x, y

    def remake(self, canvas:Drawing):
        x, y = self.start['x'], self.start['y']
        x0, y0 = self.end['x'], self.end['y']
        if self.fill == 0:
            rect = canvas.create_rectangle(x0, y0, x, y, outline=self.color, width=self.width)
        else:
            rect = canvas.create_rectangle(x0, y0, x, y, outline=self.color, width=self.width, fill = self.color)

        self.lines.append(rect)
    
    #get the color of a pixel
    def get_color(self, x:int, y:int, main:windows):
        ids = main.canvas.find_overlapping(x,y,x,y)
        if len(ids) > 0:
            index = ids[-1]
            return main.canvas.itemcget(index, 'fill')
        return main.background

    #add points to list
    def add(self, x, y):
        self.points.append(x)
        self.points.append(y)
        self.tuples.append((x, y))

class Draw_Button(tk.Button):
    #initialize
    def __init__(self, main: windows):
        tk.Button.__init__(self, main, text='Draw', command = lambda:self.draw_file(main))
        #set the main file
        main.set_file()

    def draw_file(self, main:windows):
        #set the bitmap and image
        main.set_bmp()
        main.set_file()

        #open a top-level window
        self.open_web()
        window = Draw_Window(main)
        window.mainloop()

        # #if already a .svg file, print
        # if '.svg' in main.file:
        #     ad = axidraw.AxiDraw()
        #     ad.plot_setup(self.file)
        #     ad.plot_run()
        # #turn the file into an svg
        # else:
        #     print('make file')
    def open_web(self):
        svg_url = 'https://svgtrace.com/png-to-svg'
        webbrowser.open(svg_url)
class Draw_Window(tk.Toplevel):
    #initialize
    def __init__(self, main:windows):
        tk.Toplevel.__init__(self, main)
        self.title('Draw the Image')

        #file name
        file = os.path.realpath(os.path.dirname(__file__)) + '/temp.png'
        #change the file name
        file = file.replace('\\', '/')

        explain_frame = tk.Frame(self)
        #make a text box for explaining the process
        text = tk.Label(explain_frame, anchor='w', text='In the svg converter, upload the file "' + file + '".')
        text.pack(expand=True, fill='x', side='top')
        text = tk.Label(explain_frame, anchor='w', text='Select at most four colors for the creation of the svg.\nType the hexcodes for each color in the boxes below')
        text.pack(expand=True, fill='x', side='top')
        #make the frame for containing the colors
        frame = tk.Frame(explain_frame)
        self.colors = []
        self.color_frame(frame)
        frame.pack(expand=True, fill='x', side='top')
        #final instructions
        text = tk.Label(explain_frame, anchor='w', text='When asked to choose a file, select the svg created by the converter.')
        text.pack(expand=True, fill='x', side='top')
        explain_frame.pack(expand=True, fill='x', side='top')
        #add button to upload the svg
        frm_button = tk.Frame(self)
        frm_button.pack(expand=True, fill='x', side='bottom')
        self.file = ''
        button = tk.Button(self, text='Upload svg', command=self.select_svg)
        button.pack(expand=False, fill='none', side='right')

    #fill color frame
    def color_frame(self, frame:tk.Frame):
        for i in range(0, 4):
            c = Hex_Color(frame)
            self.colors.append(c)
            c.pack(expand=True, fill='x', side='top')

    #choose the svg
    def select_svg(self):
        #get the file 
        self.file = askopenfilename(
            filetypes=[
                ('Scalabale Vector Graphics', '*.svg'),
                ('Images', '*.png *.img *.bmp *.jpeg'),
                ('All Files', '*.*')
            ]
        )
        if not self.file:
            return

        #TODO: finish the method so once an image is uploaded it is there

     
class Hex_Color(tk.Frame):
    #initialize
    def __init__(self, parent:tk.Frame):
        tk.Frame.__init__(self, parent)
        #insert an entry box
        self.entry = tk.Entry(self)
        self.entry.pack(expand=False, fill='none', side='left')
        text = tk.Label(self, anchor='w', text=' -> ')
        text.pack(expand=False, fill='none', side='left')
        self.color = tk.Label(self, anchor='w', text='')
        self.color.pack(expand=False, fill='none', side='left')

#run the program
if __name__ == '__main__':
    w = windows()
    w.mainloop()