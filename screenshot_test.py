import numpy as np,cv2
from PIL import Image



y1 = 1268
x1 = 1279
x2 = 1367
x3 = 1367
x4 = 1505
x5 = 1574
x6 = 1642
x7 = 1758
x8 = 1827
x9 = 1915
x10 = 1964
x11 = 2033
x12 = 2102
pixel_list = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12]

print_string = ''
image_test = Image.open('clients/test.jpg')
cvt_img = cv2.cvtColor(np.array(image_test),cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
counter = 1
for x_p in pixel_list:
    gray_cropped = gray[y1:y1+1,x_p:x_p+1]
    # print(f'{counter}: {gray_cropped[0]}')
    print_string += str(gray_cropped[0][0]) + ' '
    counter+=1
print(print_string)
print_string = ''
image_test = Image.open('clients/test2.jpg')
cvt_img = cv2.cvtColor(np.array(image_test),cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
counter = 1
for x_p in pixel_list:
    gray_cropped = gray[y1:y1+1,x_p:x_p+1]
    # print(f'{counter}: {gray_cropped[0]}')
    print_string += str(gray_cropped[0][0]) + ' '
    counter+=1
print(print_string)
print_string = ''
image_test = Image.open('clients/test3.jpg')
cvt_img = cv2.cvtColor(np.array(image_test),cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
counter = 1
for x_p in pixel_list:
    gray_cropped = gray[y1:y1+1,x_p:x_p+1]
    # print(f'{counter}: {gray_cropped[0]}')
    print_string += str(gray_cropped[0][0]) + ' '
    counter+=1
print(print_string)
print_string = ''
image_test = Image.open('clients/test4.jpg')
cvt_img = cv2.cvtColor(np.array(image_test),cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
counter = 1
for x_p in pixel_list:
    gray_cropped = gray[y1:y1+1,x_p:x_p+1]
    # print(f'{counter}: {gray_cropped[0]}')
    print_string += str(gray_cropped[0][0]) + ' '
    counter+=1
print(print_string)
print_string = ''