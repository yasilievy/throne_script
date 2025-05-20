import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'E:\\OCR\\tesseract.exe'


class throne_script:
    def __init__(self):
        self.static_bool = True
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.do_bot = False
        self.timer = None
        self.initial_skill_list_scan = False
        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.target_check_values = 0
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
        self.timer = time.time()
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
            11: 'e',
            12: 'r',
            13: 'x',
        }

        counter = 0
        while self.static_bool:
            if time.time() - self.timer > 1802:
                self.keyboard.press('7')
                self.keyboard.release('7')
                self.timer = time.time()
            while self.do_bot:
                    screen_shot = pyautogui.screenshot(region=(0,0,1920,1080))
                    # check_target = self.check_target(screen_shot)
                    skill_status, distance_status, buff_status = self.initialize_skill_list_check(screen_shot)
                    if self.check_target_health(screen_shot) < 20:
                        if skill_status != 0:
                            skill_to_use = skill_dict[skill_status]
                            print(f'casting attack skill {skill_to_use}')
                            if buff_status != 0:
                                self.keyboard.press(skill_dict[buff_status])
                                self.keyboard.release(skill_dict[buff_status])
                            else:
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)

                    # if self.check_target(screen_shot):
                    # # if check_target[0] == 32 or check_target[0] == 31 and check_target[1] == 20 or check_target[1] == 19:
                    #     skill_status = self.initialize_skill_list_check(screen_shot)
                    #     # skill_status = self.check_skills(screen_shot)
                    #     if skill_status != 0:
                    #         skill_to_use = skill_dict[skill_status]
                    #         print(f'casting skill {skill_to_use}')
                    #         self.keyboard.press(skill_to_use)
                    #         self.keyboard.release(skill_to_use)
                            if self.check_self_mana(screen_shot)[0] < 20:
                                print('mana recovering')
                                self.keyboard.press('r') # ------------------- require attention here -------------------
                                time.sleep(9.2)
                                self.keyboard.release('r') # ------------------- require attention here -------------------
                            if self.check_self_health(screen_shot)[0] < 20:
                                print('health recovery')
                                time.sleep(0.5)
                                # potion
                                self.keyboard.press('6') # ------------------- require attention here -------------------
                                self.keyboard.release('6') # ------------------- require attention here -------------------
                                time.sleep(0.5)
                                # artifact
                                self.keyboard.press('x') # ------------------- require attention here -------------------
                                self.keyboard.release('x') # ------------------- require attention here -------------------
                                time.sleep(0.5)
                                # guardian
                                self.keyboard.press('c') # ------------------- require attention here -------------------
                                self.keyboard.release('c') # ------------------- require attention here -------------------
                        else:
                            print('auto attacking')
                            self.keyboard.press(Key.f5)
                            self.keyboard.release(Key.f5)
                        time.sleep(0.7)
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)
                    time.sleep(0.2)
                    # press lock-on
                    self.mouse.position = (1200, 775)  # ------------------- require attention here -------------------
                    self.mouse.click(Button.left)
                    self.mouse.position = (1250, 775)  # ------------------- require attention here -------------------
                    self.mouse.click(Button.left)
                    counter += 1

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

    def initialize_skill_list_check(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        party_box_x1 = 605
        party_box_y1 = 1045

        party_box_x2 = party_box_x1 + 1
        party_box_y2 = party_box_y1 + 1
        first_inc = [0,58,57,58,58,59,0,58,58,58,58,57]

        # skip_skill_slot = [9,10,11,12]

        skip_skill_slot = []

        attacks = [4,5,6,7,8,9]
        distances = [10,11,12]
        buffs = [1,2,3]

        available_attacks = []
        available_distances = []
        available_buffs = []

        temp_all = []
        slot_count = 1
        accum = 0

        inc_counter = 0
        for inc in first_inc:

            if slot_count == 7:
                # party_box_x1 = 1016
                party_box_x1 = 1009
                party_box_x2 = party_box_x1 + 1
                accum = 0
            if slot_count not in skip_skill_slot:
                accum += inc
                img_cropped = gray[party_box_y1:party_box_y2, party_box_x1 + accum:party_box_x2 + accum]
                skill_value = int(img_cropped[0][0])
                temp_all.append((slot_count,skill_value))
                # print(f'{slot_count} : {skill_value}')
                if self.initial_skill_list_scan:
                    self.skill_list_available[inc_counter] = skill_value
                else:
                    if skill_value == self.skill_list_available[inc_counter]:
                        if slot_count in attacks:
                            available_attacks.append((slot_count,skill_value))

                        if slot_count in distances:
                            available_distances.append((slot_count,skill_value))
                        if slot_count in buffs:
                            available_buffs.append((slot_count,skill_value))

            slot_count +=1
            inc_counter+=1

        # print('|'.join(str(n) for n in temp_all))
        self.initial_skill_list_scan = False
        # print(f'available skills {non_cooldown}')
        return_command = []
        if len(available_attacks) != 0:
            return_command.append(available_attacks[0][0])
        else:
            return_command.append(0)
        if len(available_distances) !=0:
            return_command.append(available_distances[0][0])
        else:
            return_command.append(0)
        if len(available_buffs) !=0:
            return_command.append(available_buffs[0][0])
        else:
            return_command.append(0)
        return return_command


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
        party_box_x1 = 1228  # ------------------- require attention here -------------------
        party_box_y1 = 795   # ------------------- require attention here -------------------
        img = img[party_box_y1:party_box_y1+1, party_box_x1:party_box_x1 + 12]
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
                if self.target_check_values != value:
                    return False
            return True
    def initialize_skill_list_check(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        party_box_x1 = 605
        party_box_y1 = 1045

        party_box_x2 = party_box_x1 + 1
        party_box_y2 = party_box_y1 + 1
        first_inc = [0,58,57,58,58,59,0,58,58,58,58,57]

        # skip_skill_slot = [9,10,11,12]

        skip_skill_slot = []

        attacks = [3,4,5,6,7,8]
        distances = [9,10,11,12]
        buffs = [1,2]

        available_attacks = []
        available_distances = []
        available_buffs = []

        temp_all = []
        slot_count = 1
        accum = 0

        inc_counter = 0
        for inc in first_inc:

            if slot_count == 7:
                # party_box_x1 = 1016
                party_box_x1 = 1009
                party_box_x2 = party_box_x1 + 1
                accum = 0
            if slot_count not in skip_skill_slot:
                accum += inc
                img_cropped = gray[party_box_y1:party_box_y2, party_box_x1 + accum:party_box_x2 + accum]
                skill_value = int(img_cropped[0][0])
                temp_all.append((slot_count,skill_value))
                # print(f'{slot_count} : {skill_value}')
                if self.initial_skill_list_scan:
                    self.skill_list_available[inc_counter] = skill_value
                else:
                    if skill_value == self.skill_list_available[inc_counter]:
                        if slot_count in attacks:
                            available_attacks.append((slot_count,skill_value))

                        if slot_count in distances:
                            available_distances.append((slot_count,skill_value))
                        if slot_count in buffs:
                            available_buffs.append((slot_count,skill_value))

            slot_count +=1
            inc_counter+=1

        # print('|'.join(str(n) for n in temp_all))
        self.initial_skill_list_scan = False
        # print(f'available skills {non_cooldown}')
        return_command = []
        if len(available_attacks) != 0:
            return_command.append(available_attacks[0][0])
        else:
            return_command.append(0)
        if len(available_distances) !=0:
            return_command.append(available_distances[0][0])
        else:
            return_command.append(0)
        if len(available_buffs) !=0:
            return_command.append(available_buffs[0][0])
        else:
            return_command.append(0)
        return return_command

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
    #         slot_count +=1
    #         inc_counter+=1
    #
    #     # checking artifact skill
    #     party_box_x1 = 756 # ------------------- require attention here -------------------
    #     party_box_y1 = 981 # ------------------- require attention here -------------------
    #     img_cropped = gray[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
    #     skill_value = int(img_cropped[0][0])
    #     if self.initial_skill_list_scan:
    #         self.skill_list_available[12] = skill_value
    #     else:
    #         if skill_value == self.skill_list_available[12]:
    #             non_cooldown.insert(0,(13, skill_value))
    #     # print(f'available skills {non_cooldown}')
    #     if len(non_cooldown) != 0:
    #         return non_cooldown[0][0]
    #     else:
    #         return 0