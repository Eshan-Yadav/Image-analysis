import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename

#Taking image input from the user system
path_image=askopenfilename(title="Select an image")
original_image=cv.imread(path_image)

#resizing the image to 512*512
new_width = 512
height, width = original_image.shape[:2]
aspect_ratio = new_width / width
new_height = int(height * aspect_ratio)
resized_image = cv.resize(original_image, (new_width, new_height))

#creating a copy of the original image
modified_global_image=original_image.copy()
lst_operations=[]



img=resized_image.copy()
invert_contour=0

def draw_contour(im=img,*args):

    contour_img=np.copy(im)
    temp=cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    if(invert_contour==0):
        ret,thresh = cv.threshold(temp,int(slider_contour.get()),255,cv.THRESH_BINARY)
    else:
        ret,thresh = cv.threshold(temp,int(slider_contour.get()),255,cv.THRESH_BINARY_INV)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for i, contour in enumerate(contours):
            mask = np.zeros_like(img)
            cv.drawContours(mask, [contour], -1, color=255, thickness=-1)
            # avg_pixel_value = cv2.mean(img, mask=mask)[0]

        
            cv.drawContours(contour_img, [contour], -1, (0, 255, 0), 1)
            M = cv.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv.putText(contour_img, str(i), (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # cv.drawContours(contour_img, contours, -1, (0, 255, 0), 3)
    cv.imshow("contour",contour_img)





def display(img=img):
    cv.imshow("Image",img)
    draw_contour(img)

    cv.resizeWindow("Image", 512,512)

save_continue_variable = 0
reset_blur=0

save_continue_variable_morph = 0
reset_morph=0

save_continue_variable_denoise = 0
reset_denoise=0
    
#Function to blur the image--------------------------------------------------------------------------------------------------------------    
def blur():
    slider_min_median = 1
    slider_max_median = 150

    slider_min_gaussian = 1
    slider_max_gaussian = 150

    slider_min_bilateral1 = 50
    slider_max_bilateral1 = 250

    slider_min_bilateral2 = 1
    slider_max_bilateral2 = 150


    def blur_img(blur_amount_med,slider_gaussian,slider_bilateral1,slider_bilateral2,*args):
        global img
        global save_continue_variable
        global reset_blur
        im=img.copy()
        if(check_meadin_var.get()==1):
            im = cv.medianBlur(im, blur_amount_med)   
        else:
            im=cv.medianBlur(im,1)

        if(check_gaussian_var.get()==1):
            im = cv.GaussianBlur(im, (slider_gaussian, slider_gaussian), 0)
        else:
            im=cv.GaussianBlur(im,(1,1),0)  

        if(check_bilateral_var1.get()==1):
            im = cv.bilateralFilter(im, slider_bilateral2, slider_bilateral1, slider_bilateral1)
        else:
            im=cv.bilateralFilter(im,1,1,1)
        
        if(save_continue_variable==1):
            img=im
            reset_blur=0
            save_continue_variable=0
        if(reset_blur==1):
            save_continue_variable=0
            reset_blur=0
            img=resized_image.copy()

        display(im)

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




    # root.geometry("500x500")
    blur_root=tk.Toplevel()
    blur_root.title("Blur Image")
    # Median Blur-----------------------------------------------------------------------------------------------------------------------------------------
    def inc_med(*args):
        blur_slider_median.set(blur_slider_median.get() + 2)
    def dec_med(*args):
        blur_slider_median.set(blur_slider_median.get() - 2)

    check_meadin_var = tk.IntVar()
    check_meadin = tk.Checkbutton(blur_root, font=("Helvetica", 10), variable=check_meadin_var, onvalue=1,
                                offvalue=0,command=slider)
    check_meadin.grid(row=0, column=0, padx=3, pady=10)
    median=tk.Label(blur_root,text="Median Blur",font=("Helvetica", 10))
    median.grid(row=0, column=1, padx=3, pady=10)
    blur_slider_median = ttk.Scale(blur_root, from_=slider_min_median, to=slider_max_median, length=300, orient="horizontal", command=slider)
    blur_slider_median.set(0)
    blur_slider_median.grid(row=0, column=2, padx=20, pady=10)
    #button to incriment medians
    button_add = tk.Button(blur_root, text="+", command=inc_med,height=1,width=2)
    button_add.grid(row=0, column=3, padx=5, pady=10)
    button_minus = tk.Button(blur_root, text="-", command=dec_med,height=1,width=2)
    button_minus.grid(row=0, column=4, padx=5, pady=10)
    median_value_label = ttk.Label(blur_root, text="0", font=("Helvetica", 10))
    median_value_label.grid(row=0, column=5, padx=0, pady=15,sticky="we")




    # Gaussian Blur-------------------------------------------------------------------------------------------------------------------------------------------------------
    def inc_gau(*args):
        gaussian_slider.set(gaussian_slider.get() + 2)
    def dec_gau(*args):
        gaussian_slider.set(gaussian_slider.get() - 2)

    check_gaussian_var = tk.IntVar()
    check_gaussian = tk.Checkbutton(blur_root, font=("Helvetica", 10), variable=check_gaussian_var, onvalue=1,
                                    offvalue=0,command=slider)
    check_gaussian.grid(row=1, column=0, padx=3, pady=10)
    gaussian=tk.Label(blur_root,text="Gaussian Blur",font=("Helvetica", 10))
    gaussian.grid(row=1, column=1, padx=3, pady=10)
    gaussian_slider = ttk.Scale(blur_root, from_=slider_min_gaussian, to=slider_max_gaussian, length=300, orient="horizontal",command=slider)
    gaussian_slider.set(0)
    gaussian_slider.grid(row=1, column=2, padx=20, pady=10)
    #button to incriment gaussian
    button_add = tk.Button(blur_root, text="+", command=inc_gau,height=1,width=2)
    button_add.grid(row=1, column=3, padx=5, pady=10)
    button_minus = tk.Button(blur_root, text="-", command=dec_gau,height=1,width=2)
    button_minus.grid(row=1, column=4, padx=5, pady=10)
    gaussian_value_label = ttk.Label(blur_root, text="1", font=("Helvetica", 10))
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
    check_bilateral = tk.Checkbutton(blur_root, font=("Helvetica", 10), variable=check_bilateral_var1, onvalue=1,
                                    offvalue=0,command=slider)
    check_bilateral.grid(row=2, column=0, padx=3, pady=10)
    bilateral=tk.Label(blur_root,text="Bilateral Blur sigma",font=("Helvetica", 10))
    bilateral.grid(row=2, column=1, padx=3, pady=10)
    bilateral_slider1 = ttk.Scale(blur_root, from_=slider_min_bilateral1, to=slider_max_bilateral1, length=300, orient="horizontal",command=slider)
    bilateral_slider1.set(0)
    bilateral_slider1.grid(row=2, column=2, padx=20, pady=10)
    #button to incriment gaussian
    button_add = tk.Button(blur_root, text="+", command=inc_bi1,height=1,width=2)
    button_add.grid(row=2, column=3, padx=5, pady=10)
    button_minus = tk.Button(blur_root, text="-", command=dec_bi1,height=1,width=2)
    button_minus.grid(row=2, column=4, padx=5, pady=10)
    bilateral_value_label1 = ttk.Label(blur_root, text="50", font=("Helvetica", 10))
    bilateral_value_label1.grid(row=2, column=5, padx=0, pady=15,sticky="we")

    #filter argument

    bilateral=tk.Label(blur_root,text="Bilateral Blur filter",font=("Helvetica", 10))
    bilateral.grid(row=3, column=1, padx=3, pady=10)
    bilateral_slider2 = ttk.Scale(blur_root, from_=slider_min_bilateral2, to=slider_max_bilateral2, length=300, orient="horizontal",command=slider)
    bilateral_slider2.set(0)
    bilateral_slider2.grid(row=3, column=2, padx=20, pady=10)
    #button to incriment gaussian
    button_add = tk.Button(blur_root, text="+", command=inc_bi2,height=1,width=2)
    button_add.grid(row=3, column=3, padx=5, pady=10)
    button_minus = tk.Button(blur_root, text="-", command=dec_bi2,height=1,width=2)
    button_minus.grid(row=3, column=4, padx=5, pady=10)
    bilateral_value_label2 = ttk.Label(blur_root, text="1", font=("Helvetica", 10))
    bilateral_value_label2.grid(row=3, column=5, padx=0, pady=15,sticky="we")
    

    def save_continue():
        global img
        
        cv.imwrite("blur.tif",img)
        global save_continue_variable
        save_continue_variable=1
        print("save and continue")
        slider()

    save_continue=tk.Button(blur_root,text="Save and Continue",font=("Helvetica", 10),command=save_continue)
    save_continue.grid(row=5,column=0,padx=3,pady=10)

    def reset():
        global reset_blur
        reset_blur=1
        print("reset")
        slider()
    reset=tk.Button(blur_root,text="Reset",font=("Helvetica", 10),command=reset)
    reset.grid(row=5,column=1,padx=3,pady=10)

    print("Image was blurred")

    


#Function to morphological transformt the image-------------------------------------------------------------------------------------------
def morphological():
    global img
    morphological_window=tk.Toplevel(root)
    morphological_window.title("Morphological transformations")

    def kernel(*args):
        global img
        global save_continue_variable_morph
        global reset_morph
        tmp=img.copy()
        if(int(kernel_slider.get())==0):
            kernal=np.ones((1,1),np.uint8)
        else:
            if(cross.get()==1):
                kernal=cv.getStructuringElement(cv.MORPH_CROSS,(int(kernel_slider.get()),int(kernel_slider.get())))
            
            elif(ellipse.get()==1):
                kernal=cv.getStructuringElement(cv.MORPH_ELLIPSE,(int(kernel_slider.get()),int(kernel_slider.get())))
            else:
                kernal= np.ones((int(kernel_slider.get()),int(kernel_slider.get())),np.uint8)
       
        if(morph_open.get()==1):
            # print(kernal)
            tmp=cv.morphologyEx(img,cv.MORPH_OPEN,kernal)
            cv.imshow("morphological open",tmp)

        if(morph_close.get()==1):
            tmp=cv.morphologyEx(img,cv.MORPH_CLOSE,kernal)
            cv.imshow("morphological close",tmp)

        if(morph_gradient.get()==1):
            tmp=cv.morphologyEx(img,cv.MORPH_GRADIENT,kernal)
            cv.imshow("morphological gradient",tmp)

        
        if(morph_blackhat.get()==1):
            tmp=cv.morphologyEx(img,cv.MORPH_TOPHAT,kernal)
            cv.imshow("morphological tophat",tmp)
        
        
        if(morph_tophat.get()==1):
            tmp=cv.morphologyEx(img,cv.MORPH_BLACKHAT,kernal)
            cv.imshow("morphological blackhat",tmp)


        if(save_continue_variable_morph==1):
            img=tmp
            reset_morph=0
            save_continue_variable_morph=0
        if(reset_morph==1):
            save_continue_variable_morph=0
            reset_morph=0
            img=resized_image.copy()
       
        display(img)
    
        

       

        

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

    print("Image was morphed")

    def save_continue():
        global img
        cv.imwrite("morph.tif",img)
        global save_continue_variable_morph
        save_continue_variable_morph=1
        print("save and continue")
        kernel()

    save_continue=tk.Button(morphological_window,text="Save and Continue",font=("Helvetica", 10),command=save_continue)
    save_continue.grid(row=4,column=0,padx=3,pady=10)

    def reset():
        global reset_morph
        reset_morph=1
        print("reset")
        kernel()

    reset=tk.Button(morphological_window,text="Reset",font=("Helvetica", 10),command=reset)
    reset.grid(row=4,column=1,padx=3,pady=10)


#Function to denoise the image------------------------------------------------------------------------------------------------------------
def denoise():
    h_slider_min=1
    h_slider_max=50

    h_color_slider_min=1
    h_color_slider_max=50

    template_window_slider_min=1
    template_window_slider_max=50

    search_window_slider_min=1
    search_window_slider_max=50

    def denoise_img(h,h_color,template_window,search_window,*args):
        global img
        global save_continue_variable_denoise
        global reset_denoise

        im=img.copy()
        im=cv.fastNlMeansDenoisingColored(im,None,h,h_color,template_window,search_window)

        if(save_continue_variable_denoise==1):
            img=im
            reset_denoise=0
            save_continue_variable_denoise=0
        if(reset_denoise==1):
            save_continue_variable_denoise=0
            reset_denoise=0
            img=resized_image.copy()
        
        display(im)

        


    def slider(*args):
        slider_h=int(h_slider.get())
        slider_h_color=int(h_color_slider.get())
        slider_template_window=int(template_window_slider.get())
        slider_search_window=int(search_window_slider.get())
        

        denoise_img(slider_h,slider_h_color,slider_template_window,slider_search_window)

        if slider_h % 2 == 0:
            slider_h += 1
            if slider_h > h_slider_max:
                slider_h = h_slider_max-1
            h_slider.set(slider_h)
        
        if slider_h_color % 2 == 0:
            slider_h_color += 1
            if slider_h_color > h_color_slider_max:
                slider_h_color = h_color_slider_max-1
            h_color_slider.set(slider_h_color)
        
        if slider_template_window % 2 == 0:
            slider_template_window += 1
            if slider_template_window > template_window_slider_max:
                slider_template_window = template_window_slider_max-1
            template_window_slider.set(slider_template_window)
        
        if slider_search_window % 2 == 0:
            slider_search_window += 1
            if slider_search_window > search_window_slider_max:
                slider_search_window = search_window_slider_max-1
            search_window_slider.set(slider_search_window)
        
      


    denoise_window=tk.Toplevel(root)
    denoise_label=tk.Label(root,text="fastNlMeansDenoising function ",font=("Helvetica", 10))
    denoise_label.grid(row=1, column=1, padx=3, pady=10)

    

    def inc_h(*args):
        h_slider.set(h_slider.get() + 2)
    def dec_h(*args):
        h_slider.set(h_slider.get() - 2)

    h_label=tk.Label(denoise_window,text="h",font=("Helvetica", 10))
    h_label.grid(row=1, column=0, padx=3, pady=10)
    h_slider = tk.Scale(denoise_window, from_=h_slider_min, to=h_slider_max, length=300, orient="horizontal",command=slider)
    h_slider.set(3)
    h_slider.grid(row=1, column=2, padx=20, pady=10)
    #button to incriment slider
    button_add = tk.Button(denoise_window, text="+", command=inc_h,height=1,width=2)
    button_add.grid(row=1, column=3, padx=5, pady=10)
    button_minus = tk.Button(denoise_window, text="-", command=dec_h,height=1,width=2)
    button_minus.grid(row=1, column=4, padx=5, pady=10)
    

    
    def inc_h_color(*args):
        h_color_slider.set(h_color_slider.get() + 2)
    def dec_h_color(*args):
        h_color_slider.set(h_color_slider.get() - 2)    

    h_color_label=tk.Label(denoise_window,text="h_color",font=("Helvetica", 10))
    h_color_label.grid(row=2, column=0, padx=3, pady=10)
    h_color_slider = tk.Scale(denoise_window, from_=h_color_slider_min, to=h_color_slider_max, length=300, orient="horizontal",command=slider)
    h_color_slider.set(3)
    h_color_slider.grid(row=2, column=2, padx=20, pady=10)
    #button to incriment sliders
    button_add = tk.Button(denoise_window, text="+", command=inc_h_color,height=1,width=2)
    button_add.grid(row=2, column=3, padx=5, pady=10)
    button_minus = tk.Button(denoise_window, text="-", command=dec_h_color,height=1,width=2)
    button_minus.grid(row=2, column=4, padx=5, pady=10)

    
    def inc_temp(*args):
        template_window_slider.set(template_window_slider.get() + 2)
    def dec_temp(*args):
        template_window_slider.set(template_window_slider.get() - 2)

    template_label=tk.Label(denoise_window,text="template_window",font=("Helvetica", 10))
    template_label.grid(row=3, column=0, padx=3, pady=10)
    template_window_slider=tk.Scale(denoise_window,from_=template_window_slider_min,to=template_window_slider_max,length=300,orient="horizontal",command=slider)
    template_window_slider.set(7)
    template_window_slider.grid(row=3,column=2,padx=20,pady=10)
    button_add = tk.Button(denoise_window, text="+", command=inc_temp,height=1,width=2)
    button_add.grid(row=3, column=3, padx=5, pady=10)
    button_minus = tk.Button(denoise_window, text="-", command=dec_temp,height=1,width=2)
    button_minus.grid(row=3, column=4, padx=5, pady=10)

    def inc_search(*args):
        search_window_slider.set(search_window_slider.get() + 2)
    def dec_search(*args):
        search_window_slider.set(search_window_slider.get() - 2)
    
    search_label=tk.Label(denoise_window,text="search_window",font=("Helvetica", 10))
    search_label.grid(row=4, column=0, padx=3, pady=10)
    search_window_slider=tk.Scale(denoise_window,from_=search_window_slider_min,to=search_window_slider_max,length=300,orient="horizontal",command=slider)
    search_window_slider.set(21)
    search_window_slider.grid(row=4,column=2,padx=20,pady=10)
    button_add = tk.Button(denoise_window, text="+", command=inc_search,height=1,width=2)
    button_add.grid(row=4, column=3, padx=5, pady=10)
    button_minus = tk.Button(denoise_window, text="-", command=dec_search,height=1,width=2)
    button_minus.grid(row=4, column=4, padx=5, pady=10)

    def save_continue():
        global img
        cv.imwrite("denoise.tif",img)
        global save_continue_variable_denoise
        save_continue_variable_denoise=1
        print("save and continue")
        slider()

   

    def reset():
        global reset_denoise
        reset_denoise=1
        print("reset")
        slider()

    save_continue=tk.Button(denoise_window,text="Save and Continue",command=save_continue)
    save_continue.grid(row=5,column=2,padx=20,pady=10)

    
       

    reset=tk.Button(denoise_window,text="Reset",command=reset)
    reset.grid(row=5,column=3,padx=20,pady=10)






    





    print("Image was denoised")



#Function to perform the operations--------------------------------------------------------------------------------------------------------
def operations():
    if(process1.get()!="None"):
        if(process1.get()=="Blur"):
            lst_operations.append(blur)
        elif(process1.get()=="Morphological Transform"):
            lst_operations.append(morphological)
        elif(process1.get()=="Denoise"):
            lst_operations.append(denoise)
    if(process2.get()!="None"):
        if(process2.get()=="Blur"):
            lst_operations.append(blur)
        elif(process2.get()=="Morphological Transform"):
            lst_operations.append(morphological)
        elif(process2.get()=="Denoise"):
            lst_operations.append(denoise)
    if(process3.get()!="None"):
        if(process3.get()=="Blur"):
            lst_operations.append(blur)
        elif(process3.get()=="Morphological Transform"):
            lst_operations.append(morphological)
        elif(process3.get()=="Denoise"):
            lst_operations.append(denoise)
    
    for i in lst_operations:
        i()

#Main root window--------------------------------------------------------------------------------------------------------------------------
root=tk.Tk()
root.title("Image Processing Options")

description=tk.Label(root,text="Select the mode of operation",font=("Helvetica", 19))
description.grid(row=0,column=1,columnspan=3,padx=10,pady=10)

#label for the processing order
Process1=tk.Label(root,text="1. First Process",font=("Helvetica", 13))
Process1.grid(row=1,column=0,columnspan=2,padx=5,pady=10,sticky="we")
Process2=tk.Label(root,text="2. Second Process",font=("Helvetica", 13))
Process2.grid(row=2,column=0,columnspan=2,padx=10,pady=10,sticky="we")
Process3=tk.Label(root,text="3. Third Process",font=("Helvetica", 13))
Process3.grid(row=3,column=0,columnspan=2,padx=5,pady=10,sticky="we")


#drop down for the processes
process1=tk.StringVar()
process1.set("None")
process1_options=["Blur","Morphological Transform","Denoise","None"]
process1_drop=tk.OptionMenu(root,process1,*process1_options)
process1_drop.grid(row=1,column=3,columnspan=3,padx=10,pady=10)

process2=tk.StringVar()
process2.set("None")
process2_options=["Blur","Morphological Transform","Denoise","None"]
process2_drop=tk.OptionMenu(root,process2,*process2_options)
process2_drop.grid(row=2,column=3,columnspan=3,padx=10,pady=10)

process3=tk.StringVar()
process3.set("None")
process3_options=["Blur","Morphological Transform","Denoise","None"]
process3_drop=tk.OptionMenu(root,process3,*process3_options)
process3_drop.grid(row=3,column=3,columnspan=3,padx=10,pady=10)


continue_operations=tk.Button(root,text="Continue",font=("Helvetica", 13),command=operations)
continue_operations.grid(row=4,column=1,columnspan=3,padx=10,pady=10,sticky="we")




contour_display=tk.Toplevel()
contour_display.title("Contour")
# contour_display.geometry("512x512")


def invert_contour_func(*args):
    global img
    global invert_contour
    if(invert_contour_var.get()==1):
        invert_contour=1
    else:
        invert_contour=0
    draw_contour(img)

def temp(*args):
    global img
    draw_contour(img)
invert_contour_var=tk.IntVar()
invert_contour_var.set(0)
invert_contour_check=tk.Checkbutton(contour_display,text="Invert Contour",variable=invert_contour_var,command=invert_contour_func)
invert_contour_check.grid(row=1,column=0,columnspan=3)
slider_contour = tk.Scale(contour_display, from_=0, to=255, orient=tk.HORIZONTAL, length=512, command=temp)
slider_contour.grid(row=0,column=0,columnspan=3)

root.mainloop()




