import tkinter as tk
from pyaxidraw import axidraw
from tkinter.filedialog import askopenfilename, asksaveasfilename
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk

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
        self.medium='pen'
        self.file = ''
        self.image = ''
        self.svg = ''
        
        #creating a menu for the main window
        self.make_menu()

        #create a toolbar for the main window
        self.tools = {}
        self.make_toolbar()

        #create a large generic frame for the main window
        # self.container = Drawing(self)
        # self.container.pack(side='top', fill='both',expand=True)
        self.container = tk.Frame(self)
        # self.container.configure(bg='white')
        self.container.pack(side='top', fill='both',expand=True)
        # self.frm_can.pack(side='top', fill='both',expand=True)
        self.canvas = Drawing(self.container, self)
        self.canvas.pack(side='top', fill='both',expand=True)
        # self.container = self.canvas.canvas

        #create a button for packing
        self.btn_plt = tk.Button()
        self.make_plot()
        

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
        for B in (Pen, Eraser, Circle, Rectangle, Edit):
            button = B(tools,self)
            self.tools[B] = button
        tools.pack(anchor='n',fill='x')

    def make_plot(self):
        self.btn_plot = tk.Button(master=self, text='Draw', command=self.draw_file)
        self.btn_plot.pack(side='bottom', anchor='se')

    def set_medium(self, medium):
        self.medium = medium
        print(self.medium)

    def draw_file(self):
        print('Drawing')
    
    def open(self):
        #print the image
        print(self.file)
        print(self.image)
        img = Image.open(self.image)
        pimg = ImageTk.PhotoImage(img)
        #With label
        # label = tk.Label(main.container, image=pimg)
        # label.image = pimg
        # label.grid(row=0, column=0, sticky='nesw')
        # main.update()
        #with canvas
        self.canvas.create_image(0,0,anchor=tk.NW, image=pimg)
        self.canvas.image = pimg
        self.update()

      
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
            main.image = 'temp.png'
        else:
            main.image = main.file
    
        #print the image
        print(main.file)
        print(main.image)
        img = Image.open(main.image)
        pimg = ImageTk.PhotoImage(img)

        #with canvas
        main.canvas.create_image(0,0,anchor=tk.NW, image=pimg)
        main.canvas.image = pimg
        #main.update()
        


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
        self.bind('<B1-Motion>',lambda event: self.paint(event, main))
    
    def paint(self, event:tk.Event, parent:windows):
        x1, y1 = (event.x-1),(event.y-1)
        x2, y2 = (event.x+1),(event.y+1)
        if parent.medium == 'eraser':
                self.create_oval(x1, y1, x2, y2, fill = 'white', outline='white')
        else:
            self.create_oval(x1, y1, x2, y2, fill = 'black')

#Class for canvas frame
class Drawing2():
    def __init__(self, parent:tk.Frame):
        self.canvas = tk.Canvas(parent, bg='white')
        self.canvas.pack(side='top', fill='both',expand=True)
        self.canvas.bind('<B1-Motion>',lambda event: self.paint(event, parent))
    
    def paint(self, event:tk.Event, parent:windows):
        x1, y1 = (event.x-1),(event.y-1)
        x2, y2 = (event.x+1),(event.y+1)
        if parent.medium == 'eraser':
                self.canvas.create_oval(x1, y1, x2, y2, fill = 'white', outline='white')
        else:
            self.canvas.create_oval(x1, y1, x2, y2, fill = 'black')


#Classes for toolbar menu
class Pen():
    def __init__(self, parent:tk.Frame, window:windows):
        pen = tk.Button(parent, text='Pen', command = lambda: window.set_medium('Pen'))
        pen.pack(side='left',fill='none')
class Eraser():
    def __init__(self, parent:tk.Frame, window:windows):
        pen = tk.Button(parent, text='Eraser', command= lambda: window.set_medium('Eraser'))
        pen.pack(side='left',fill='none')
class Circle():
    def __init__(self, parent:tk.Frame, window:windows):
        pen = tk.Button(parent, text='Circle', command = lambda: window.set_medium('Circle'))
        pen.pack(side='left',fill='none')
class Rectangle():
    def __init__(self, parent:tk.Frame, window:windows):
        pen = tk.Button(parent, text='Rectangle', command = lambda: window.set_medium('Rectangle'))
        pen.pack(side='left',fill='none')
class Edit():
    def __init__(self, parent:tk.Frame, window:windows):
        pen = tk.Button(parent, text='Edit', command = lambda: window.set_medium('Edit'))
        pen.pack(side='left',fill='none')
        

#run the program
if __name__ == '__main__':
    w = windows()
    w.mainloop()