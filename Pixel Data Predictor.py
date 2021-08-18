#Written by Suraj Vaddi
#2020
#Goes to TJHSST

import tkinter as tk
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from keras.models import load_model

def main():
    global img,w,h,square_radius,root,canvas,image,all_rgbs,columns
    global color_chosen1,color_chosen2,color_chosen3
    global tar_print_model,labels_alph,predicted_label

#    img_name = input("What is the name of the file ")
    img_name = "Images/IBETGroup17.jpg"
    img = Image.open(img_name).convert('RGB')

    w = 625
    h = 625

    root = tk.Tk()
    root.resizable(0,0)
    root.title("All Data Collector")
    canvas = tk.Canvas(root, width = w, height = h, bg = 'white')
    canvas.pack()

    display = ImageTk.PhotoImage(img)
    image = canvas.create_image(0,0,anchor = NW, image = display)

    square_radius = 35 #pixels
    all_rgbs = []
    labels_alph = ['dry_pervious','fall_pervious','norm_impervious','norm_pervious','shaded_pervious','tan_impervious','water']

    tar_print_model = load_model('Models/wFall-woutWater-Models/Model-2/ML-Model.model')
    predicted_label = ''

#    canvas.tag_bind(image, '<Button-1>', click)
    build_interface()
    root.mainloop()

def to_2(val):
    val = str(val)
    if(len(val)<2):
        val = '0'+ val
    return val

def count_categorized_pixels(arr,center_x,center_y,blend_or_edge1,blend_or_edge2,blend_or_edge3):
    global img,w,h
    pixels_count = 0
    rgb_sums = [0,0,0]
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if(arr[x][y] == blend_or_edge1 or
               arr[x][y] == blend_or_edge2 or
               arr[x][y] == blend_or_edge3):
                pixels_count += 1
                if(x+center_x-35<w and y+center_y-35<h):
                    r,g,b = img.getpixel((x+center_x-35,y+center_y-35))
                    rgb_sums[0] += r
                    rgb_sums[1] += g
                    rgb_sums[2] += b
    if(pixels_count==0):
        return[0,0,0]
    else:
        rgb_avgs = [int(rgb_sums[0]/pixels_count),
                    int(rgb_sums[1]/pixels_count),
                    int(rgb_sums[2]/pixels_count)]
        return rgb_avgs

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
    global w,h
    subtraction_vector = get_subtraction_vector(center_x,center_y,curr_x,curr_y)
    prev_x = curr_x - subtraction_vector[0]
    prev_y = curr_y - subtraction_vector[1]

    arr_val_x = to_array_values(center_x,curr_x)
    arr_val_y = to_array_values(center_y,curr_y)

    prev_arr_val_x = to_array_values(center_x,prev_x)
    prev_arr_val_y = to_array_values(center_y,prev_y)

    if(0<=curr_x and curr_x<img.width and
       0<=curr_y and curr_y<img.height and
       0 <= prev_x and prev_x < img.width and
       0 <= prev_y and prev_y < img.height
    ):
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
    global img,square_radius

    categorized_pixels = []
    rgbs = img.getpixel((center_x,center_y))

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
#    print2d(categorized_pixels)
    local_rgbs = count_categorized_pixels(categorized_pixels,center_x,center_y,0,-1,-1)
    edges_rgbs = count_categorized_pixels(categorized_pixels,center_x,center_y,2,3,4)
    if(edges_rgbs[0]==0 and
       edges_rgbs[1]==0 and
       edges_rgbs[2]==0):
        edges_rgbs[0] = local_rgbs[0]
        edges_rgbs[1] = local_rgbs[1]
        edges_rgbs[2] = local_rgbs[2]
    return [rgbs[0],rgbs[1],rgbs[2],
            local_rgbs[0],local_rgbs[1],local_rgbs[2],
            edges_rgbs[0],edges_rgbs[1],edges_rgbs[2],]

def click(evt):
    global all_rgbs
    all_rgbs = square_loop(evt.x, evt.y)
    update_interface(all_rgbs)

def predict(evt):
    global tar_print_model,img,all_rgbs,labels_alph,predicted_label
    all_normal_rgbs = []
    all_normal_rgbs.append([])
    for i in range(len(all_rgbs)):
        all_normal_rgbs[0].append(all_rgbs[i]/255.0)
    predictions = tar_print_model.predict(all_normal_rgbs)
    predictions_max = np.amax(predictions)
    predictions_max_index = np.where(predictions==predictions_max)
    for i in range(len(predictions_max_index[1])):
        predicted_label = labels_alph[predictions_max_index[1][i]]
    update_interface(all_rgbs)

def build_interface():
    global img,w,h,root,canvas,image
    global color_chosen1,color_chosen2,color_chosen3,prediction_label_display

    canvas.tag_bind(image, '<Button-1>', click)
    # ------------------
    # BUTTONS AND LABELS

    # Displays color chosen
    color_chosen1 = tk.Label(root, width=50)
    color_chosen1.pack()

    color_chosen2 = tk.Label(root, width=50)
    color_chosen2.pack()

    color_chosen3 = tk.Label(root, width=50)
    color_chosen3.pack()

    prediction_label_display = tk.Label(root, width = 50)
    prediction_label_display.pack()

    # Buttons and Button Functions:
    btn_perv = tk.Button(root, text='Predict')
    btn_perv.pack(side=tk.LEFT)
    btn_perv.bind('<Button-1>',predict)

    btn_stop = tk.Button(root, text='Stop', bg='red', command=root.destroy)
    btn_stop.pack(side=tk.RIGHT)

def update_interface(all_rgbs):
    global img, w, h, root, canvas, image
    global color_chosen1, color_chosen2, color_chosen3, prediction_label_display
    global predicted_label

    color_chosen1.config(bg='#' + to_2(hex(all_rgbs[0])[2:]) + to_2(hex(all_rgbs[1])[2:]) + to_2(hex(all_rgbs[2])[2:]))
    color_chosen2.config(bg='#' + to_2(hex(all_rgbs[3])[2:]) + to_2(hex(all_rgbs[4])[2:]) + to_2(hex(all_rgbs[5])[2:]))
    color_chosen3.config(bg='#' + to_2(hex(all_rgbs[6])[2:]) + to_2(hex(all_rgbs[7])[2:]) + to_2(hex(all_rgbs[8])[2:]))
    if predicted_label == 'tan_impervious':
        prediction_label_display.config(text='Predicted label: ' + 'tan_pervious')
    else:
        prediction_label_display.config(text='Predicted label: ' + predicted_label)

if __name__ == '__main__':
    main()