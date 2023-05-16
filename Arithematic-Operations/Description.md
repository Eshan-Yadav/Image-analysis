#Types of Arithematic Oprations on images and their uses

1.Addition:The addition operation adds the corresponding pixel values of image1 and image2 and stores the result in the result image. It can be used for tasks like image blending and intensity adjustment.

`result = cv.add(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/489d11c8-9b73-497d-98c7-552f6ece5d21)


2.Subtraction:The subtraction operation subtracts the corresponding pixel values of image2 from image1 and stores the result in the result image. It can be useful for tasks like image differencing and background removal.

`result = cv.subtract(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/146f456a-3235-4949-809f-655d8b3a6652)


3.Multiplication:The multiplication operation multiplies the corresponding pixel values of image1 and image2 and stores the result in the result image. It can be used for tasks like image blending, intensity adjustment, and creating special effects.

`result = cv.multiply(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/c85e43a4-0f3a-4c10-a008-e87e3d7a581d)


4.Division:The division operation divides the corresponding pixel values of image1 by image2 and stores the result in the result image. It can be useful for tasks like image normalization and adjusting brightness/contrast.

`result = cv.divide(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/ff1e8444-64e7-4c13-94b0-cd35e6ac352f)


5.Bitwise Operations (AND, OR, XOR, NOT):

`result = cv.bitwise_and(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/0aba32a8-2a87-49c2-8016-fa4a6ed5c6d5)


`result = cv.bitwise_or(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/ac569439-a29d-41a9-b8bd-7fbda0ab75d8)

`result = cv.bitwise_xor(image1, image2)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/9c3f435b-fda0-4cca-92fd-97e9f5b82837)

`result = cv.bitwise_not(image)`

![image](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/fdfbc53f-bd82-40ad-9f52-4baa8acd367e)

The bitwise operations perform element-wise logical operations between the pixels of the input images. They are commonly used for tasks like image masking, combining masks, and creating special effects.



Original images:
*First:*

![tut1](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/20d89ebb-d0ec-45ea-97c8-e3c46c4425fe)

*Second:*

![tut2](https://github.com/Eshan-Yadav/Image-analysis/assets/76656875/60eeaaad-f25b-43a7-b391-b5c6edec2147)


