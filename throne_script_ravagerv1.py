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
        self.combo_to_do = 0
        self.do_nav = False
        self.do_exit = False
        self.do_move = False
        self.button_open = True
        self.button_open_two = True
        self.timer = time.time()
        self.timer_boolean = False
        self.counter = -1
        self.current_key = None
        self.do_bot = False
        self.do_dungeon = False
        self.initial_skill_list_scan = True
        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]
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
            self.initial_skill_list_scan = False

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

    def while_loop(self):
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
            14: 'c'
        }

        combo_sequence_three_str = [
            9, # umbral spirit
            4, # precision dash
            12, # inject venom
            11,  # willbreaker
            1, # cleaving moonlight
            2,  # death blow
            6,  # frenzied sword dance
            10,  # fatal stigma
            8, # gaia crash
            7,  # stunning blow
            3, # guillotine blade
        ]

        start_boo = False
        timer = None

        to_do_skill = []
        while self.static_bool:
            time.sleep(0.5)
            counter = 0
            while self.do_dungeon:
                if counter == 0:
                    timer = time.time()
                    if start_boo:
                        pass
                    else:
                        self.keyboard.press(Key.enter)
                        self.keyboard.release(Key.enter)
                        time.sleep(0.7)
                    self.mouse.position = (19,12) # ------------------- require attention here -------------------
                    self.mouse.click(Button.left)
                    time.sleep(0.7)
                    self.mouse.position = (445,330) # ------------------- require attention here -------------------
                    self.mouse.click(Button.left)
                    time.sleep(0.7)
                    self.keyboard.press(Key.f11) # ------------------- require attention here -------------------
                    self.keyboard.release(Key.f11) # ------------------- require attention here -------------------
                    time.sleep(0.7)
                    # self.mouse.position = (1700, 580)
                    # self.mouse.click(Button.left)
                    # time.sleep(0.7)
                    self.mouse.position = (960,1000) # ------------------- require attention here -------------------
                    self.mouse.click(Button.left)

                    time.sleep(6)
                    while True:
                        if self.check_loading_screen(pyautogui.screenshot(region=(0, 0, 1920, 1080)))[0] == 255:
                            break
                        time.sleep(0.5)


                if counter == 1:
                    time_helper = 1.07
                    self.keyboard.press('a')
                    # time.sleep(1)
                    self.keyboard.press('q')
                    self.keyboard.release('q')
                    self.keyboard.release('a')

                    # -------------------------------------- movement reader
                    self.timer_boolean = True
                    self.timer = time.time()
                    self.do_dungeon = False
                    # -------------------------------------- movement reader
                    #
                    # self.keyboard.press('w')
                    # self.keyboard.press(Key.shift)
                    # self.keyboard.release(Key.shift)
                    # time.sleep(3.24 * time_helper)
                    # self.keyboard.press('5')
                    # self.keyboard.release('5')
                    # time.sleep(5.61 * time_helper)
                    # self.keyboard.press('d')
                    # time.sleep(4.63 * time_helper)
                    # self.keyboard.release('d')
                    # time.sleep(4 * time_helper)
                    # self.keyboard.press('q')
                    # self.keyboard.release('q')
                    # # time.sleep(0.57 * time_helper)
                    # self.keyboard.press(Key.shift)
                    # self.keyboard.release(Key.shift)
                    # time.sleep(5.6 * time_helper)
                    # self.keyboard.release('w')

                if counter == 2:
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)
                    time.sleep(0.5)

                    skill_counter = 0
                    if self.check_target(pyautogui.screenshot(region=(0, 0, 1920, 1080))):
                        print('found target, starting combo sequence')
                        while True:
                            if skill_counter == len(combo_sequence_three_str):
                                break
                            else:
                                while True:
                                    current_combo = combo_sequence_three_str[skill_counter]
                                    screen_shot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
                                    skill_status_p1 = self.initialize_skill_list_check_list(screen_shot)[0]
                                    if len(skill_status_p1) != 0:
                                        rendered_skill_status_p1 = [s_s_p1[0] for s_s_p1 in skill_status_p1]
                                        if current_combo not in rendered_skill_status_p1:
                                            break
