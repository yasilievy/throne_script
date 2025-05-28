import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'


class throne_script:
    def __init__(self):
        self.static_bool = True
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.do_combo = False
        self.do_nav = False
        self.do_exit = False
        self.do_move = False
        self.timer = None
        self.counter = -1
        self.current_key = None
        # self.skill_list = {'cleaving moonlight 1':[0.5,'1',0],
        #                    'cleaving moonlight 2': [0.7, '1', 0],
        #                    'death blow hold': [0.7, '2', 2],
        #                    'death blow fire': [0.1, '2', 0],
        #                    'guillotine blade hold': [0.7, '3', 2],
        #                    'guillotine blade fire': [0.1, '3', 0],
        #                    'shadow strike': [0.3, '4', 0],
        #                    'precision dash ini': [0.1, '4', 0],
        #                    'precision dash': [0.3, '4', 0],
        #                    'thundering bomb': [0.5, '5', 0],
        #                    'ascending slash': [0.5, '5', 0],
        #                    'stunning blow': [0.4, Key.f1, 0],
        #                    'stunning blow fire': [0.1, Key.f1, 0],
        #                    'frost cleaving': [1, Key.f2, 0],
        #                    'umbral spirit': [0.4, Key.f3, 0],
        #                    'valiant brawl': [1.4, Key.f7, 0],
        #                    'fatal stigma': [0.3, Key.f8, 0],
        #                    'willbreaker': [0.7, 'e', 0],
        #                    'lighting infusion': [0.5, 'r', 0],
        #                    'lighting infusion fire': [0.1, 'r', 0],
        #                    }
        self.skill_list = {'cleaving moonlight 1':[0.3,'1',0],
                           'cleaving moonlight 2': [0.2, '1', 0],

                           'death blow 1 hold': [0.7, '2', 0.8],
                           'death blow 2 hold': [0.7, '2', 1.2],
                           'death blow fire': [0.1, '2', 0],

                           'guillotine blade hold': [1.2, '3', 1],
                           'guillotine blade fire': [0.1, '3', 0],

                           'shadow strike': [0.3, '4', 0],

                           'precision dash ini': [0.1, '4', 0],
                           'precision dash': [0.3, '4', 0],

                           'thundering wwdwabomb': [0.5, '5', 0],
                           'ascending slash': [0.3, '5', 0],

                           'stunning blow': [0.4, Key.f1, 0],
                           'stunning blow fire': [0.1, Key.f1, 0],

                           'frost cleaving': [0.8, Key.f2, 0],
                           'frost cleaving fire': [0.1, Key.f2, 0],

                           'umbral spirit': [0.3, Key.f3, 0],

                           'valiant brawl fire': [0.8, Key.f7, 1],
                           'valiant brawl 1': [0.8, Key.f7, 0],
                           'valiant brawl 2': [1, Key.f7, 0],
                           'fatal stigma': [0.3, Key.f8, 0],

                           'willbreaker': [0.3, 'e', 0],

                           'lighting infusion': [0.2, 'r', 0],

                           'lighting infusion fire': [0.1, 'r', 0],
                           }


    def while_loop(self,mouse_c,keyboard_c):
        pyautogui.hotkey('alt', 'tab')

        while self.static_bool:
            while self.do_combo:
                if self.counter == -1:
                    self.do_skill('lighting infusion')
                if self.counter == 0:
                    self.do_skill('umbral spirit')
                if self.counter == 1:
                    self.do_skill('precision dash')
                if self.counter == 2:
                    self.do_skill('valiant brawl 1')
                if self.counter == 3:
                    self.do_skill('cleaving moonlight 2')
                if self.counter == 4:
                    self.do_skill('death blow 1 hold')
                if self.counter == 5:
                    self.do_skill('precision dash')
                if self.counter == 6:
                    self.do_skill('cleaving moonlight 1')
                if self.counter == 7:
                    self.do_skill('lighting infusion')
                if self.counter == 8:
                    self.do_skill('willbreaker')
                if self.counter == 9:
                    self.do_skill('stunning blow')
                if self.counter == 10:
                    self.do_skill('frost cleaving fire')
                if self.counter == 11:
                    self.do_skill('frost cleaving')
                    self.do_skill('valiant brawl 1')
                if self.counter == 12:
                    self.do_skill('ascending slash')
                if self.counter == 13:
                    self.do_skill('guillotine blade hold')
                if self.counter == 14:
                    self.do_skill('cleaving moonlight 1')
                if self.counter == 15:
                    self.do_skill('fatal stigma')
                if self.counter == 16:
                    self.do_skill('cleaving moonlight 1')
                if self.counter == 17:
                    self.do_skill('precision dash')
                if self.counter == 18:
                    self.do_skill('valiant brawl 1')
                if self.counter == 19:
                    self.do_skill('death blow 1 hold')
                if self.counter == 20:
                    self.do_skill('precision dash')
                if self.counter == 21:
                    self.do_skill('cleaving moonlight 1')
                if self.counter == 22:
                    self.do_skill('cleaving moonlight 1')
                if self.counter == 23:
                    self.do_skill('lighting infusion')
                if self.counter == 24:
                    self.do_skill('lighting infusion')
                if self.counter == 25:
                    self.do_combo = False
                self.counter += 1
                print(self.counter)

    def do_skill(self,skill_name):
        skill_duration, key_press, key_press_duration = self.skill_list[skill_name]
        if 'hold' in skill_name:
            self.keyboard.press(key_press)
            time.sleep(key_press_duration)
            self.keyboard.release(key_press)
            time.sleep(skill_duration)
        else:
            # self.keyboard.press(key_press)
            # self.keyboard.release(key_press)
            # time.sleep(0.05)
            self.keyboard.press(key_press)
            self.keyboard.release(key_press)
            time.sleep(0.05)
            self.keyboard.press(key_press)
            self.keyboard.release(key_press)
            time.sleep(skill_duration)

    def on_press(self,key):
        # if key != self.current_key:
        #     # self.timer +=
        #     self.current_key = key
        #     self.timer = time.time()
        #     print('{0} pressed'.format(key))
        pass

    def on_release(self,key):
        if key == keyboard.Key.esc:
            self.static_bool = False
            return False
        if 'q' in '{0}'.format(key):
            print('perform block')
            temp_counter = self.counter
            print(temp_counter)
            if self.do_combo:
                self.do_combo = False
                time.sleep(1)
                print(temp_counter)
                self.do_combo = True
                self.counter = temp_counter

        if '`' in '{0}'.format(key):
            print('perform combo')
            if self.do_combo:
                self.do_combo = False
                self.counter = -1
            else:
                self.do_combo = True
                self.counter = -1
        # if '+' in '{0}'.format(key):
        #     print('perform exit')
        #     if self.do_exit:
        #         self.do_exit = False
        #     else:
        #         self.do_exit = True
        # if '*' in '{0}'.format(key):
        #     print('perform full')
        #     if self.do_move:
        #         self.do_move = False
        #     else:
        #         self.do_move = True
        # if '/' in '{0}'.format(key):
        #     print('text:')
        #     print(self.read_chat())







    def start_assist(self):
        print("started throne script")
        # self.one_execute(self.mouse,self.keyboard)
        t1 = threading.Thread(target=self.while_loop,args=(self.mouse,self.keyboard))
        listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()

        print('stopped throne script')

    def check_target(self):
        loc = "ss\\"
        name = "img_shot.png"
        ss = pyautogui.screenshot()
        ss.save(loc+name)
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 1033
        party_box_y1 = 792
        party_box_x2 = 1035
        party_box_y2 = 793

        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray[0]

    def read_chat(self):
        loc = "ss\\"
        name = "img_shot.png"
        ss = pyautogui.screenshot()
        ss.save(loc+name)
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 30
        party_box_y1 = 962
        party_box_x2 = 195
        party_box_y2 = 983
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)


