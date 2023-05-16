import cv2 as cv

img1=cv.imread('tut1.jpeg')
img1=cv.resize(img1,(512,512))
img2=cv.imread('tut2.jpeg')
img2=cv.resize(img2,(512,512))


img3=cv.add(img1,img2)
cv.imshow('image add',img3)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()

img4=cv.subtract(img1,img2)
cv.imshow('image sub',img4)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()

img5=cv.multiply(img1,img2)
cv.imshow('image mul',img5)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()


img6=cv.divide(img1,img2)
cv.imshow('image div',img6)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()

img7=cv.bitwise_and(img1,img2)
cv.imshow('image and',img7)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()

img8=cv.bitwise_or(img1,img2)
cv.imshow('image or',img8)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()

img9=cv.bitwise_xor(img1,img2)
cv.imshow('image xor',img9)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()

img10=cv.bitwise_not(img1)
cv.imshow('image not',img10)
k=cv.waitKey(0)
if(k==ord('q')):
    cv.destroyAllWindows()



