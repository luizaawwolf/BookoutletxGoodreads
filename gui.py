# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:24:45 2020

@author: Luiza
"""
import io
from PIL import Image, ImageTk
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen
    
root = tk.Toplevel()
root.title("Title")
pic_url = "https://img1.od-cdn.com/ImageType-150/2183-1/9A5/466/AE/%7B9A5466AE-4A17-4489-9D81-958936F81BE9%7DImg150.jpg"
my_page = urlopen(pic_url)
# create an image file object
my_picture = io.BytesIO(my_page.read())
# use PIL to open image formats like .jpg  .png  .gif  etc
img = Label(self, image=my_pibcture)
img.image = render
        img.place(x=0, y=0).
pil_img = Image.open(my_picture)
# convert to an image Tkinter can use
tk_img = ImageTk.PhotoImage(pil_img)
# put the image on a typical widget
label = tk.Label(root, image=tk_img)
label.pack(padx=5, pady=5)
root.mainloop()