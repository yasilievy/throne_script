import os, sys, cv2, pytesseract, pyautogui, time, numpy as np, threading
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from vessel_reader import vessel_reader
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'

# class text_reader:
#     def __init__(self):
#         self.chat_box_x1 =
#         # self.chat_box_y1 = 410
#         self.chat_box_y1 = 690
#         self.chat_box_x2 = 340
#         self.chat_box_y2 = 859
#
#         self.target_box_x1 = 360
#         self.target_box_y1 = 725
#         self.target_box_x2 = 480
#         self.target_box_y2 = 740
#
#         # self.party_box_x1 =
#         # self.party_box_x2 =
#         # self.party_box_y1 =
#         # self.party_box_y2 =
#
#
#     def read_text(self):
#         # temp_time = time.time()
#
#         loc = "ss\\"
#         # name = "img" + str(no) + ".png"
#         name = "img_shot.png"
#         ss = pyautogui.screenshot()
#
#         img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
#
#         img = img[target_box_y1:target_box_y2, target_box_x1:target_box_x2]
#
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#         # cv2.imwrite(loc + "threshold" + name, thresh1)
#
#         # Specify structure shape and kernel size.
#         # Kernel size increases or decreases the area
#         # of the rectangle to be detected.
#         # A smaller value like (10, 10) will detect
#         # each word instead of a sentence.
#         # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
#
#         # print(f'rect_kernel {time.time() - temp_time}')
#         # dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
#         contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#         im2 = img.copy()
#         text = ""
#         # print(f'before contours {time.time() - temp_time}')
#
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
#
#             # Drawing a rectangle on copied image
#             rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#             # Cropping the text block for giving input to OCR
#             cropped = im2[y:y + h, x:x + w]
#
#             # Open the file in append mode
#             # file = open("recognized.txt", "w+")
#
#             # Apply OCR on the cropped image
#             text = pytesseract.image_to_string(cropped)
#             # print(text)
#         # print(f'after contours {time.time() - temp_time}')
#         return (text)




class assist_melee:
    def __init__(self,pyautogui,button):
        self.vessel_reader = vessel_reader()
        self.static_bool = True
        self.mouse = Controller()
        self.button = button
        self.pyautogui = pyautogui
        self.y_coord = 0
        self.constant_x = 1116
        self.pause_boolean = False



    def initialize_target_assist(self):
        increment = 35
        initial_y = 505
        while True:
            party_coord_list_quest = 'party target:\n1\t2\n3\t4\n5\t6\n7\t8\n'
            select_op =  input(party_coord_list_quest)
            # print(int(select_op) >=9)
            if select_op.isnumeric() and int(select_op)>=0 and int(select_op)<=8:
                self.y_coord = ((int(select_op)-1) * increment) + initial_y
                break
            else:
                print('select an appropriate target')

    def on_press(self,key):
        # print('{0}'.format(key))
        pass

    def on_release(self,key):
        # print('{0} pressed'.format(key))
        if key == Key.esc:
            self.static_bool = False
            return False
        if key == Key.f12:
            print('pausing')
            if self.pause_boolean:
                self.pause_boolean = False
            else:
                self.pause_boolean = True

        if key == Key.f11:
            self.pause_boolean = True
            print('changing target')
            self.initialize_target_assist()
            self.pause_boolean = False


    def while_loop(self,controller):
        pyautogui.hotkey('alt', 'tab')
        # follow_after_dead_bool = True
        while self.static_bool:
            if self.pause_boolean:
                pass
                # pyautogui.hotkey('alt','tab')
                # input()
                # self.pause_boolean = False
                # pyautogui.hotkey('alt', 'tab')
            else:
                controller.position = (self.constant_x, self.y_coord)
                controller.click(self.button.right)
                controller.click(self.button.right)
                # controller.click(self.button.left)
                # pyautogui.press('f2')

                target_health = self.vessel_reader.flash_vessel('target')
                # print(target_health)
                # if target_health[2] == 45:
                #     controller.position = (self.constant_x, self.y_coord)
                #     controller.click(self.button.left)
                #     controller.click(self.button.left)
                # else:
                #     controller.position = (self.constant_x, self.y_coord)
                #     controller.click(self.button.right)
                #     controller.click(self.button.right)

                if target_health[60] ==113:
                    pyautogui.press('f3')

                    controller.position = (self.constant_x, self.y_coord)
                    controller.click(self.button.right)
                    controller.click(self.button.right)

                # pyautogui.press('f5')

            time.sleep(1)

    def start_assist(self):
        print("started assist")
        self.initialize_target_assist()
        t1 = threading.Thread(target=self.while_loop,args=(self.mouse,))
        listener_key = Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()

        print('stopped assist')



if __name__ =="__main__":

    melee_assist = assist_melee(pyautogui,Button)
    melee_assist.start_assist()
    # vessel_reader = vessel_reader()
    # temp = ''
    # while True:
    #     try:
    #         temp = input('coords:\n')
    #         print(f'temp {temp}')
    #         array = temp.split(' ')
    #         print(f'temp {array}')
    #         converted = [int(c) for c in array]
    #         print(f'temp {converted}')
    #         xx1, yy1, xx2, yy2 = converted
    #         vessel_reader.flash_vessel(xx1, yy1, xx2, yy2)
    #     except Exception as e:
    #         print(e)

