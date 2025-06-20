import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import ImageGrab
from collections import Counter

pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'


class throne_script:
    def __init__(self):
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.do_script = True
        self.do_fish = False
        self.screen_shot_counter = 0
    def while_loop(self):
        cast_bool = True
        reel_bool = True
        while self.do_script:
            cast_bool = True
            reel_bool = True
            drag_bool = False
            while self.do_fish:
                if drag_bool:
                    # fish_test = open('fish_test\\fish_test.txt', 'w')
                    # write_to = ''W
                    print('dragging')
                    cast_bool = True
                    left_button_hold = False
                    right_button_hold = False
                    time.sleep(0.2)
                    while self.do_fish:
                        temp_time = time.time()
                        screen_shot = pyautogui.screenshot(region=(760, 78, 200, 1))
                        img = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                        left_counter = Counter(im_bw[0][:75])[255]
                        right_counter = Counter(im_bw[0][125:])[255]
                        screen_shot = pyautogui.screenshot(region=(1138, 708, 1, 1)) # need config - stamina
                        if self.check_stamina(screen_shot)[0] >= 39:
                            # print('stamina ready')
                            if left_counter > right_counter:
                                if right_button_hold:
                                    pass
                                else:
                                    print(f'{left_counter} {right_counter} pulling right')
                                    self.keyboard.release('a')
                                    left_button_hold = False
                                    right_button_hold = True
                                    self.keyboard.press('d')
                            elif left_counter < right_counter:
                                if left_button_hold :
                                    pass
                                else:
                                    print(f'{left_counter} {right_counter} pulling left')
                                    self.keyboard.release('d')
                                    left_button_hold = True
                                    right_button_hold = False
                                    self.keyboard.press('a')
                            else:
                                print(f'{left_counter} {right_counter} staying idle')
                                if left_button_hold:
                                    self.keyboard.release('a')
                                    left_button_hold = False
                                if right_button_hold:
                                    right_button_hold = False
                                    self.keyboard.release('d')
                        else:
                            print('stamina depleted, resting')
                            if left_button_hold:
                                self.keyboard.release('a')
                                left_button_hold = False
                            if right_button_hold:
                                right_button_hold = False
                                self.keyboard.release('d')
                            time.sleep(0.2)
                        screen_shot = pyautogui.screenshot(region=(1138, 593, 1, 1)) # need config - dragging status
                        dragging_status = self.check_dragging_status(screen_shot)[0]
                        print(dragging_status)
                        if dragging_status != 95:
                            print('done_fishing')
                            drag_bool = False
                            self.keyboard.release('a')
                            self.keyboard.release('d')
                            break
                        # print(f'dragging {time.time() - temp_time}')
                    # fish_test.write(write_to)
                    # fish_test.close()
                else:
                    screen_shot = pyautogui.screenshot(region=(1200, 650, 75, 20)) # need config - detect cast
                    if cast_bool and 'cast' in self.check_cast_float(screen_shot).lower():
                        print('casting')
                        cast_bool = False
                        reel_bool = True
                        self.keyboard.press('f')
                        self.keyboard.release('f')
                        while self.do_fish:
                            temp_time = time.time()
                            screen_shot = pyautogui.screenshot(region=(939, 716, 1, 1)) # need config - detect reel
                            reel_check_one = self.check_reel_in(screen_shot)[0] == 159
                            screen_shot = pyautogui.screenshot(region=(942, 716, 3, 1)) # need config - detect reel 2
                            reel_check_two = True
                            for reel_value in self.check_reel_in(screen_shot):
                                if reel_value != 4:
                                    reel_check_two = False
                            if reel_bool and reel_check_two and reel_check_one:
                                print('reeling')
                                reel_bool = False
                                drag_bool = True
                                self.keyboard.press('q')
                                self.keyboard.release('q')
                                break
                            # print(f'waiting to reel {time.time() - temp_time}')
                    # print(f'waiting to cast {time.time() - temp_time}')
    def read_chat(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)

    def check_green_indicator(self,ss):
        pass
    def check_reel_in(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray[0]

    def check_dragging_status(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray[0]
    def check_stamina(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray[0]
    def check_cast_float(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)
    def on_press(self, key):
        pass
    def on_release(self, key):
        if '`' in '{0}'.format(key):
            if self.do_fish:
                print('turning off fish')
                self.do_fish = False
            else:
                print('turning on fish')
                self.do_fish = True
        if key == keyboard.Key.esc:
            self.static_bool = False
            return False
        if '+' in '{0}'.format(key):
            screen_shot = pyautogui.screenshot()
            screen_shot.save(f'fishing_screen_shot{self.screen_shot_counter}.png')
            self.screen_shot_counter +=1

    def start_assist(self):
        print("started throne script")
        t1 = threading.Thread(target=self.while_loop)
        listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()

if __name__ == "__main__":
    assist = throne_script()
    assist.start_assist()