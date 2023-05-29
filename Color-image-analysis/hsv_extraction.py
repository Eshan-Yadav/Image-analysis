
import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename

img=cv.imread(askopenfilename())
img=cv.resize(img,(500,500))
# img=cv.bitwise_not(img)

def slider(*args):
    hue1=int(h1_scale.get())
    sat1=int(s1_scale.get())
    val1=int(v1_scale.get())
    hue2=int(h2_scale.get())
    sat2=int(s2_scale.get())
    val2=int(v2_scale.get())

    lower_color = np.array([hue1, sat1, val1])  # Lower bound for HSV values 
    upper_color = np.array([hue2, sat2, val2])  # Upper bound for HSV values 
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # Create a mask using the inRange function
    mask = cv.inRange(hsv_image, lower_color, upper_color)


    # Apply the mask to the original image
    result = cv.bitwise_and(img, img, mask=mask)

    label_coloured_pixels.config(text="Total number of coloured pixels="+str(np.count_nonzero(mask)))
    label_percentage.config(text="Percentage of coloured pixels="+str(np.count_nonzero(mask)/(img.shape[0]*img.shape[1])*100)+"%")

    # Display the original image, mask, and the result
    cv.imshow('Original Image', img)
    cv.imshow('Mask', mask)
    cv.imshow('Result', result)





root=tk.Tk()

quantification=tk.Toplevel()
quantification.title("Quantification")

label_pixels=tk.Label(quantification,text=f"Total number of pixels={img.shape[0]*img.shape[1]}",font=("Arial", 16))
label_pixels.grid(row=0,column=0)

label_coloured_pixels=tk.Label(quantification,text="Total number of coloured pixels=0",font=("Arial", 16))
label_coloured_pixels.grid(row=1,column=0)

label_percentage=tk.Label(quantification,text="Percentage of coloured pixels=0%",font=("Arial", 16))
label_percentage.grid(row=2,column=0)


root.title("lower Color")

label_h1=tk.Label(root,text="Hue 1:",font=("Arial", 16))
label_h1.grid(row=0,column=0)
h1_scale=tk.Scale(root,from_=0,to=179,orient=tk.HORIZONTAL,command=slider)
h1_scale.set(0)
h1_scale.grid(row=0,column=1)
add_button=tk.Button(root,text="+",font=("Arial", 16),command=lambda:h1_scale.set(h1_scale.get()+1))
add_button.grid(row=0,column=2)
sub_button=tk.Button(root,text="-",font=("Arial", 16),command=lambda:h1_scale.set(h1_scale.get()-1))
sub_button.grid(row=0,column=3)



label_s1=tk.Label(root,text="Saturation 1:",font=("Arial", 16))
label_s1.grid(row=1,column=0)
s1_scale=tk.Scale(root,from_=0,to=255,orient=tk.HORIZONTAL,command=slider)
s1_scale.grid(row=1,column=1)
add_button=tk.Button(root,text="+",font=("Arial", 16),command=lambda:s1_scale.set(s1_scale.get()+1))
add_button.grid(row=1,column=2)
sub_button=tk.Button(root,text="-",font=("Arial", 16),command=lambda:s1_scale.set(s1_scale.get()-1))
sub_button.grid(row=1,column=3)


label_v1=tk.Label(root,text="Value 1:",font=("Arial", 16))
label_v1.grid(row=2,column=0)
v1_scale=tk.Scale(root,from_=0,to=255,orient=tk.HORIZONTAL,command=slider)
v1_scale.grid(row=2,column=1)
add_button=tk.Button(root,text="+",font=("Arial", 16),command=lambda:v1_scale.set(v1_scale.get()+1))
add_button.grid(row=2,column=2)
sub_button=tk.Button(root,text="-",font=("Arial", 16),command=lambda:v1_scale.set(v1_scale.get()-1))
sub_button.grid(row=2,column=3)


root2=tk.Toplevel(root)
root2.title("Upper Color")

label_h2=tk.Label(root2,text="Hue 2:",font=("Arial", 16))
label_h2.grid(row=0,column=0)
h2_scale=tk.Scale(root2,from_=0,to=179,orient=tk.HORIZONTAL,command=slider)
h2_scale.set(179)
h2_scale.grid(row=0,column=1)
add_button=tk.Button(root2,text="+",font=("Arial", 16),command=lambda:h2_scale.set(h2_scale.get()+1))
add_button.grid(row=0,column=2)
sub_button=tk.Button(root2,text="-",font=("Arial", 16),command=lambda:h2_scale.set(h2_scale.get()-1))
sub_button.grid(row=0,column=3)

label_s2=tk.Label(root2,text="Saturation 2:",font=("Arial", 16))
label_s2.grid(row=1,column=0)
s2_scale=tk.Scale(root2,from_=0,to=255,orient=tk.HORIZONTAL,command=slider)
s2_scale.set(255)
s2_scale.grid(row=1,column=1)
add_button=tk.Button(root2,text="+",font=("Arial", 16),command=lambda:s2_scale.set(s2_scale.get()+1))
add_button.grid(row=1,column=2)
sub_button=tk.Button(root2,text="-",font=("Arial", 16),command=lambda:s2_scale.set(s2_scale.get()-1))
sub_button.grid(row=1,column=3)



label_v2=tk.Label(root2,text="Value 2:",font=("Arial", 16))
label_v2.grid(row=2,column=0)
v2_scale=tk.Scale(root2,from_=0,to=255,orient=tk.HORIZONTAL,command=slider)
v2_scale.set(255)
v2_scale.grid(row=2,column=1)
add_button=tk.Button(root2,text="+",font=("Arial", 16),command=lambda:v2_scale.set(v2_scale.get()+1))
add_button.grid(row=2,column=2)
sub_button=tk.Button(root2,text="-",font=("Arial", 16),command=lambda:v2_scale.set(v2_scale.get()-1))
sub_button.grid(row=2,column=3)



root.mainloop()


