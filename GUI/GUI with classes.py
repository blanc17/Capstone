import tkinter as tk
from pyaxidraw import axidraw
from tkinter.filedialog import askopenfilename, asksaveasfilename
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from tkinter import colorchooser
import re
import sys
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
    
        #plot the image
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

    # #TODO: test getting color
    # def get_color(self, event:tk.Event, main:windows):
    #     x, y = event.x, event.y
    #     ids = self.find_overlapping(x, y, x, y)
    #     if len(ids) == 0:
    #         print(main.background)
    #     else:
    #         index = ids[-1]
    #         color = self.itemcget(index, 'fill')
    #         print(color)

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
# class Bucket():
#     def __init__(self, main:windows, x:int, y:int):      
#         self.points = []
#         self.tuples = []
#         #set the original color
#         self.og_color = self.get_color(x, y, main)
#         self.new_color = main.color
#         print(self.new_color)
#         self.lines = ''
        
#         #perform the painting operation
#         if self.og_color is not self.new_color:
#             self.paint(x, y, main.canvas, main)

    # def paint2(self, x:int, y:int, canvas: Drawing, main:windows):
    #     #get the color at the point specified
    #     color = self.get_color(x, y, main)

    #     #if the color of the points is the same as the original color
    #     if color == self.og_color:
    #         #change the color of the pixel
    #         r = canvas.create_rectangle(x, y, x, y, fill = self.new_color, outline=self.new_color)
    #         self.points.append(r)

    #         #recusively check the surrounding points
    #         if self.og_color == self.get_color(x, y-1, main):
    #             self.paint(x, y-1, canvas, main)
    #         if self.og_color == self.get_color(x+1, y, main):
    #             self.paint(x+1,y,canvas, main)
    #         if self.og_color == self.get_color(x, y+1, main):
    #             self.paint(x, y+1, canvas, main)
    #         if self.og_color == self.get_color(x-1, y, main):
    #             self.paint(x-1, y, canvas, main)

    # #TODO: attempting painting with a polygon
    # def paint(self, x:int, y:int, canvas:Drawing, main:windows):
            
    #     #get the first point to fill in
    #     y0 = self.get_first_point(x, y, canvas, main)
    #     self.add(x, y0)

    #     #get the rest of the points
    #     self.get_points(x, y0, canvas, main)
    #     print(self.points)
        
    #     # #attempt to try drawing with canvas
    #     # self.points = [x, y-10, x+10, y, x, y+10, x-5, y+5]
    #     #draw the points
    #     canvas.create_polygon(self.points, outline=main.color, fill=main.color)

    # def get_first_point(self, x:int, y:int, canvas:Drawing, main:windows):
    #     first_point = y
    #     if y == 1:
    #         return first_point
    #     else:
    #         #get the color at the point specified
    #         color = self.get_color(x, y, main)
    #         color2 = self.get_color(x, y-1, main)
    #         #if the color is the same
    #         if color == color2:
    #             #recursion 
    #             first_point = self.get_first_point(x, y-1, canvas, main)
    #             return first_point
    #         else:
    #             return first_point
        
    
    # #get points to add to the list
    # def get_points(self, x:int, y:int, canvas:Drawing, main:windows):
    #     print(x, y)
    #     print(self.tuples)
    #     #if the tuple has not been used yet
    #     if (x, y) not in self.tuples or len(self.tuples) == 1:
    #         self.add(x, y)
    #         #look at surrounding points in a circle
    #         if self.og_color == self.get_color(x, y-1, main) and (x, y-1) not in self.tuples:
    #             #up
    #             print('up')
    #             #self.add(x, y-1)
    #             self.get_points(x, y-1, canvas, main)
    #         else:
    #             if self.og_color == self.get_color(x+1, y, main) and (x+1, y) not in self.tuples:
    #                 #right
    #                 print('right')
    #                 #self.add(x+1, y)
    #                 self.get_points(x+1, y, canvas, main)
    #             else:
    #                 if self.og_color == self.get_color(x, y+1, main) and (x, y+1) not in self.tuples:
    #                     #down
    #                     print('down')
    #                     #self.add(x, y+1)
    #                     self.get_points(x, y+1, canvas, main)
    #                 else:
    #                     if self.og_color == self.get_color(x-1, y, main) and (x-1, y) not in self.tuples:
    #                         #left
    #                         print('left')
    #                         #self.add(x-1, y)
    #                         self.get_points(x-1, y, canvas, main)
        #if the recurion has not made it's way back to the start
        # if x != self.points[0] or y != self.points[1] or len(self.points) <= 2:
        #     print('in')
        #     #look at all points in a circle from the given point
        #     if self.og_color == self.get_color(x, y-1, main):
        #         print('up')
        #         if len(self.points) <=2 or x is not self.points[-2] or y-1 is not self.points[-1]:
        #             print('up')
        #             self.add(x, y-1)
        #             self.get_points(x, y-1, canvas, main)
        #     else:
        #         print('in')
        #         if self.og_color == self.get_color(x+1, y, main):
        #             print('right')
        #             if len(self.points) <=2 or x+1 is not self.points[-2] or y is not self.points[-1]:
        #                 print('right')
        #                 self.add(x+1, y)
        #                 self.get_points(x+1, y, canvas, main)
        #         else:
        #             if self.og_color == self.get_color(x, y+1, main):
        #                 print('down')
        #                 if len(self.points) <=2 or x is not self.points[-2] or y+1 is not self.points[-1]:
        #                     print('down')
        #                     self.add(x, y+1)
        #                     self.get_points(x, y+1, canvas, main)
        #             else:
        #                 if self.og_color == self.get_color(x-1, y, main):
        #                     print('left')
        #                     if len(self.points) <=2 or x-1 is not self.points[-2] or y is not self.points[-1]:
        #                         print('left')
        #                         self.add(x-1, y)
        #                         self.get_points(x-1, y, canvas, main)
    
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


    # #TODO: test getting color
    # def get_color(self, event:tk.Event, main:windows):
    #     x, y = event.x, event.y
    #     ids = self.find_overlapping(x, y, x, y)
    #     if len(ids) == 0:
    #         print(main.background)
    #     else:
    #         index = ids[-1]
    #         color = self.itemcget(index, 'fill')
    #         print(color)

#run the program
if __name__ == '__main__':
    w = windows()
    w.mainloop()