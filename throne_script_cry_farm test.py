import pyautogui, time, numpy as np, threading,cv2
# import pytesseract, pyautogui, time, numpy as np, threading,cv2

from pynput.keyboard import Key
from pynput.mouse import Button
from pynput import keyboard, mouse
# pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'


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
        self.current_key = None
        self.counter = -1
        self.skill_list = {'cleaving moonlight 1':[0.4,'1',0],
                           'cleaving moonlight 2': [0.3, '1', 0],

                           'death blow 1 hold': [0.8, '2', 0.8],
                           'death blow 2 hold': [0.8, '2', 1.2],
                           'death blow fire': [0.1, '2', 0],

                           'guillotine blade hold': [1.3, '3', 1.2],
                           'guillotine blade fire': [0.1, '3', 0],

                           'shadow strike': [0.3, '4', 0],

                           'precision dash ini': [0.1, '4', 0],
                           'precision dash': [0.4, '4', 0],

                           'thundering bomb': [0.6, '5', 0],
                           'ascending slash': [0.6, '5', 0],

                           'stunning blow': [0.5, '7', 0],
                           'stunning blow fire': [0.1, '7', 0],

                           'frost cleaving': [1, '8', 0],
                           'frost cleaving fire': [0.1, '8', 0],

                           'umbral spirit': [0.4, 'q', 0],

                           'valiant brawl fire': [0.1, Key.f7, 1],
                           'valiant brawl 1': [1, '5', 0],
                           'valiant brawl 2': [1, Key.f7, 0],
                           'fatal stigma': [0.4, 'r', 0],

                           'willbreaker': [0.4, '-', 0],

                           'lighting infusion': [0.3, '=', 0],

                           'lighting infusion fire': [0.1, '=', 0],
                           }


    def while_loop(self,mouse_c,keyboard_c):
        pyautogui.hotkey('alt', 'tab')

        # movespeed 786
        # attackspeed 37.4%
        # counter = 0
        while self.static_bool:
            timer = None
            counter = -1
            start_boo = False
            while self.do_move:
                if counter == -1:
                    timer = time.time()
                    if start_boo:
                        pass
                    else:
                        self.keyboard.press(Key.enter)
                        self.keyboard.release(Key.enter)
                        time.sleep(0.7)

                    self.mouse.position = (19,12)
                    self.mouse.click(Button.left)
                    time.sleep(0.7)
                    self.mouse.position = (445,330)
                    self.mouse.click(Button.left)
                    time.sleep(0.7)
                    self.keyboard.press(Key.f11)
                    self.keyboard.release(Key.f11)
                    time.sleep(0.7)
                    self.mouse.position = (1700, 580)
                    self.mouse.click(Button.left)
                    time.sleep(0.7)
                    self.mouse.position = (960,1000)
                    self.mouse.click(Button.left)
                    # time.sleep(1)
                    time.sleep(9)
                    print('phase 1 done')
                if counter == 0:
                    self.keyboard.press('a')
                    time.sleep(0.5)
                    self.keyboard.release('a')
                    time.sleep(0.1)
                    self.do_skill('prescision dash')
                    self.do_skill('prescision dash')
                    # self.keyboard.press('/')
                    # self.keyboard.release('/')
                    time.sleep(0.1)
                    self.keyboard.press(Key.shift)
                    self.keyboard.release(Key.shift)
                    time.sleep(2)
                if counter == 1:
                    self.keyboard.press(Key.f7)
                    self.keyboard.release(Key.f7)
                    time.sleep(0.1)
                    self.keyboard.press('/')
                    self.keyboard.release('/')
                    time.sleep(5.5)
                    self.keyboard.press('d')
                    self.keyboard.press('w')
                    time.sleep(4.4)
                if counter == 2:
                    self.keyboard.release('d')
                    # self.keyboard.release('w')
                    # self.keyboard.press('/')
                    # self.keyboard.release('/')
                    # time.sleep(3.6)
                    # self.keyboard.press('q')
                    # self.keyboard.release('q')
                    # time.sleep(0.3)
                    # self.keyboard.press(Key.shift)
                    # self.keyboard.release(Key.shift)
                    # time.sleep(6.6)
                    time.sleep(15)
                    # time.sleep(self.buff_multiplier)
                    self.keyboard.release('w')
                    # self.keyboard.press('/')
                    # self.keyboard.release('/')
                    print('phase 2 done')

                if counter == 3:
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)
                    # self.mouse.click(Button.right)
                    # time.sleep(0.1)
                    # self.mouse.click(Button.right)
                    # time.sleep(0.1)
                    # self.mouse.click(Button.right)
                    # time.sleep(0.1)
                    self.keyboard.press('d')
                    time.sleep(0.25)
                    self.keyboard.release('d')
                    time.sleep(1)
                    check_one, check_two = self.check_target()
                    # print(str(check_one) + ' ' + str(check_two))
                    if check_one == 50 and check_two == 36:
                        print('found raid boss, performing combo')
                        self.keyboard.press('x')
                        time.sleep(0.1)
                        self.keyboard.release('x')
                        time.sleep(0.1)
                        self.do_skill('lighting infusion')
                        self.do_skill('umbral spirit')
                        self.do_skill('precision dash')
                        self.do_skill('valiant brawl 1')
                        self.do_skill('cleaving moonlight 2')
                        self.do_skill('death blow 1 hold')
                        self.do_skill('precision dash')
                        self.do_skill('cleaving moonlight 1')
                        self.do_skill('lighting infusion')
                        self.do_skill('willbreaker')
                        self.do_skill('stunning blow')
                        self.do_skill('frost cleaving fire')
                        self.do_skill('frost cleaving')
                        self.do_skill('guillotine blade hold')
                        self.do_skill('cleaving moonlight 1')
                        self.do_skill('fatal stigma')
                        self.do_skill('cleaving moonlight 1')
                        self.do_skill('precision dash')
                        self.do_skill('precision dash')
                        self.do_skill('valiant brawl 1')
                        self.do_skill('death blow 1 hold')
                    else:
                        print('did not find raid boss successfully, attempting to exit')
                        print(f'raid time attempt: {time.time() - timer}')
                        self.keyboard.press(Key.enter)
                        self.keyboard.release(Key.enter)
                        while True:
                            time.sleep(0.1)
                            chat_read = self.read_chat()
                            if 'safe' in chat_read or 'left' in chat_read or 'expired' in chat_read:
                                print('successfully exited dungeon')
                                start_boo = True
                                break
                            else:
                                time.sleep(0.3)
                                self.mouse.position = (1870, 280)
                                self.mouse.click(Button.left)
                                time.sleep(0.3)
                                self.keyboard.press('y')
                                self.keyboard.release('y')
                                time.sleep(10)

                        counter = -2

                    print('phase 3 done')

                if counter == 4:
                    while True:
                        if self.check_target()[0] == 50 and self.check_target()[1] == 36:
                            print('raid boss is not dead yet, double tapping')
                            self.do_skill('cleaving moonlight 1')
                            self.do_skill('cleaving moonlight 1')
                            self.do_skill('valiant brawl 1')
                            self.do_skill('death blow 1 hold')
                            self.do_skill('lighting infusion')
                            self.do_skill('lighting infusion')
                        else:
                            print('raid boss has died')
                            break
                    print('phase 4 done')

                if counter == 5:
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                    while True:
                        time.sleep(0.1)

                        chat_read = self.read_chat()
                        print(chat_read)
                        if 'safe' in chat_read or 'left' in chat_read or 'expired' in chat_read:
                            print('successfully exited dungeon')
                            print(f'raid time: {time.time() - timer}')
                            start_boo = True
                            break
                        else:
                            print('attempting to exit dungeon after successful raid')
                            time.sleep(0.3)
                            self.mouse.position = (1870, 280)
                            self.mouse.click(Button.left)
                            time.sleep(0.3)
                            self.keyboard.press('y')
                            self.keyboard.release('y')
                            time.sleep(5)
                    counter = -2
                    print('phase 5 done')
                counter += 1



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
                counter += 1
                print('finished combo')

            if self.do_exit:
                while True:
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                    time.sleep(0.1)
                    chat_read = self.read_chat()
                    if 'safe' in chat_read or 'left' in chat_read:
                        self.do_move = False
                        break
                    else:
                        time.sleep(0.3)
                        self.mouse.position = (1870, 280)
                        self.mouse.click(Button.left)
                        time.sleep(0.3)
                        self.keyboard.press('y')
                        self.keyboard.release('y')
                        time.sleep(5)
                self.do_exit = False
                print('finished exit')

            if self.do_nav:
                self.keyboard.press(Key.alt)
                self.keyboard.release(Key.alt)
                time.sleep(0.3)
                self.mouse.position = (19,12)
                self.mouse.click(Button.left)
                time.sleep(0.3)
                self.mouse.position = (445,330)
                self.mouse.click(Button.left)
                time.sleep(0.3)
                self.keyboard.press(Key.f11)
                self.keyboard.release(Key.f11)
                time.sleep(0.3)
                self.mouse.position = (1700,580)
                self.mouse.click(Button.left)
                time.sleep(0.3)
                self.mouse.position = (960,1000)
                self.mouse.click(Button.left)
                time.sleep(1)
                self.keyboard.press(Key.alt)
                self.keyboard.release(Key.alt)
                self.do_nav = False
                print('finished navigation')
            time.sleep(1)

    def do_skill(self,skill_name):
        skill_duration, key_press, key_press_duration = self.skill_list[skill_name]
        if 'hold' in skill_name:
            self.keyboard.press(key_press)
            time.sleep(key_press_duration)
            self.keyboard.release(key_press)
            time.sleep(skill_duration)
        else:
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
        if '`' in '{0}'.format(key):

            if self.do_combo:
                print('stopping script')
                self.do_combo = False
            else:
                print('starting script')
                self.do_combo = True
        # if '-' in '{0}'.format(key):
        #     print('perform navigation')
        #     if self.do_nav:
        #         self.do_nav = False
        #     else:
        #         self.do_nav = True
        if '+' in '{0}'.format(key):
            print('perform exit')
            if self.do_exit:
                self.do_exit = False
            else:
                self.do_exit = True
        if '*' in '{0}'.format(key):
            print('perform full')
            if self.do_move:
                self.do_move = False
            else:
                self.do_move = True
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
        party_box_y1 = 942
        party_box_x2 = 195
        party_box_y2 = 983
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # return pytesseract.image_to_string(gray)


if __name__ =="__main__":
    melee_assist = throne_script()
    melee_assist.start_assist()
