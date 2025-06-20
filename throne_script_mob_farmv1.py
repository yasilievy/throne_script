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
        self.do_bot = False
        self.timer  = time.time()
        self.initial_skill_list_scan = False
        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.target_check_values = 21
        self.config_file = None
        self.initialize_config()


    def initialize_config(self):
        time.sleep(0.2)
        pyautogui.hotkey('alt','tab')
        self.config_file = open('throne_script_config.txt','r+')
        config_file_read = self.config_file.read()
        if len(config_file_read) == 0:
            self.initial_skill_list_scan = True
            write_to = ''
            print('config file is empty\nstarting initialization')
            print('setting target values')
            print('please target something')
            # initial_screenshot = None
            while True:
                time.sleep(0.5)
                initial_screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
                if self.check_target(initial_screenshot):
                    print('setting target values completed')
                    write_to += f'target_value={self.target_check_values}\n' # value is set in self.check_target()
                    break
            print('setting skill list values')
            self.initialize_skill_list_check(initial_screenshot)
            write_to += f'skill_values={','.join(str(v) for v in self.skill_list_available)}'  # value is set in self.initialize_skill_list_check()
            print('setting skill list values completed')

            self.config_file.write(write_to)
            self.config_file.close()
            self.initial_skill_list_scan = False
        else:
            print('config file exists, skipping initialization')
            self.config_file.close()
            config_file_read_split = config_file_read.split('\n')
            for line in config_file_read_split:
                print(line)
                setting,value = line.split('=')
                if 'target' in setting:
                    self.target_check_values = int(value)
                if 'skill' in setting:
                    config_skill_counter = 0
                    for skill_value in value.split(','):
                        self.skill_list_available[config_skill_counter] = int(skill_value)
                        config_skill_counter+=1



    def while_loop(self, mouse_c, keyboard_c):
        if self.initial_skill_list_scan:
            time.sleep(0.3)
            pyautogui.hotkey('alt', 'tab')

        skill_dict = { # ------------------- require attention here -------------------
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: Key.f7,
            7: Key.f1,
            8: Key.f2,
            9: Key.f3,
            10: Key.f8,
            11: 'r',
            12: 't',
            13: 'x',
        }

        counter = 0

        while self.static_bool:
            no_target_counter = 0
            alter_camera_bool = True
            has_target_counter = 0

            while self.do_bot:
                if time.time() - self.timer > 1802:
                    self.keyboard.press('7')
                    self.keyboard.release('7')
                    self.timer = time.time()

                screen_shot = pyautogui.screenshot(region=(0,0,1920,1080))
                if self.check_self_mana(screen_shot)[0] < 20:
                    print('mana recovering')
                    self.keyboard.press('r')  # ------------------- require attention here -------------------
                    time.sleep(9.2)
                    self.keyboard.release('r')  # ------------------- require attention here -------------------
                if self.check_self_health(screen_shot)[0] < 20:
                    print('health recovery')
                    time.sleep(0.5)
                    # potion
                    self.keyboard.press('6')  # ------------------- require attention here -------------------
                    self.keyboard.release('6')  # ------------------- require attention here -------------------
                    time.sleep(0.5)
                    # artifact
                    self.keyboard.press('x')  # ------------------- require attention here -------------------
                    self.keyboard.release('x')  # ------------------- require attention here -------------------
                    time.sleep(0.5)
                    # guardian
                    self.keyboard.press('c')  # ------------------- require attention here -------------------
                    self.keyboard.release('c')  # ------------------- require attention here -------------------
                # check_target = self.check_target(screen_shot)
                screen_shot = pyautogui.screenshot(region=(0, 1045, 1920, 1))
                skill_status_p1, skill_status_p2, distance_status, buff_status = self.initialize_skill_list_check(
                    screen_shot)

                if buff_status != 0:
                    # print(f'casting buff {buff_status}')
                    self.keyboard.press(skill_dict[buff_status])
                    self.keyboard.release(skill_dict[buff_status])
                if self.check_target(pyautogui.screenshot(region=(1064, 810, 9, 1))):
                    has_target_counter +=1
                # if check_target[0] == 32 or check_target[0] == 31 and check_target[1] == 20 or check_target[1] == 19:
                    if self.check_target_health(pyautogui.screenshot(region=(1200, 802, 1, 1))) < 20:
                        print('is full health')
                        if skill_status_p2 != 0:
                            skill_to_use = skill_dict[skill_status_p2]
                            print(f'p2 casting skill {skill_to_use}')
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                        elif skill_status_p1 != 0:
                            skill_to_use = skill_dict[skill_status_p1]
                            print(f'p1 casting skill {skill_to_use}')
                            if skill_status_p1 == 12:
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                                time.sleep(0.1)
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                            else:
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                        else:
                            print('auto attacking')
                            self.keyboard.press(Key.f5)
                            self.keyboard.release(Key.f5)
                    else:
                        print('is not full health')
                        if skill_status_p1 != 0:
                            skill_to_use = skill_dict[skill_status_p1]
                            print(f'p1 casting skill {skill_to_use}')
                            if skill_status_p1 == 12:
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                                time.sleep(0.1)
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                            else:
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                        else:
                            print('auto attacking')
                            self.keyboard.press(Key.f5)
                            self.keyboard.release(Key.f5)
                    time.sleep(0.7)
                else:
                    no_target_counter +=1
                self.keyboard.press(Key.tab)
                self.keyboard.release(Key.tab)
                time.sleep(0.2)
                if no_target_counter == 2:
                    self.keyboard.press(Key.left)
                    no_target_counter = 0

                    # if alter_camera_bool:
                    #     self.keyboard.press(Key.left)
                    #     alter_camera_bool = False
                    # else:
                    #     self.keyboard.release(Key.left)
                    #     alter_camera_bool = True
                # if has_target_counter == 10:
                #     has_target_counter= 0
                #     self.keyboard.press(Key.tab)
                #     self.keyboard.release(Key.tab)
                # press lock-on
                # self.mouse.position = (1200, 775)  # ------------------- require attention here -------------------
                # self.mouse.click(Button.left)
                # self.mouse.position = (1250, 775)  # ------------------- require attention here -------------------
                # self.mouse.click(Button.left)
                # if no_target_counter > 2:
                #     if alter_camera_bool:
                #         self.keyboard.press(Key.right)
                #         alter_camera_bool = False
                #     else:
                #         self.keyboard.press(Key.left)
                #         alter_camera_bool = True
                #     alter_target_bool = True
                #     while self.do_bot:
                #         if alter_target_bool:
                #             self.mouse.click(Button.right)
                #             alter_target_bool = False
                #         else:
                #             self.keyboard.press(Key.tab)
                #             self.keyboard.release(Key.tab)
                #             alter_target_bool = True
                #         self.mouse.click(Button.right)
                #         if self.check_target(pyautogui.screenshot(region=(0, 0, 1920, 1080))):
                #             self.keyboard.release(Key.right)
                #             self.keyboard.release(Key.left)
                #
                #             no_target_counter = 0
                #             break
                #         time.sleep(0.1)
                # counter += 1

    def on_press(self,key):
        pass

    def on_release(self,key):
        if key == keyboard.Key.esc:
            self.static_bool = False
            return False
        if '`' in '{0}'.format(key):
            if self.do_bot:
                print('turning off script')
                self.do_bot = False
            else:
                print('turning on script')
                self.do_bot = True
        # if '+' in '{0}'.format(key):
        #     self.check_target(pyautogui.screenshot(region=(0,0,1920,1080)))



    def start_script(self):
        print("started throne script")
        t1 = threading.Thread(target=self.while_loop,args=(self.mouse,self.keyboard))
        listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()
        print("stopped throne script")


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


    def check_target_health(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        print(gray[0])
        return gray[0]
    def initialize_skill_list_check(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        attacks_p1 = [3,7,8,12]
        attacks_p2 = [4,5,6]
        distances = []
        buffs = [2]
        skill_set_list = [attacks_p1,attacks_p2,distances,buffs]
        available_skill_set_list = [0,0,0,0]
        first_inc = [0,58,57,58,58,59]
        second_inc = [0,58,58,58,58,57]

        skip_skill_slot = [1,9,10,11]
        temp_skill_skill_value = []
        skill_set_counter = 0
        for skill_set in skill_set_list:
            for skill in skill_set:
                if skill not in skip_skill_slot:
                    if skill > 6:
                        x1 = 1009
                        incre_list = second_inc
                        x1_accum = sum(incre_list[:skill-6])
                    else:
                        x1 = 605
                        incre_list = first_inc
                        x1_accum = sum(incre_list[:skill])
                    skill_pixel_value = gray[0][x1+x1_accum]
                    temp_skill_skill_value.append((skill,skill_pixel_value))
                    if int(skill_pixel_value) == self.skill_list_available[skill-1]:
                        available_skill_set_list[skill_set_counter] = skill
                        break
            skill_set_counter += 1
        print(available_skill_set_list)
        return available_skill_set_list
    # def initialize_skill_list_check(self, ss):
    #     temp_time = time.time()
    #     img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     party_box_x1 = 605   # ------------------- require attention here -------------------
    #     party_box_y1 = 1045  # ------------------- require attention here -------------------
    #
    #     party_box_x2 = party_box_x1 + 1
    #     party_box_y2 = party_box_y1 + 1
    #     first_inc = [0,58,57,58,58,59,0,58,58,58,58,57]
    #
    #     # selects which skills to skip over
    #     skip_skill_slot = [9,10,11,12]
    #
    #     non_cooldown = []
    #
    #     temp_all = []
    #     slot_count = 1
    #     accum = 0
    #
    #     inc_counter = 0
    #     for inc in first_inc:
    #         if slot_count == 7:
    #             party_box_x1 = 1009 # ------------------- require attention here -------------------
    #             party_box_x2 = party_box_x1 + 1
    #             accum = 0
    #         if slot_count not in skip_skill_slot:
    #             accum += inc
    #             img_cropped = gray[party_box_y1:party_box_y2, party_box_x1 + accum:party_box_x2 + accum]
    #             skill_value = int(img_cropped[0][0])
    #             temp_all.append((slot_count,skill_value))
    #             # print(f'{slot_count} : {skill_value}')
    #             if self.initial_skill_list_scan:
    #                 self.skill_list_available[inc_counter] = skill_value
    #             else:
    #                 if skill_value == self.skill_list_available[inc_counter]:
    #                     non_cooldown.append((slot_count,skill_value))
    #         else:
    #             accum += inc
    #         slot_count +=1
    #         inc_counter+=1
    #
    #     # # checking artifact skill
    #     # party_box_x1 = 756 # ------------------- require attention here -------------------
    #     # party_box_y1 = 981 # ------------------- require attention here -------------------
    #     # img_cropped = gray[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
    #     # skill_value = int(img_cropped[0][0])
    #     # if self.initial_skill_list_scan:
    #     #     self.skill_list_available[12] = skill_value
    #     # else:
    #     #     if skill_value == self.skill_list_available[12]:
    #     #         non_cooldown.insert(0,(13, skill_value))
    #     # print(f'available skills {non_cooldown}')
    #     if len(non_cooldown) != 0:
    #         return non_cooldown[0][0]
    #     else:
    #         return 0

    def check_self_mana(self,ss):
        temp_time = time.time()
        # ss = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 750  # ------------------- require attention here -------------------
        party_box_y1 = 825  # ------------------- require attention here -------------------
        img = img[party_box_y1:party_box_y1 + 1, party_box_x1:party_box_x1 + 1]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')

        return gray[0]

    def check_self_health(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 785  # ------------------- require attention here -------------------
        party_box_y1 = 805  # ------------------- require attention here -------------------
        img = img[party_box_y1:party_box_y1 + 1, party_box_x1:party_box_x1 + 1]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        return gray[0]

if __name__ =="__main__":

    assist = throne_script()
    assist.start_script()




    # def read_chat(self):
    #     loc = "ss\\"
    #     name = "img_shot.png"
    #     ss = pyautogui.screenshot()
    #     # ss.save(loc+name)
    #     img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
    #     party_box_x1 = 30
    #     party_box_y1 = 962
    #     party_box_x2 = 195
    #     party_box_y2 = 983
    #     img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     return pytesseract.image_to_string(gray)