#Written by Suraj Vaddi
#2020
#Goes to TJHSST

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

r,g,b = -1,-1,-1
clicks = -1
rgb = [-1,-1]
ALL_VALS = {'Edge':[],'Blend':[]}

img_name = 'Baseball Field.png'

root = tk.Tk()
root.resizable(0,0)
root.title("Edge Detector")

img = Image.open(img_name).convert('RGB')
display = ImageTk.PhotoImage(img)

canvas = tk.Canvas(root, width = img.width, height = img.height, bg = 'white')
canvas.pack()

image = canvas.create_image(0,0,anchor = NW, image = display)

conc_rgb = -1

ALL_FILES = {}

for key in ALL_VALS:
    ALL_FILES[key] = open("Data_" + key +".txt", "a+")

def get_conc_rgb(rgb1,rgb2):
    global conc_rgb
    r_diff = abs(rgb1[0]-rgb2[0])
    g_diff = abs(rgb1[1]-rgb2[1])
    b_diff = abs(rgb1[2]-rgb2[2])
    rg_avg = (r_diff+g_diff)/2
    gb_avg = (g_diff+b_diff)/2
    br_avg = (b_diff+r_diff)/2
    conc_rgb = (rg_avg+gb_avg+br_avg)/3

def add_edge(evt,type):
    print('clicked!')
    global ALL_VALS,r,g,b
    rgb_vals = [r,g,b]
    data_array = ALL_VALS[type]
    data_array.append(rgb_vals)
    ALL_FILES[type].write(str(rgb_vals[0]) + "\t" + str(rgb_vals[1]) + "\t" + str(rgb_vals[2]) + "\n")
    print(ALL_VALS)

def click(evt):
    global r,g,b,clicks
    clicks += 1
    x = evt.x
    y = evt.y
    curr_rgb = []
    r,g,b = img.getpixel((x,y))
    curr_rgb.append(r)
    curr_rgb.append(g)
    curr_rgb.append(b)
    if(x<=img.width and y<=img.height):
        if(clicks%2==0):
            rgb[0] = curr_rgb
            pixel_chosen1.config(text=(str(rgb[0][0]) + ", " + str(rgb[0][1]) + ", " + str(rgb[0][2])))
            pixel_chosen2.config(text="")
            conc_avg.config(text="")
        if(clicks%2==1):
            rgb[1] = curr_rgb
            pixel_chosen2.config(text=(str(rgb[1][0]) + ", " + str(rgb[1][1]) + ", " + str(rgb[1][2])))
            get_conc_rgb(rgb[0],rgb[1])
            conc_avg.config(text=str(conc_rgb))

#------------------
#BUTTONS AND LABELS

#Displays color chosen
pixel_chosen1 = tk.Label(root, width = 50)
pixel_chosen1.pack()

pixel_chosen2 = tk.Label(root, width = 50)
pixel_chosen2.pack()

conc_avg = tk.Label(root, width = 50)
conc_avg.pack()

#Buttons and Button Functions:
edge_btn = tk.Button(root, text = 'Edge')
edge_btn.pack(side = tk.LEFT)
edge_btn.bind('<Button-1>',lambda event:add_edge(event,'Edge'))

blend_btn = tk.Button(root, text = 'Blend')
blend_btn.pack(side = tk.LEFT)
blend_btn.bind('<Button-1>',lambda event:add_edge(event,'Blend'))

btn_stop = tk.Button(root, text='Stop', bg = 'red', command=root.destroy)
btn_stop.pack(side = tk.RIGHT)

canvas.tag_bind(image,'<Button-1>', click)
root.mainloop()