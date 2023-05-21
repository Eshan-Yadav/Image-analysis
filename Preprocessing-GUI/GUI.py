import cv2 as cv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from tkinter.filedialog import askopenfilename




slider_min_median = 1
slider_max_median = 50

slider_min_gaussian = 1
slider_max_gaussian = 50

slider_min_bilateral1 = 50
slider_max_bilateral1 = 250

slider_min_bilateral2 = 1
slider_max_bilateral2 = 50

path=askopenfilename()

update=0

img=cv.imread(path)
new_width = 512
height, width = img.shape[:2]
aspect_ratio = new_width / width
new_height = int(height * aspect_ratio)
resized_image = cv.resize(img, (new_width, new_height))
img = resized_image
final=img
morph=final

def kernel(*args):
    global morph
    global update
    
    if(int(kernel_slider.get())==0):
        kernal=np.ones((1,1),np.uint8)
    else:
        if(cross.get()==1):
            kernal=cv.getStructuringElement(cv.MORPH_CROSS,(int(kernel_slider.get()),int(kernel_slider.get())))
        
        elif(ellipse.get()==1):
            kernal=cv.getStructuringElement(cv.MORPH_ELLIPSE,(int(kernel_slider.get()),int(kernel_slider.get())))
        else:
            kernal= np.ones((int(kernel_slider.get()),int(kernel_slider.get())),np.uint8)
    img=final
    if(morph_open.get()==1):
        # print(kernal)
        img=cv.morphologyEx(final,cv.MORPH_OPEN,kernal)
        cv.imshow("morphological open",img)

    if(morph_close.get()==1):
        img=cv.morphologyEx(img,cv.MORPH_CLOSE,kernal)
        cv.imshow("morphological close",img)

    if(morph_gradient.get()==1):
        img=cv.morphologyEx(img,cv.MORPH_GRADIENT,kernal)
        cv.imshow("morphological gradient",img)

    
    if(morph_blackhat.get()==1):
        img=cv.morphologyEx(img,cv.MORPH_TOPHAT,kernal)
        cv.imshow("morphological tophat",img)
    
    
    if(morph_tophat.get()==1):
        img=cv.morphologyEx(img,cv.MORPH_BLACKHAT,kernal)
        cv.imshow("morphological blackhat",img)


    if(morph_open.get()==0 and morph_close.get()==0 and morph_gradient.get()==0 and morph_blackhat.get()==0 and morph_tophat.get()==0):
        update=0
   
      

    morph=img


def display(img):
    global final
    final=img
    cv.imshow("blurred", img)
    kernel()
   


def blur_img(blur_amount_med,slider_gaussian,slider_bilateral1,slider_bilateral2,*args):
    if(update==0):
        img=resized_image
    else:
        img=final
    if(check_meadin_var.get()==1):
        img = cv.medianBlur(img, blur_amount_med)   
    else:
        img=cv.medianBlur(img,1)

    if(check_gaussian_var.get()==1):
        img = cv.GaussianBlur(img, (slider_gaussian, slider_gaussian), 0)
    else:
        img=cv.GaussianBlur(img,(1,1),0)  

    if(check_bilateral_var1.get()==1):
        img = cv.bilateralFilter(img, slider_bilateral2, slider_bilateral1, slider_bilateral1)
    else:
        img=cv.bilateralFilter(img,1,1,1)

    
    

    
    display(img)
    