# ---------------------------------------------------------------- need attention
                                        elif current_combo == 2 or current_combo == 3:  # ------------------- require attention here -------------------
                                            self.keyboard.press(skill_dict[current_combo])
                                            time.sleep(1)
                                            self.keyboard.release(skill_dict[current_combo])
                                        elif current_combo == 4: # ------------------- require attention here -------------------
                                            self.keyboard.press(skill_dict[current_combo])
                                            self.keyboard.release(skill_dict[current_combo])
                                            time.sleep(0.1)
                                            self.keyboard.press(skill_dict[current_combo])
                                            self.keyboard.release(skill_dict[current_combo])
                                        else:
                                            self.keyboard.press(skill_dict[current_combo])
                                            self.keyboard.release(skill_dict[current_combo])
# ---------------------------------------------------------------- need attention

                                        time.sleep(0.1)
                            skill_counter +=1
                    else:
                        print('did not find boss successfully, attempting to exit')
                        print(f'raid time attempt: {time.time() - timer}')
                        self.keyboard.press(Key.enter)
                        self.keyboard.release(Key.enter)
                        while True:
                            time.sleep(0.1)
                            chat_read = self.read_chat()
                            if 'safe' in chat_read or 'left' in chat_read or 'expire' in chat_read:
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
                        counter = -1
                if counter == 3:
                    if self.check_target(pyautogui.screenshot(region=(0, 0, 1920, 1080))):
                        print('boss is not dead yet, double tapping')
                        while True:
                            if self.check_target(pyautogui.screenshot(region=(0, 0, 1920, 1080))):
# ---------------------------------------------------------------- need attention
                                self.keyboard.press(skill_dict[2])
                                self.keyboard.release(skill_dict[2])
                                self.keyboard.press(skill_dict[1])
                                self.keyboard.release(skill_dict[1])
                                self.keyboard.press(skill_dict[12])
                                self.keyboard.release(skill_dict[12])
                                self.keyboard.press(skill_dict[6])
                                self.keyboard.release(skill_dict[6])
