import numpy as np,cv2
from PIL import Image

image_test = Image.open('alio_test.jpg')
cvt_img = cv2.cvtColor(np.array(image_test),cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)

y1 = 1273
x1 = 1280
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

counter = 1
for x_p in pixel_list:
    gray_cropped = gray[y1:y1+1,x_p:x_p+1]
    print(f'{counter}: {gray_cropped[0]}')
    counter+=1


manage_party = (31,16)
loading_screen = (1318,1008)
enter_dungeon = ()
exit_dungeon = ()