#To show the image
def slider(*args):
    slider_median = int(blur_slider_median.get())
    slider_gaussian = int(gaussian_slider.get())
    slider_bilateral1 = int(bilateral_slider1.get())
    slider_bilateral2 = int(bilateral_slider2.get())

    blur_img(slider_median,slider_gaussian,slider_bilateral1,slider_bilateral2)
    if slider_median % 2 == 0:
        slider_median += 1
        if slider_median > slider_max_median:
            slider_median = slider_max_median-1
        blur_slider_median.set(slider_median)
    
    if slider_gaussian % 2 == 0:
        slider_gaussian += 1
        if slider_gaussian > slider_max_gaussian:
            slider_gaussian = slider_max_gaussian-1
        gaussian_slider.set(slider_gaussian)
    median_value_label.configure(text= str(slider_median))
    gaussian_value_label.configure(text= str(slider_gaussian))

    if slider_bilateral1 % 2 == 0:
        slider_bilateral1 += 1
        if slider_bilateral1 > slider_max_bilateral1:
            slider_bilateral1 = slider_max_bilateral1-1
        bilateral_slider1.set(slider_bilateral1)
    bilateral_value_label1.configure(text= str(slider_bilateral1))

    if slider_bilateral2 % 2 == 0:
        slider_bilateral2 += 1
        if slider_bilateral2 > slider_max_bilateral2:
            slider_bilateral2 = slider_max_bilateral2-1
        bilateral_slider2.set(slider_bilateral2)
    bilateral_value_label2.configure(text= str(slider_bilateral2))




root = tk.Tk()
# root.geometry("500x500")
root.title("Blur Image")
# Median Blur-----------------------------------------------------------------------------------------------------------------------------------------
def inc_med(*args):
    blur_slider_median.set(blur_slider_median.get() + 2)
def dec_med(*args):
    blur_slider_median.set(blur_slider_median.get() - 2)

check_meadin_var = tk.IntVar()
check_meadin = tk.Checkbutton(root, font=("Helvetica", 10), variable=check_meadin_var, onvalue=1,
                              offvalue=0,command=slider)
check_meadin.grid(row=0, column=0, padx=3, pady=10)
median=tk.Label(root,text="Median Blur",font=("Helvetica", 10))
median.grid(row=0, column=1, padx=3, pady=10)
blur_slider_median = ttk.Scale(root, from_=slider_min_median, to=slider_max_median, length=300, orient="horizontal", command=slider)
blur_slider_median.set(0)
blur_slider_median.grid(row=0, column=2, padx=20, pady=10)
#button to incriment medians
button_add = tk.Button(root, text="+", command=inc_med,height=1,width=2)
button_add.grid(row=0, column=3, padx=5, pady=10)
button_minus = tk.Button(root, text="-", command=dec_med,height=1,width=2)
button_minus.grid(row=0, column=4, padx=5, pady=10)
median_value_label = ttk.Label(root, text="0", font=("Helvetica", 10))
median_value_label.grid(row=0, column=5, padx=0, pady=15,sticky="we")




# Gaussian Blur-------------------------------------------------------------------------------------------------------------------------------------------------------
def inc_gau(*args):
    gaussian_slider.set(gaussian_slider.get() + 2)
def dec_gau(*args):
    gaussian_slider.set(gaussian_slider.get() - 2)

check_gaussian_var = tk.IntVar()
check_gaussian = tk.Checkbutton(root, font=("Helvetica", 10), variable=check_gaussian_var, onvalue=1,
                                offvalue=0,command=slider)
check_gaussian.grid(row=1, column=0, padx=3, pady=10)
gaussian=tk.Label(root,text="Gaussian Blur",font=("Helvetica", 10))
gaussian.grid(row=1, column=1, padx=3, pady=10)
gaussian_slider = ttk.Scale(root, from_=slider_min_gaussian, to=slider_max_gaussian, length=300, orient="horizontal",command=slider)
gaussian_slider.set(0)
gaussian_slider.grid(row=1, column=2, padx=20, pady=10)
#button to incriment gaussian
button_add = tk.Button(root, text="+", command=inc_gau,height=1,width=2)
button_add.grid(row=1, column=3, padx=5, pady=10)
button_minus = tk.Button(root, text="-", command=dec_gau,height=1,width=2)
button_minus.grid(row=1, column=4, padx=5, pady=10)
gaussian_value_label = ttk.Label(root, text="1", font=("Helvetica", 10))
gaussian_value_label.grid(row=1, column=5, padx=0, pady=15,sticky="we")






# Bilateral Blur-------------------------------------------------------------------------------------------------------------------------------------------------------
def inc_bi1(*args):
    bilateral_slider1.set(bilateral_slider1.get() + 10)
def dec_bi1(*args):
    bilateral_slider1.set(bilateral_slider1.get() - 10)

