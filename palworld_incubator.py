import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import ImageGrab


class throne_script:
    def __init__(self):
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.starting_coord = (303, 256)
        self.x_incre = 88
        self.y_incre = 88
        self.x_slots = 6
        self.y_slots = 7

    def start_incubate(self, mouse_c, keyboard_c):
        pass



    def check_target(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.initial_skill_list_scan:
            constant_value = gray[0][0]
            for value in gray[0]:
                if constant_value != value:
                    return False
            self.target_check_values = constant_value
            return True
        else:
            for value in gray[0]:
                if self.target_check_values != value and value != 116:
                # if value != 42: #42:
                    # print(gray[0])
                    return False
            return True

    def initialize_pixels(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for



if __name__ =="__main__":

    assist = throne_script()
    assist.start_incubate()