if __name__ =="__main__":

    melee_assist = throne_script()
    melee_assist.start_assist()




    # def while_loop(self,mouse_c,keyboard_c):
    #     pyautogui.hotkey('alt', 'tab')
    #     while self.static_bool:
    #         if self.do_move:
    #             self.keyboard.press('w')
    #             time.sleep(3)
    #             self.keyboard.release('w')
    #             self.do_move = False
    #         if self.do_combo:
    #             # print('move````')
    #             self.do_skill('lighting infusion')
    #             self.do_skill('umbral spirit')
    #             # self.do_skill('shadow strike')
    #             # self.do_skill('precision dash ini')
    #             self.do_skill('precision dash')
    #             self.do_skill('willbreaker')
    #             self.do_skill('valiant brawl')
    #             self.do_skill('cleaving moonlight 1')
    #             self.do_skill('precision dash')
    #             self.do_skill('cleaving moonlight 2')
    #             # self.do_skill('stunning blow fire')
    #             # self.do_skill('stunning blow')
    #             self.do_skill('guillotine blade hold')
    #             self.do_skill('thundering bomb')
    #             self.do_skill('lighting infusion')
    #             self.do_skill('cleaving moonlight 1')
    #             self.do_skill('cleaving moonlight 1')
    #             self.do_skill('valiant brawl')
    #             self.do_skill('fatal stigma')
    #             # self.do_skill('precision dash ini')
    #             # self.do_skill('precision dash ini')
    #             self.do_skill('precision dash')
    #             self.do_skill('precision dash')
    #             self.do_skill('frost cleaving')
    #             self.do_skill('death blow hold')
    #             self.do_skill('cleaving moonlight 1')
    #             self.do_skill('cleaving moonlight 1')
    #             self.do_skill('valiant brawl')
    #             self.do_skill('thundering bomb')
    #             self.do_combo = False
    #             print('finished combo')

    # if counter == 0:
    #     self.keyboard.press('a')
    #     time.sleep(0.7)
    #     self.keyboard.release('a')
    #     time.sleep(0.3)
    #     self.keyboard.press(Key.f1)
    #     self.keyboard.release(Key.f1)
    #     time.sleep(0.3)
    # if counter == 1:
    #     self.keyboard.press('w')
    #     time.sleep(20)
    #     self.keyboard.release('w')
    #     self.keyboard.press('d')
    #     time.sleep(3.4)