import numpy as np,cv2
from PIL import Image

image_test = Image.open('clients/alio.jpg')
image_test = Image.open('combo_sequence/test.png')

cvt_img = cv2.cvtColor(np.array(image_test),cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
first_inc = [0, 58, 57, 58, 58, 59, 0, 58, 58, 58, 58, 57]
y1 = 993
second_skill_cast_x1 = 587
slot_count = 1
accum = 0
for inc in first_inc:
    if slot_count == 7:
        # party_box_x1 = 1016
        second_skill_cast_x1 = 990
        accum = 0
    accum += inc
    x1_accum = second_skill_cast_x1 + accum
    gray_cropped = gray[y1:y1 + 1, x1_accum:x1_accum + 1]

    print(f'{slot_count}: {gray_cropped[0][0]}')
    slot_count+=1



# counter = 1
# for x_p in pixel_list:
#     gray_cropped = gray[y1:y1+1,x_p:x_p+1]
#     print(f'{counter}: {gray_cropped[0][0]}')
#     counter+=1
