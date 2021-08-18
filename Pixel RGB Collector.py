#Written by Suraj Vaddi
#2020
#Goes to TJHSST

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

w = 625
h = 625
r,g,b = -1,-1,-1
ALL_VALS = {'Pervious':[],'Fall_Pervious':[], 'Dry_Pervious':[], 'Shaded_Pervious':[], 'Impervious':[],
            'Tan_Impervious':[]}

img_name = input("What is the name of the file ")

root = tk.Tk()
root.resizable(0,0)
root.title("Data Collector")
canvas = tk.Canvas(root, width = w, height = h, bg = 'white')
canvas.pack()

ALL_FILES = {}

for key in ALL_VALS:
    ALL_FILES[key] = open("Data_" + key +".txt", "a+")

stats_file = open("Data_Files_Stats.txt","w")

img = Image.open(img_name).convert('RGB')
display = ImageTk.PhotoImage(img)
image = canvas.create_image(0,0,anchor = NW, image = display)

def to_2(val):
    val = str(val)
    if(len(val)<2):
        val = '0'+ val
    return val

def add_perv(evt,type):
    print('clicked!')
    global ALL_VALS,r,g,b
    rgb_vals = [r,g,b]
    data_array = ALL_VALS[type]
    data_array.append(rgb_vals)
    ALL_FILES[type].write(str(rgb_vals[0]) + "\t" + str(rgb_vals[1]) + "\t" + str(rgb_vals[2]) + "\n")
    print(ALL_VALS)

def click(evt):
    global r,g,b
    x = evt.x
    y = evt.y
    if(x<=img.width and y<=img.height):
        r,g,b = img.getpixel((x,y))
        color_chosen1.config(bg = '#'+to_2(hex(r)[2:])+to_2(hex(g)[2:])+to_2(hex(b)[2:]))
        print(r,g,b)

#------------------
#BUTTONS AND LABELS

#Displays color chosen
color_chosen1 = tk.Label(root, width = 50)
color_chosen1.pack()

color_chosen2 = tk.Label(root, width = 50)
color_chosen2.pack()

color_chosen3 = tk.Label(root, width = 50)
color_chosen3.pack()

#Buttons and Button Functions:
btn_perv = tk.Button(root, text = 'Pervious')
btn_perv.pack(side = tk.LEFT)
btn_perv.bind('<Button-1>',lambda event:add_perv(event,'Pervious'))

btn_fall_perv = tk.Button(root, text = 'Fall Pervious')
btn_fall_perv.pack(side = tk.LEFT)
btn_fall_perv.bind('<Button-1>',lambda event:add_perv(event,'Fall_Pervious'))

btn_dry_perv = tk.Button(root, text = 'Dry Pervious')
btn_dry_perv.pack(side = tk.LEFT)
btn_dry_perv.bind('<Button-1>',lambda event:add_perv(event,'Dry_Pervious'))

btn_shade_perv = tk.Button(root, text = 'Shaded Pervious')
btn_shade_perv.pack(side = tk.LEFT)
btn_shade_perv.bind('<Button-1>',lambda event:add_perv(event,'Shaded_Pervious'))

btn_imperv = tk.Button(root, text = 'Impervious')
btn_imperv.pack(side = tk.LEFT)
btn_imperv.bind('<Button-1>',lambda event:add_perv(event,'Impervious'))

btn_tan_imperv = tk.Button(root, text = 'Tan Impervious')
btn_tan_imperv.pack(side = tk.LEFT)
btn_tan_imperv.bind('<Button-1>',lambda event:add_perv(event,'Tan_Impervious'))

btn_stop = tk.Button(root, text='Stop', bg = 'red', command=root.destroy)
btn_stop.pack(side = tk.RIGHT)

canvas.tag_bind(image,'<Button-1>', click)
root.mainloop()