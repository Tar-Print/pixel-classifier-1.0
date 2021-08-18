#Written by Suraj Vaddi
#2020
#Goes to TJHSST

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

def main():
    global img,w,h,square_radius,root,canvas,image

    #img_name = input("What is the name of the file "
    img_name = "IBETGroup17.jpg"
    img = Image.open(img_name).convert('RGB')

    w = img.height
    h = img.width

    root = tk.Tk()
    root.resizable(0,0)
    root.title("Neighborhood Draft")
    canvas = tk.Canvas(root, width = w, height = h, bg = 'white')
    canvas.pack()

    display = ImageTk.PhotoImage(img)
    image = canvas.create_image(0,0,anchor = NW, image = display)

    square_radius = 35 #pixels

    canvas.tag_bind(image, '<Button-1>', click)
    root.mainloop()

def count_categorized_pixels(arr,center_x,center_y,blend_or_edge1,blend_or_edge2,blend_or_edge3):
    global img
    pixels_count = 0
    rgb_sums = [0,0,0]
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if(arr[x][y] == blend_or_edge1 or
               arr[x][y] == blend_or_edge2 or
               arr[x][y] == blend_or_edge3):
                pixels_count += 1
                r,g,b = img.getpixel((x+center_x-35,y+center_y-35))
                rgb_sums[0] += r
                rgb_sums[1] += g
                rgb_sums[2] += b
    rgb_avgs = [int(rgb_sums[0]/pixels_count),
                int(rgb_sums[1]/pixels_count),
                int(rgb_sums[2]/pixels_count)]
    if(blend_or_edge1 == 0):
        print("Blend pixel average:")
    elif(blend_or_edge1 == 2):
        print("Edge pixel average:")
    else:
        print("Not a valid category value")
    print(rgb_avgs)

def is_valid(to_check_x,to_check_y,max_x,max_y,arr,num_to_check):
    if(to_check_x >= 0 and to_check_x < max_x and
       to_check_y >= 0 and to_check_y < max_y):
        if(arr[to_check_x][to_check_y] == num_to_check):
            return True
    return False

def add_edges(arr,num_detect,num_mark):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if arr[x][y] == 1:
                max_x = len(arr)
                max_y = len(arr)
                if(is_valid(x-1,y-1,max_x,max_y,arr,num_detect) or
                   is_valid(x,y-1,max_x,max_y,arr,num_detect) or
                   is_valid(x+1,y-1,max_x,max_y,arr,num_detect) or
                   is_valid(x+1,y,max_x,max_y,arr,num_detect) or
                   is_valid(x+1,y+1,max_x,max_y,arr,num_detect) or
                   is_valid(x,y+1,max_x,max_y,arr,num_detect) or
                   is_valid(x-1,y+1,max_x,max_y,arr,num_detect) or
                   is_valid(x-1,y,max_x,max_y,arr,num_detect)):
                    arr[x][y] = num_mark
    return arr

def print2d(arr):
    arr_to_print = []
    for i in range(len(arr)):
        arr_to_print.append([])
        for j in range(len(arr[i])):
            arr_to_print[i].append(arr[j][i])
        print(arr_to_print[i])


def to_array_values(center_val,to_change_val):
    array_value = to_change_val - center_val
    array_value += 35
    return array_value

def get_color_diff(rgb1,rgb2):
    r_diff = abs(rgb1[0]-rgb2[0])
    g_diff = abs(rgb1[1]-rgb2[1])
    b_diff = abs(rgb1[2]-rgb2[2])
    rg_avg = (r_diff+g_diff)/2
    gb_avg = (g_diff+b_diff)/2
    br_avg = (b_diff+r_diff)/2
    conc_rgb = (rg_avg+gb_avg+br_avg)/3
    return conc_rgb

