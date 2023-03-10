import tkinter as tk
from pyaxidraw import axidraw
from tkinter.filedialog import askopenfilename, asksaveasfilename
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from tkinter import colorchooser
import re
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
        self.width = 1
        self.file = ''
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
        self.btn_plt = tk.Button()
        self.make_plot()

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

        #add the menu to the window
        self.config(menu=menu)

    def make_toolbar(self):
        tools = tk.Frame(self)
        for B in (Pen, Eraser, Circle, Rectangle, Edit, Color, Width):
            button = B(tools,self)
            self.tools[B] = button
        tools.pack(anchor='n',fill='x')

    def make_plot(self):
        self.btn_plot = tk.Button(master=self, text='Draw', command=self.draw_file)
        self.btn_plot.pack(side='bottom', anchor='se')

    def set_medium(self, medium):
        self.medium = medium
        print(self.medium)

    def set_color(self):
        color = colorchooser.askcolor(title='Choose color')[1]
        self.color = "#" + color.partition("#")[2]

    def set_width(self, event:tk.Event, entry:tk.Entry):
        print('in')
        # self.width = entry.get()
        # print(self.width)
        # print(entry.get())
        # print(type(entry.get()))
        # print(event.char)
        # print(type(event.char))

        #remove letters
        num = re.sub("[^0-9]", "", entry.get())
        #set width
        if num == '' or num == '0':
            num = '1'
        self.width = int(num)
        #update entry
        entry.delete(0, tk.END)
        entry.insert(0, num)
        print(self.width)



    def draw_file(self):
        #if already a .svg file, print
        if '.svg' in self.file:
            ad = axidraw.AxiDraw()
            ad.plot_setup(self.file)
            ad.plot_run()
        
    

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

        #set the image
        if '.svg' in main.file:
            #if .svg, get the file and then set the image
            get_svg(main.file)
            main.svg = main.file
            main.image = 'temp.png'
        else:
            main.image = main.file
    
        #print the image
        img = Image.open(main.image)
        pimg = ImageTk.PhotoImage(img)

        #with canvas
        main.canvas.create_image(0,0,anchor=tk.NW, image=pimg)
        main.canvas.image = pimg
        


class Save():
    def __init__(self, button:tk.Menu, parent:windows):
        button.add_command(label='Save', command=self.save_file)
    def save_file(self):
        print('Save file')

#Class for canvas frame
class Drawing(tk.Canvas):
    def __init__(self, parent:tk.Frame, main:windows):
        tk.Canvas.__init__(self, parent)
        self.configure(bg='white')
        self.shapes = []
        self.bind('<Button-1>', lambda event: self.make_shape(event, main))
        self.bind('<B1-Motion>',lambda event: self.paint(event, main))
    
    def make_shape(self, event:tk.Event, main:windows):
        if main.medium == 'Pen':
            line = Line()
            self.shapes.append(line)
            for i in self.shapes:
                print(i)
            print(self.shapes)
        elif main.medium == 'Eraser':
            eraser = Erase(main)
            self.shapes.append(eraser)
            for i in self.shapes:
                print(i)
            print(self.shapes)

    #fix painting so it is continuous
    def paint(self, event:tk.Event, parent:windows):
        x1, y1 = (event.x-1),(event.y-1)
        x2, y2 = (event.x+1),(event.y+1)
        if len(self.shapes) > 0 and type(self.shapes[-1]) == Erase:
            self.shapes[-1].add_point(event.x, event.y, self)

        else:
            if len(self.shapes) > 0 and type(self.shapes[-1]) == Line:
                self.shapes[-1].add_point(event.x, event.y, self, parent)



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
class Edit():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Edit', command = lambda: window.set_medium('Edit'))
        m.pack(side='left',fill='none')
class Color():
    def __init__(self, parent:tk.Frame, window:windows):
        m = tk.Button(parent, text='Color', command = window.set_color)
        m.pack(side='left',fill='none')
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


class Line():
    def __init__(self):
        self.points = []
        self.lines = []

    def add_point(self, x, y, canvas: Drawing, main:windows):
        #make the line
        if len(self.points) != 0:
            x0, y0 = self.points[-1]['x'], self.points[-1]['y']
            line = canvas.create_line(x0, y0, x, y, fill=main.color, width=main.width)
            self.lines.append(line)

        self.points.append({'x': x, 'y': y})

class Erase():
    def __init__(self):
        self.points = []
        self.lines = []

    def add_point(self, x, y, canvas: Drawing, main:windows):
        #make the line
        if len(self.points) != 0:
            x0, y0 = self.points[-1]['x'], self.points[-1]['y']
            line = canvas.create_line(x0, y0, x, y, fill='white', width=main.width)
            self.lines.append(line)

        self.points.append({'x': x, 'y': y})

#run the program
if __name__ == '__main__':
    w = windows()
    w.mainloop()