def inc_bi2(*args):
    bilateral_slider2.set(bilateral_slider2.get() + 1)
def dec_bi2(*args):
    bilateral_slider2.set(bilateral_slider2.get() - 1)

check_bilateral_var1 = tk.IntVar()
check_bilateral = tk.Checkbutton(root, font=("Helvetica", 10), variable=check_bilateral_var1, onvalue=1,
                                offvalue=0,command=slider)
check_bilateral.grid(row=2, column=0, padx=3, pady=10)
bilateral=tk.Label(root,text="Bilateral Blur sigma",font=("Helvetica", 10))
bilateral.grid(row=2, column=1, padx=3, pady=10)
bilateral_slider1 = ttk.Scale(root, from_=slider_min_bilateral1, to=slider_max_bilateral1, length=300, orient="horizontal",command=slider)
bilateral_slider1.set(0)
bilateral_slider1.grid(row=2, column=2, padx=20, pady=10)
#button to incriment gaussian
button_add = tk.Button(root, text="+", command=inc_bi1,height=1,width=2)
button_add.grid(row=2, column=3, padx=5, pady=10)
button_minus = tk.Button(root, text="-", command=dec_bi1,height=1,width=2)
button_minus.grid(row=2, column=4, padx=5, pady=10)
bilateral_value_label1 = ttk.Label(root, text="50", font=("Helvetica", 10))
bilateral_value_label1.grid(row=2, column=5, padx=0, pady=15,sticky="we")

#filter argument

bilateral=tk.Label(root,text="Bilateral Blur filter",font=("Helvetica", 10))
bilateral.grid(row=3, column=1, padx=3, pady=10)
bilateral_slider2 = ttk.Scale(root, from_=slider_min_bilateral2, to=slider_max_bilateral2, length=300, orient="horizontal",command=slider)
bilateral_slider2.set(0)
bilateral_slider2.grid(row=3, column=2, padx=20, pady=10)
#button to incriment gaussian
button_add = tk.Button(root, text="+", command=inc_bi2,height=1,width=2)
button_add.grid(row=3, column=3, padx=5, pady=10)
button_minus = tk.Button(root, text="-", command=dec_bi2,height=1,width=2)
button_minus.grid(row=3, column=4, padx=5, pady=10)
bilateral_value_label2 = ttk.Label(root, text="1", font=("Helvetica", 10))
bilateral_value_label2.grid(row=3, column=5, padx=0, pady=15,sticky="we")

def save_image_morphological():
    cv.imwrite("morphological.tif",morph)
def save():
    cv.imwrite("blur.tif",final)

def update_image_morphological():
    global update
    update=1
    global morph
    final=morph
    display(final)
    # slider_cont(final)
save_image=tk.Button(root,text="Save Image",font=("Helvetica", 10),command=save)
save_image.grid(row=4, column=0, padx=3, pady=10)













# Morphological Blur-------------------------------------------------------------------------------------------------------------------------------------------------------

morphological_window=tk.Toplevel(root)
morphological_window.title("Morphological transformations")


    

def inc_kernal(*args):
    if(kernel_slider.get()<149):
        if((kernel_slider.get()+1)%2==0):
            kernel_slider.set(int(kernel_slider.get() + 2))
        else:
            kernel_slider.set(int(kernel_slider.get() + 1))
    
    kernal_label.config(text="Kernal size="+str(int(kernel_slider.get())))
    kernel()
   

def dec_kernal(*args):
    if(kernel_slider.get()>1):
        if((kernel_slider.get()-1)%2==0):
            kernel_slider.set(int(kernel_slider.get() - 2))
        else:
            kernel_slider.set(int(kernel_slider.get() - 1))
  
    kernal_label.config(text="Kernal size="+str(int(kernel_slider.get())))
    kernel()




kernal_label=tk.Label(morphological_window,text="Kernal size=0",font=("Helvetica", 10))
kernal_label.grid(row=0, column=0, padx=3, pady=10)

kernel_slider = ttk.Scale(morphological_window, from_=1, to=150, length=300, orient="horizontal")