# ---------------------------------------------------------------- need attention
                                time.sleep(0.3)
                            else:
                                print('boss is dead')
                                break
                    else:
                        print('boss is dead')
                    time.sleep(2)
                if counter == 4:
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                    while True:
                        time.sleep(0.1)

                        chat_read = self.read_chat()
                        print(chat_read)
                        if 'safe' in chat_read or 'left' in chat_read or 'expire' in chat_read:
                            print('successfully exited dungeon')
                            print(f'raid time: {time.time() - timer}')
                            start_boo = True
                            break
                        else:
                            print('attempting to exit dungeon after successful raid')
                            time.sleep(0.3)
                            self.mouse.position = (1870, 280) # ------------------- require attention here -------------------
                            self.mouse.click(Button.left)
                            time.sleep(0.3)
                            self.keyboard.press('y')
                            self.keyboard.release('y')
                            time.sleep(3)
                    counter = -1
                    # print('dungeon script done')
                counter +=1


            unstuck_sequence_one = [('a', 1), ('d', 1), ('d', 1)]
            unstuck_sequence_two = [('d', 1), ('a', 1), ('a', 1)]
            unstuck_sequence_bool = True
            unstuck_sequence_to_do = []

            no_target_counter = 0
            out_sight_counter = 0
            jump_counter = 0
            next_target_counter = 0
            truly_stuck_counter = 0
            alter_bool_two = True
            alter_camera_bool = True

            while self.do_bot:
                screen_shot = pyautogui.screenshot(region=(0,0,1920,1080))
                time_sleep = 0.2
                skill_status_p1,  skill_status_p2, distance_status, buff_status,  = self.initialize_skill_list_check(screen_shot)
                if buff_status != 0:
                    print(f'casting buff {buff_status}')
                    self.keyboard.press(skill_dict[buff_status])
                    self.keyboard.release(skill_dict[buff_status])
                    time_sleep = 0

                if 'sight' in self.check_target_out_sight(screen_shot):
                    self.keyboard.press('w')
                    self.keyboard.press(Key.shift)
                    self.keyboard.release(Key.shift)
                    self.keyboard.press(Key.space)
                    self.keyboard.release(Key.space)
                    unstuck_boolean = True
                    while unstuck_boolean and self.do_bot:
                        if unstuck_sequence_bool:
                            unstuck_sequence_to_do = unstuck_sequence_one
                            unstuck_sequence_bool = False
                        else:
                            unstuck_sequence_to_do = unstuck_sequence_two
                            unstuck_sequence_bool = True
                        for unstuck_move in unstuck_sequence_to_do:
                            next_target_counter += 1
                            self.keyboard.press(unstuck_move[0])
                            time.sleep(0.2)
                            self.keyboard.press(Key.space)
                            self.keyboard.release(Key.space)
                            time.sleep(unstuck_move[1])
                            self.keyboard.release(unstuck_move[0])
                            if 'sight' not in self.check_target_out_sight(
                                    pyautogui.screenshot(region=(0, 0, 1920, 1080))):
                                self.keyboard.release('w')
                                unstuck_boolean = False
                                break
                            time_sleep = 0
                if truly_stuck_counter == 30:
                    print('truly unstuck, moving back')
                    self.keyboard.press('s')
                    time.sleep(1)
                    self.keyboard.press(Key.space)
                    self.keyboard.release(Key.space)
                    time.sleep(1)
                    self.keyboard.release('s')
                    truly_stuck_counter= 0
                if next_target_counter == 2:
                    print('target next')
                    if alter_bool_two:
                        self.keyboard.press(Key.right)
                        alter_bool_two = False
                    else:
                        self.keyboard.press(Key.left)
                        alter_bool_two = False
                    alter_bool = True
                    while self.do_bot:
                        if alter_bool:
                            self.mouse.click(Button.right)
                            alter_bool = False
                        else:
                            self.keyboard.press(Key.tab)
                            self.keyboard.release(Key.tab)
                            alter_bool = True
                        self.mouse.click(Button.right)
                        if self.check_target(pyautogui.screenshot(region=(0, 0, 1920, 1080))):
                            self.keyboard.release(Key.right)
                            self.keyboard.release(Key.left)
                            break
                        time.sleep(0.1)
                    next_target_counter = 0


                screen_shot = pyautogui.screenshot(region=(0,0,1920,1080))
                if self.check_target(screen_shot):
                    truly_stuck_counter +=1
                    no_target_counter = 0
                    out_sight_counter +=1
                    if self.check_target_health(screen_shot) < 20:
                        print('damaged health, using attack skill')
                        if skill_status_p1 != 0:
                            skill_to_use = skill_dict[skill_status_p1]
                            print(f'casting attack skill {skill_to_use}')
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                        elif skill_status_p2 != 0:
                            skill_to_use = skill_dict[skill_status_p2]
                            print(f'casting attack skill {skill_to_use}')
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                        else:
                            self.keyboard.press(Key.f5)
                            self.keyboard.release(Key.f5)

                    else:
                        print('undamaged, using distance skill')
                        distance_scan = self.check_distance(pyautogui.screenshot(region=(0, 0, 1920, 1080)))
                        print(distance_scan)
                        if distance_scan == 3 and distance_status != 0:
                            skill_to_use = skill_dict[distance_status]
                            print(f'casting distance skill {skill_to_use}')
                            if skill_to_use == 'r':  # ------------------- require attention here -------------------
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                                time.sleep(0.1)
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
                            self.keyboard.press(Key.f5)  # ------------------- require attention here -------------------
                            self.keyboard.release(Key.f5)  # ------------------- require attention here -------------------
                        jump_counter += 1
                    if jump_counter == 5:
                        self.keyboard.press(Key.space)
                        self.keyboard.release(Key.space)
                        jump_counter = 0
                else:
                    jump_counter = 0
                    no_target_counter +=1
                    truly_stuck_counter = 0
                    out_sight_counter = 0
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)
                    if no_target_counter > 1:
                        if alter_camera_bool:
                            self.keyboard.press(Key.right)
                            alter_camera_bool = False
                        else:
                            self.keyboard.press(Key.left)
                            alter_camera_bool = True
                        alter_target_bool = True
                        while True:
                            if alter_target_bool:
                                self.mouse.click(Button.right)
                                alter_target_bool = False
                            else:
                                self.keyboard.press(Key.tab)
                                self.keyboard.release(Key.tab)
                                alter_target_bool = True
                            if self.check_target(pyautogui.screenshot(region=(0, 0, 1920, 1080))):
                                self.keyboard.release(Key.right)
                                self.keyboard.release(Key.left)
                                break
                            time.sleep(0.1)
                time.sleep(time_sleep)



    def on_press(self,key):
        if self.timer_boolean:
            if self.button_open:
# ---------------------------------------------------------------- need attention
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift', "'q'"]:  # ------------------- require attention here -------------------
                    self.button_open = False
                    new_time = time.time()
                    print(f'time.sleep({round(new_time - self.timer,2)} * time_helper)')
                    print(f'self.keyboard.press({'{0}'.format(key)})')
                    self.timer = new_time
            elif self.button_open_two:
                if '{0}'.format(key) in ["'w'", "'a'", "'s'", "'d'", "'5'", 'Key.shift', "'q'"]:  # ------------------- require attention here -------------------
                    self.button_open_two = False
                    new_time = time.time()
                    print(f'time.sleep({round(new_time - self.timer,2)} * time_helper)')
                    print(f'self.keyboard.press({'{0}'.format(key)})')
                    self.timer = new_time

    def on_release(self,key):
        # print('{0}'.format(key))
        if self.timer_boolean and '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift',"'q'"]:  # ------------------- require attention here -------------------
            if not self.button_open:
                self.button_open = True
                new_time = time.time()
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'"]:
                    print(f'time.sleep({round(new_time - self.timer,2)} * time_helper)')
                print(f'self.keyboard.release({'{0}'.format(key)})')
                self.timer = new_time
            elif not self.button_open_two:
                self.button_open_two = True
                new_time = time.time()
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'"]:
                    print(f'time.sleep({round(new_time - self.timer,2)} * time_helper)')
                print(f'self.keyboard.release({'{0}'.format(key)})')
                self.timer = new_time
        if key == keyboard.Key.esc:
            self.static_bool = False
            return False

        if '`' in '{0}'.format(key):  # ------------------- require attention here -------------------
            if self.do_bot:
                print('turning off script')
                self.do_bot = False
            else:
                print('turning on script')
                self.do_bot = True
        if '*' in '{0}'.format(key):  # ------------------- require attention here -------------------
            if self.do_dungeon:
                print('turning off dungeon')
                self.do_dungeon = False
            else:
                print('turning on dungeon')
                self.do_dungeon = True

    # field auto
    def count_bw(self,bw_list):
        bw_count = 0
        for x in bw_list:
            if x == 255:
                bw_count +=1
        return bw_count

    # field auto
    def check_distance(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
# ---------------------------------------------------------------- need attention
        party_box_x1 = 1039 # ------------------- require attention here -------------------
        party_box_y1 = 827 # ------------------- require attention here -------------------
        party_box_x2 = party_box_x1 + 7
        party_box_y2 = party_box_y1 + 1
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # print(f'{im_bw[0]} lows: {self.count_bw(im_bw[0])}')
        return self.count_bw(im_bw[0])

    # def check_target(self, ss):
    #     temp_time = time.time()
    #     img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
    #     party_box_x1 = 1033
    #     party_box_y1 = 792
    #     party_box_x2 = 1035
    #     party_box_y2 = 793
    #     img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     # print(f'target time check {time.time()-temp_time}')
    #     return gray[0]

    # field auto / dungeon
    def check_target(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        # ---------------------------------------------------------------- need attention
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

    # dungeon
    def initialize_skill_list_check_list(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        party_box_x1 = 605  # ------------------- require attention here -------------------
        party_box_y1 = 1045  # ------------------- require attention here -------------------

        party_box_x2 = party_box_x1 + 1
        party_box_y2 = party_box_y1 + 1
        first_inc = [0, 58, 57, 58, 58, 59, 0, 58, 58, 58, 58, 57]

        skip_skill_slot = []

        attacks_p1 = [1,2,3,4, 5, 6, 7, 8, 9,10,11,12]
        attacks_p2 = []
        distances = []
        buffs = []

        available_attacks_p1 = []
        available_attacks_p2 = []
        available_distances = []
        available_buffs = []

        temp_all = []
        slot_count = 1
        accum = 0

        inc_counter = 0
        for inc in first_inc:
            if slot_count == 7:
                party_box_x1 = 1009 # ------------------- require attention here -------------------
                party_box_x2 = party_box_x1 + 1
                accum = 0
            if slot_count not in skip_skill_slot:
                accum += inc
                img_cropped = gray[party_box_y1:party_box_y2, party_box_x1 + accum:party_box_x2 + accum]
                skill_value = int(img_cropped[0][0])
                temp_all.append((slot_count, skill_value))
                if self.initial_skill_list_scan:
                    self.skill_list_available[inc_counter] = skill_value
                else:
                    if skill_value == self.skill_list_available[inc_counter]:
                        if slot_count in attacks_p1:
                            available_attacks_p1.append((slot_count, skill_value))
                        if slot_count in attacks_p2:
                            available_attacks_p2.append((slot_count, skill_value))
                        if slot_count in distances:
                            available_distances.append((slot_count, skill_value))
                        if slot_count in buffs:
                            available_buffs.append((slot_count, skill_value))
            slot_count += 1
            inc_counter += 1

        return_command = [available_attacks_p1,available_attacks_p2, available_distances, available_buffs]
        self.initial_skill_list_scan = False
        return return_command

    # field auto
    def initialize_skill_list_check(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        party_box_x1 = 605 # ------------------- require attention here -------------------
        party_box_y1 = 1045 # ------------------- require attention here -------------------

        party_box_x2 = party_box_x1 + 1
        party_box_y2 = party_box_y1 + 1
        first_inc = [0,58,57,58,58,59,0,58,58,58,58,57]

        skip_skill_slot = []


        attacks_p1 = [4,5,6,7,8,9]
        attacks_p2 = [8,9]
        distances = [10,11,12]
        buffs = [1,2,3]


        available_attacks_p1 = []
        available_attacks_p2 = []
        available_distances = []
        available_buffs = []

        temp_all = []
        slot_count = 1
        accum = 0

        inc_counter = 0
        for inc in first_inc:

            if slot_count == 7:
                party_box_x1 = 1009 # ------------------- require attention here -------------------
                party_box_x2 = party_box_x1 + 1
                accum = 0
            if slot_count not in skip_skill_slot:
                accum += inc
                img_cropped = gray[party_box_y1:party_box_y2, party_box_x1 + accum:party_box_x2 + accum]
                skill_value = int(img_cropped[0][0])
                temp_all.append((slot_count,skill_value))
                if self.initial_skill_list_scan:
                    self.skill_list_available[inc_counter] = skill_value
                else:
                    if skill_value == self.skill_list_available[inc_counter]:
                        if slot_count in attacks_p1:
                            available_attacks_p1.append((slot_count,skill_value))
                        if slot_count in attacks_p2:
                            available_attacks_p2.append((slot_count,skill_value))
                        if slot_count in distances:
                            available_distances.append((slot_count,skill_value))
                        if slot_count in buffs:
                            available_buffs.append((slot_count,skill_value))

            slot_count +=1
            inc_counter+=1
        self.initial_skill_list_scan = False
        return_command = []
        if len(available_attacks_p1) != 0:
            return_command.append(available_attacks_p1[0][0])
        else:
            return_command.append(0)
        if len(available_attacks_p2) != 0:
            return_command.append(available_attacks_p2[0][0])
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

    # field auto
    def check_target_health(self,ss):
        temp_time = time.time()

        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 1216 # ------------------- require attention here -------------------
        party_box_y1 = 802 # ------------------- require attention here -------------------
        party_box_x2 = party_box_x1 + 1
        party_box_y2 = party_box_y1 + 1
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        return gray[0]

    # field auto
    def check_target_out_sight(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 820 # ------------------- require attention here -------------------
        party_box_y1 = 250 # ------------------- require attention here -------------------
        party_box_x2 = party_box_x1 + 280
        party_box_y2 = party_box_y1 + 20
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)

    # dungeon
    def check_loading_screen(self,ss):
        temp_time = time.time()

        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 729 # ------------------- require attention here -------------------
        party_box_y1 = 781 # ------------------- require attention here -------------------
        party_box_x2 = party_box_x1 + 1
        party_box_y2 = party_box_y1 + 1
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        print(gray[0])
        return gray[0]


    # dungeon
    def read_chat(self):
        ss = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 30 # ------------------- require attention here -------------------
        party_box_y1 = 942 # ------------------- require attention here -------------------
        party_box_x2 = 195 # ------------------- require attention here -------------------
        party_box_y2 = 983 # ------------------- require attention here -------------------
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)

    def start_assist(self):
        print("started throne script")
        t1 = threading.Thread(target=self.while_loop)
        listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()



if __name__ =="__main__":

    melee_assist = throne_script()
    melee_assist.start_assist()

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

# combo_sequence_three_str = [
#     12,
#     9,
#     4,
#     6,
#     1,
#     2,
#     4,
#     1,
#     12,
#     11,
#     7,
#     8,
#     6,
#     5,
#     3,
#     10,
#     1,
#     4,
#     4,
#     6,
#     2,
#     1,
# ]