def get_subtraction_vector(center_x,center_y,curr_x,curr_y):
    x_diff = curr_x - center_x
    y_diff = curr_y - center_y
    if(abs(x_diff)==abs(y_diff)):
        return [x_diff//(abs(x_diff)),y_diff//(abs(y_diff))]
    else:
        return([x_diff//(abs(x_diff)),0] if (abs(x_diff)>abs(y_diff)) else [0,y_diff//(abs(y_diff))])

def operate_on_pixel(categorized_pixels,center_x,center_y,curr_x,curr_y):
    subtraction_vector = get_subtraction_vector(center_x,center_y,curr_x,curr_y)
    prev_x = curr_x - subtraction_vector[0]
    prev_y = curr_y - subtraction_vector[1]

    arr_val_x = to_array_values(center_x,curr_x)
    arr_val_y = to_array_values(center_y,curr_y)

    prev_arr_val_x = to_array_values(center_x,prev_x)
    prev_arr_val_y = to_array_values(center_y,prev_y)

    if(categorized_pixels[prev_arr_val_x][prev_arr_val_y] == 1 or categorized_pixels[prev_arr_val_x][prev_arr_val_y] == 2):
        categorized_pixels[arr_val_x][arr_val_y] = 1
        return categorized_pixels
    elif(categorized_pixels[prev_arr_val_x][prev_arr_val_y] == 0):
        if(get_color_diff(img.getpixel((curr_x,curr_y)),img.getpixel((prev_x,prev_y)))>=15):
            categorized_pixels[arr_val_x][arr_val_y] = 2
            return categorized_pixels
        elif(abs(curr_x-center_x)>=2 and abs(curr_y-center_y)>=2 and get_color_diff(img.getpixel((curr_x, curr_y)),img.getpixel((curr_x-subtraction_vector[0]*2, curr_y-subtraction_vector[1]*2))) >= 15):
            categorized_pixels[arr_val_x][arr_val_y] = 2
            return categorized_pixels
        else:
            categorized_pixels[arr_val_x][arr_val_y] = 0
            return categorized_pixels
    else:
        print("Problem")

def square_loop(center_x,center_y):
    global square_radius
    categorized_pixels = []

    for i in range(square_radius * 2 + 1):
        categorized_pixels.append([])
        for j in range(square_radius * 2 + 1):
            categorized_pixels[i].append(9)
    categorized_pixels[35][35] = 0

    for i in range(36):
        local_x = 0 - i
        local_y = 0 - i
        curr_x = local_x + center_x
        curr_y = local_y + center_y
        for j in range(4):
            for k in range(i*2):
                    if j == 0:
                        if (curr_x >= 0 and curr_x < w and curr_y >= 0 and curr_y < h):
                            operate_on_pixel(categorized_pixels,center_x,center_y,curr_x,curr_y)
                        curr_x += 1
                    elif j == 1:
                        if (curr_x >= 0 and curr_x < w and curr_y >= 0 and curr_y < h):
                            operate_on_pixel(categorized_pixels,center_x,center_y,curr_x,curr_y)
                        curr_y += 1
                    elif j == 2:
                        if (curr_x >= 0 and curr_x < w and curr_y >= 0 and curr_y < h):
                            operate_on_pixel(categorized_pixels,center_x,center_y,curr_x,curr_y)
                        curr_x -= 1
                    else:
                        if (curr_x >= 0 and curr_x < w and curr_y >= 0 and curr_y < h):
                            operate_on_pixel(categorized_pixels,center_x,center_y,curr_x,curr_y)
                        curr_y -= 1
    categorized_pixels = add_edges(categorized_pixels,0,2)
    categorized_pixels = add_edges(categorized_pixels,2,3)
    categorized_pixels = add_edges(categorized_pixels,3,4)
    print2d(categorized_pixels)
    count_categorized_pixels(categorized_pixels,center_x,center_y,0,-1,-1)
    count_categorized_pixels(categorized_pixels,center_x,center_y,2,3,4)

    print(" ")

def click(evt):
    square_loop(evt.x, evt.y)

if __name__ == '__main__':
    main()