button_add = tk.Button(morphological_window, text="+", command=inc_kernal,height=1,width=2)
button_add.grid(row=0, column=1, padx=5, pady=10)
button_minus = tk.Button(morphological_window, text="-", command=dec_kernal,height=1,width=2)
button_minus.grid(row=0, column=2, padx=5, pady=10)



morph_open = tk.IntVar()
check_morph_open = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=morph_open, onvalue=1,
                                offvalue=0,command=kernel)
check_morph_open.grid(row=2, column=0, padx=3, pady=10)
morph_open_label=tk.Label(morphological_window,text="Opening (erosion followed by dialtion)",font=("Helvetica", 10))
morph_open_label.grid(row=2, column=1, padx=3, pady=10)




morph_close = tk.IntVar()
check_morph_close = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=morph_close, onvalue=1,
                                offvalue=0,command=kernel)
check_morph_close.grid(row=3, column=0, padx=3, pady=10)
morph_close_label=tk.Label(morphological_window,text="Closing (dialation followed by erosion)",font=("Helvetica", 10))
morph_close_label.grid(row=3, column=1, padx=3, pady=10)




morph_gradient = tk.IntVar()
check_morph_gradient = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=morph_gradient, onvalue=1,
                                offvalue=0,command=kernel)
check_morph_gradient.grid(row=4, column=0, padx=3, pady=10)
morph_gradient_label=tk.Label(morphological_window,text="gradient",font=("Helvetica", 10))
morph_gradient_label.grid(row=4, column=1, padx=3, pady=10)


morph_blackhat = tk.IntVar()
check_morph_blackhat = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=morph_blackhat, onvalue=1,
                                offvalue=0,command=kernel)
check_morph_blackhat.grid(row=5, column=0, padx=3, pady=10)
morph_blackhat_label=tk.Label(morphological_window,text="blackhat",font=("Helvetica", 10))
morph_blackhat_label.grid(row=5, column=1, padx=3, pady=10)


morph_tophat = tk.IntVar()
check_morph_tophat = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=morph_tophat, onvalue=1,
                                offvalue=0,command=kernel)
check_morph_tophat.grid(row=6, column=0, padx=3, pady=10)
morph_tophat_label=tk.Label(morphological_window,text="tophat",font=("Helvetica", 10))
morph_tophat_label.grid(row=6, column=1, padx=3, pady=10)




structuring_element = tk.Label(morphological_window, text="structuring element", font=("Helvetica", 10))
structuring_element.grid(row=7, column=0, padx=0, pady=10)
cross = tk.IntVar()
check_cross = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=cross, onvalue=1,
                                offvalue=0,command=kernel)
check_cross.grid(row=7, column=1, padx=0, pady=10)
check_cross_label=tk.Label(morphological_window,text="check_cross",font=("Helvetica", 10))
check_cross_label.grid(row=7, column=2, padx=3, pady=10)

ellipse = tk.IntVar()
check_ellipse = tk.Checkbutton(morphological_window, font=("Helvetica", 10), variable=ellipse, onvalue=1,
                                offvalue=0,command=kernel)
check_ellipse.grid(row=8, column=1, padx=0, pady=10)
check_ellipse_label=tk.Label(morphological_window,text="check_ellipse",font=("Helvetica", 10))
check_ellipse_label.grid(row=8, column=2, padx=3, pady=10)

#save the image
save_image =tk.Button(morphological_window, text="Save Image", command=save_image_morphological,height=1,width=10)
save_image.grid(row=9, column=0, padx=5, pady=10)

#update the image
update_image =tk.Button(morphological_window, text="Update Image", command=update_image_morphological,height=1,width=10)
update_image.grid(row=9, column=1, padx=5, pady=10)








#Contour---------------------------------------------------------------------------------------------------------------------------
# contour_window = tk.Toplevel(root)
# contour_window.title("Contour")

# def update_slider_contour(*args):
   

# slider_contour=tk.Scale(contour_window, from_=0, to=255, length=300, orient="horizontal",command=update_slider_contour)
# slider_contour.grid(row=0, column=0, padx=3, pady=10)


root.mainloop()
