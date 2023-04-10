# import aspose.words as aw
# from tkinter.filedialog import askopenfilename, asksaveasfilename
# import os

# doc = aw.Document()
# builder = aw.DocumentBuilder(doc)

# file = askopenfilename(
#             filetypes=[
#                 ('Scalabale Vector Graphics', '*.svg'),
#                 ('Images', '*.png *.img *.bmp *.jpeg'),
#                 ('All Files', '*.*')
#             ]
#         )
# shape = builder.insert_image(file)
# filename = os.path.realpath(os.path.dirname(__file__)) + '\\' + 'test_aspose.svg'
# shape.image_data.save(filename)

import aspose.words as aw
import os

doc = aw.Document()
builder = aw.DocumentBuilder(doc)
path = os.path.realpath(os.path.dirname(__file__)) + '\\'
shape = builder.insert_image(path + "Myles Morales.png")
shape.image_data.save(path + "aghagh.svg")


#import pypotrace as pypo
########################################

#Using aspose

# doc = aw.Document()
# builder = aw.DocumentBuilder(doc)

# file = askopenfilename(
#             filetypes=[
#                 ('Scalabale Vector Graphics', '*.svg'),
#                 ('Images', '*.png *.img *.bmp *.jpeg'),
#                 ('All Files', '*.*')
#             ]
#         )

# shape = builder.insert_image(file)
# shape.image_data.save("Output.svg")

########################################

