import tkinter as tk
from pyaxidraw import axidraw
from tkinter.filedialog import askopenfilename, asksaveasfilename
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk

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
        
        #creating a menu for the main window
        self.make_menu()

        #create a toolbar for the main window
        self.tools = {}
        self.make_toolbar()

        #create a large generic frame for the main window
        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand=True)
        

    def make_menu(self):
        
        menu = tk.Menu()

        #add a file button
        file = tk.Menu(menu, tearoff=0)
        for M in (New, Open, Save):
            M(file)
        menu.add_cascade(label='File', menu=file)

        #add the menu to the window
        self.config(menu=menu)

    def make_toolbar(self):
        tools = tk.Frame(self)
        for B in (Pen, Eraser, Circle, Rectangle, Edit):
            button = B(tools,self)
            self.tools[B] = button
        tools.pack(anchor='n',fill='x')

    def set_medium(self, medium):
        self.medium = medium
        print(self.medium)

            
        
#Classes for file menu
class New():
    def __init__(self, button):
        button.add_command(label='New', command=self.new_file)
    def new_file(self):
        print('New file')

class Open():
    def __init__(self, button):
        button.add_command(label='Open', command=self.open_file)
    def open_file(self):
        print('Open file')

class Save():
    def __init__(self, button):
        button.add_command(label='Save', command=self.save_file)
    def save_file(self):
        print('Save file')

#Classes for toolbar menu
class Pen():
    def __init__(self, parent, window):
        pen = tk.Button(parent, text='Pen', command = lambda: window.set_medium('Pen'))
        pen.pack(side='left',fill='none')
class Eraser():
    def __init__(self, parent, window):
        pen = tk.Button(parent, text='Eraser', command= lambda: window.set_medium('Eraser'))
        pen.pack(side='left',fill='none')
class Circle():
    def __init__(self, parent, window):
        pen = tk.Button(parent, text='Circle', command = lambda: window.set_medium('Circle'))
        pen.pack(side='left',fill='none')
class Rectangle():
    def __init__(self, parent, window):
        pen = tk.Button(parent, text='Rectangle', command = lambda: window.set_medium('Rectangle'))
        pen.pack(side='left',fill='none')
class Edit():
    def __init__(self, parent, window):
        pen = tk.Button(parent, text='Edit', command = lambda: window.set_medium('Edit'))
        pen.pack(side='left',fill='none')
        

#Classes for buttons

#run the program
if __name__ == '__main__':
    w = windows()
    w.mainloop()