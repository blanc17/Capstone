#Import the required Libraries
from tkinter import *
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename


#Create an instance of tkinter frame
win = Tk()

#Set the geometry of tkinter frame
win.geometry("750x250")

#Create a canvas
canvas= Canvas(win, width= 600, height= 400)
canvas= Canvas(win)
canvas.pack()

file = askopenfilename(
    filetypes=[
        ('All Files', '*.*')
    ]
)
#Load an image in the script
img= ImageTk.PhotoImage(Image.open(file))

#Add image to the Canvas Items
canvas.create_image(0, 0, anchor=NW,image=img)

win.mainloop()