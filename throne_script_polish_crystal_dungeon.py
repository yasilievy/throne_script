import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key,Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Tesseract-OCR\\tesseract.exe'

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
        self.do_contracts = False
        self.button_open = True
        self.button_open_two = True
        self.timer = None
        self.timer_boolean = False
        self.counter = -1
        self.current_key = None
        self.do_bot = False
        self.do_dungeon = False
        self.initial_skill_list_scan = True
        # self.initialize_config()

        self.skill_dict = {
            1: [Key.shift,'1'],
            2: 'f',
            3: '3',
            4: '4',
            5: 'r',
            6: 'e',
            7: [Key.shift,'4'],
            8: [Key.shift,'v'],
            9: 'v',
            10: [Key.shift,'r'],
            11: [Key.shift,'q'],
            12: [Key.shift,'e'],
            13: 'x',
            14: 'c'
        }

        self.combo_sequence = []

        self.phase_counter = 0

        self.stealth_button = 'r'
        self.dodge_button = 'q'
        self.morph_button = Key.shift

        self.cursor_button = [Key.shift,'g']

        self.start_bool = False

        # self.manage_party_button = None
        self.manage_party_coord = (879, 998)
        self.manage_party_leave_coord = (536, 470)

        self.open_co_op_menu_button = Key.f11
        self.enter_dungeon = (1716, 1352)

        self.check_loading_screen_coord = (1318, 1008, 1, 1)
        self.check_loading_screen_value = 255 # need to scan a screenshot

        self.check_target_coord = (1503, 791, 9, 1)
        self.target_check_values = 115 # need to scan a screenshot
        self.target_check_values_list = [0,0,0,0,0,0,0,0,0]

        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.check_skill_coord = (0, 1045, 1920, 1)

        self.read_chat_coord = (30, 942, 165, 41)

        self.exit_dungeon = (3378, 328)
        self.yes_button = 'y'
        self.initialize_config()

    def initialize_config(self):
        time.sleep(0.2)
        pyautogui.hotkey('alt','tab')
        self.config_file = open('throne_script_config.txt','r+')
        config_file_read = self.config_file.read()
        if len(config_file_read) == 0:
            self.initial_skill_list_scan = True

            image_test = Image.open('clients\\test.JPG')
            # print(self.check_available_skill_list(image_test))
            cvt_img = cv2.cvtColor(np.array(image_test), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
            thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)  # | cv2.THRESH_OTSU)

            y1 = 1268
            x1 = 1279
            x2 = 1367
            x3 = 1436
            x4 = 1505
            x5 = 1574
            x6 = 1642
            x7 = 1758
            x8 = 1827
            x9 = 1915
            x10 = 1964
            x11 = 2033
            x12 = 2102
            pixel_list = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12]
            skill_pixel_value = []
            counter = 1
            gray_cropped = gray[y1:y1 + 1, 0:3440]
            for x_p in pixel_list:
                # gray_cropped = gray[y1:y1 + 1, x_p:x_p + 1]
                skill_pixel_value.append(gray_cropped[0][x_p])
                self.skill_list_available[counter] = gray_cropped[0][x_p]
                print(f'{counter}: {gray_cropped[0][x_p]}')
                counter += 1

            write_to = ''
            print('config file is empty\nstarting initialization')
            print('setting target values and available skill pixel values')
            target_value_screenshot = pyautogui.screenshot(region=self.check_target_coord)
            cvt_img = cv2.cvtColor(np.array(target_value_screenshot), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cvt_img, cv2.COLOR_BGR2GRAY)
            self.target_check_values_list = gray[0]
            print('setting target values completed')
            write_to += f'target_value={','.join(str(v) for v in self.target_check_values_list)}\n' # value is set in self.check_target()

            print('setting skill list values')
            write_to += f'skill_values={','.join(str(v) for v in skill_pixel_value)}'  # value is set in self.initialize_skill_list_check()
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
                    config_skill_counter = 0
                    for target_value in value.split(','):
                        self.target_check_values_list[config_skill_counter] = int(target_value)
                        config_skill_counter += 1
                if 'skill' in setting:
                    config_skill_counter = 0
                    for skill_value in value.split(','):
                        self.skill_list_available[config_skill_counter] = int(skill_value)
                        config_skill_counter+=1



    def move_to_boss_one(self):
        self.mouse.position = self.manage_party_coord
        self.mouse.click(Button.left)
        time.sleep(0.7)
        self.mouse.position = self.manage_party_leave_coord
        self.mouse.click(Button.left)
        time.sleep(0.7)
        self.keyboard.press(self.open_co_op_menu_button)
        self.keyboard.release(self.open_co_op_menu_button)
        time.sleep(0.7)
        self.mouse.position = self.enter_dungeon
        self.mouse.click(Button.left)
        time.sleep(6)
        while True:
            screen_shot_check_loading_screen = pyautogui.screenshot(region=self.check_loading_screen_coord)
            if self.check_loading_screen(screen_shot_check_loading_screen)[0] == self.check_loading_screen_value:
                break
            time.sleep(0.5)

    def move_to_boss_two(self):
        time_helper = 1.07
        self.keyboard.press('a')
        self.keyboard.press(self.dodge_button)
        self.keyboard.release(self.dodge_button)
        self.keyboard.release('a')
        # self.timer_boolean = True
        # self.timer = time.time()`

        # self.do_dungeon = False
        time.sleep(0.5)

        self.keyboard.press('w')
        self.keyboard.press(self.morph_button)
        self.keyboard.release(self.morph_button)
        time.sleep(3.24 * time_helper)
        self.keyboard.press(self.stealth_button ) # need configuration
        self.keyboard.release(self.stealth_button ) # need configuration
        time.sleep(5.61 * time_helper)
        self.keyboard.press('d')
        time.sleep(5.0 * time_helper)
        self.keyboard.release('d')
        time.sleep(4 * time_helper)
        self.keyboard.press(self.dodge_button)
        self.keyboard.release(self.dodge_button)
        # time.sleep(0.57 * time_helper)`5
        self.keyboard.press(self.morph_button)
        self.keyboard.release(self.morph_button)
        time.sleep(8.5 * time_helper)
        self.keyboard.release('w')

    def move_to_boss_two_non_gs(self):
        movement_speed = 630
        # movement_speed = 797
        time_helper = 1 - ((movement_speed - 600) / 600)
        time_helper_two = 1 - ((movement_speed - 600) / 600 /2 )

        self.keyboard.press('a')
        self.keyboard.press(self.dodge_button)
        self.keyboard.release(self.dodge_button)
        self.keyboard.release('a')

        # self.timer_boolean = True`

        # self.timer = time.time()
        # self.do_dungeon = False

        time.sleep(0.2)
        print('moving')

        self.keyboard.press('w')
        self.keyboard.press(self.morph_button)
        self.keyboard.release(self.morph_button)
        time.sleep(5 * time_helper_two)
        self.keyboard.press(self.stealth_button ) # need configuration
        self.keyboard.release(self.stealth_button ) # need configuration
        time.sleep(8 * time_helper)
        self.keyboard.press('d')
        time.sleep(5.7 * time_helper)
        self.keyboard.release('d')
        time.sleep(3)
        self.keyboard.press(self.morph_button)
        self.keyboard.release(self.morph_button)
        time.sleep(9.8 * time_helper_two)
        self.keyboard.release('w')

    def check_combo_sequence(self):
        combo_sequence_open = open('combo_sequence\\ravager_combo_sequence.txt','r')
        combo_sequence_read_split = combo_sequence_open.read().split('\n')
        rendered_combo_sequence = []
        try:
            rendered_combo_sequence = [int(line.split(',')[0]) for line in combo_sequence_read_split]
        except Exception as e:
            print('an issue occured - review the combo_sequence.txt')
            self.keyboard.press(Key.esc)
        return rendered_combo_sequence
    def do_combo_sequence(self):
        skill_counter = 0
        self.combo_sequence = self.check_combo_sequence()

        while self.do_dungeon or self.do_combo:
            # print(skill_counter)
            if skill_counter == len(self.combo_sequence):
                break
            else:
                while self.do_dungeon or self.do_combo:
                    current_combo = self.combo_sequence[skill_counter]
                    screen_shot = pyautogui.screenshot(region=self.check_skill_coord)
                    skill_status_p1 = self.check_available_skill_list(screen_shot)[0]
                    if len(skill_status_p1) != 0:
                        rendered_skill_status_p1 = [s_s_p1[0] for s_s_p1 in skill_status_p1]
                        # if current_combo == 12:
                        #     self.skill_pause_counter = True
                        current_button_to_press = self.skill_dict[current_combo]
                        if current_combo not in rendered_skill_status_p1:
                            break
                        elif current_combo == 2 or current_combo == 3:
                            if isinstance(current_button_to_press, list):
                                self.keyboard.press(self.skill_dict[current_combo][0])
                                self.keyboard.press(self.skill_dict[current_combo][1])
                                time.sleep(1)
                                self.keyboard.release(self.skill_dict[current_combo][0])
                                self.keyboard.release(self.skill_dict[current_combo][1])
                            else:
                                self.keyboard.press(self.skill_dict[current_combo])
                                time.sleep(1)
                                self.keyboard.release(self.skill_dict[current_combo])
                        else:
                            if isinstance(current_button_to_press, list):
                                self.keyboard.press(self.skill_dict[current_combo][0])
                                self.keyboard.press(self.skill_dict[current_combo][1])
                                time.sleep(1)
                                self.keyboard.release(self.skill_dict[current_combo][0])
                                self.keyboard.release(self.skill_dict[current_combo][1])
                            else:
                                self.keyboard.press(self.skill_dict[current_combo])
                                self.keyboard.release(self.skill_dict[current_combo])
                        time.sleep(0.1)
            skill_counter += 1
    def do_kill_confirm(self):
        while self.do_dungeon:
            screen_shot_check_target = pyautogui.screenshot(region=self.check_target_coord)
            if self.check_target(screen_shot_check_target):
                skill_to_use = self.skill_dict[2]
                if isinstance(skill_to_use, list):
                    self.keyboard.press(skill_to_use[0])
                    self.keyboard.press(skill_to_use[1])
                    self.keyboard.release(skill_to_use[0])
                    self.keyboard.release(skill_to_use[1])
                else:
                    self.keyboard.press(skill_to_use)
                    self.keyboard.release(skill_to_use)

                skill_to_use = self.skill_dict[1]
                if isinstance(skill_to_use, list):
                    self.keyboard.press(skill_to_use[0])
                    self.keyboard.press(skill_to_use[1])
                    self.keyboard.release(skill_to_use[0])
                    self.keyboard.release(skill_to_use[1])
                else:
                    self.keyboard.press(skill_to_use)
                    self.keyboard.release(skill_to_use)

                skill_to_use = self.skill_dict[6]
                if isinstance(skill_to_use, list):
                    self.keyboard.press(skill_to_use[0])
                    self.keyboard.press(skill_to_use[1])
                    self.keyboard.release(skill_to_use[0])
                    self.keyboard.release(skill_to_use[1])
                else:
                    self.keyboard.press(skill_to_use)
                    self.keyboard.release(skill_to_use)

                skill_to_use = self.skill_dict[12]
                if isinstance(skill_to_use, list):
                    self.keyboard.press(skill_to_use[0])
                    self.keyboard.press(skill_to_use[1])
                    self.keyboard.release(skill_to_use[0])
                    self.keyboard.release(skill_to_use[1])
                else:
                    self.keyboard.press(skill_to_use)
                    self.keyboard.release(skill_to_use)

                time.sleep(0.3)
            else:
                print('boss is dead')
                break

    def do_exit_sequence(self, end_timer):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        while True:
            time.sleep(0.1)
            screen_shot_read_chat = pyautogui.screenshot(region=self.read_chat_coord)
            chat_read = self.read_chat(screen_shot_read_chat)
            if 'safe' in chat_read or 'left' in chat_read or 'expire' in chat_read:
                print('successfully exited dungeon')
                self.start_bool = True
                break
            else:
                time.sleep(0.3)
                self.mouse.position = self.exit_dungeon
                self.mouse.click(Button.left)
                time.sleep(0.3)
                self.keyboard.press('y')
                self.keyboard.release('y')
                time.sleep(end_timer)
        self.phase_counter = -1


    def while_loop(self):
        pyautogui.hotkey('alt', 'tab')
        while self.static_bool:
            time.sleep(0.1)
            while self.do_combo:
                self.do_combo_sequence()
                self.do_combo = False
                print('combo completed')

            while self.do_dungeon:
                if self.phase_counter == 0:
                    timer = time.time()
                    print('entering dungeon')
                    if self.start_bool:
                        pass
                    else:
                        self.keyboard.press(Key.enter)
                        self.keyboard.release(Key.enter)
                        time.sleep(0.7)
                    self.move_to_boss_one()
                if self.phase_counter == 1: # ------------------------ enter dungeon
                    print('moving to boss')
                    self.move_to_boss_two()
                    # self.move_to_boss_two_non_gs()
                if self.phase_counter == 2: # ------------------------ move to boss
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)
                    time.sleep(0.5)
                    screen_shot_check_target = pyautogui.screenshot(region=self.check_target_coord)
                    if self.check_target(screen_shot_check_target):
                        print('found target, starting combo sequence')
                        self.do_combo_sequence()
                    else:
                        print('did not find boss successfully, attempting to exit')
                        self.do_exit_sequence(10)
                        print(f'raid time attempt: {time.time() - timer}')
                        self.phase_counter = -1

                if self.phase_counter == 3: # ------------------------ kill the boss
                    screen_shot_check_target = pyautogui.screenshot(region=self.check_target_coord)
                    if self.check_target(screen_shot_check_target):
                        print('boss is not dead yet, double tapping')
                        self.do_kill_confirm()
                    else:
                        print('boss is dead')
                    time.sleep(2)

                if self.phase_counter == 4: # ------------------------ exit the dungeon
                    self.do_exit_sequence(3)
                    print(f'raid time complete: {time.time() - timer}')
                self.phase_counter += 1



    def on_press(self,key):
        # print('{0}'.format(key))
        if self.timer_boolean:
            if self.button_open:
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift', "'q'"]:
                    self.button_open = False
                    new_time = time.time()
                    print(f'time.sleep({round(new_time - self.timer,2)} * time_helper)')
                    print(f'self.keyboard.press({'{0}'.format(key)})')
                    self.timer = new_time
            elif self.button_open_two:
                if '{0}'.format(key) in ["'w'", "'a'", "'s'", "'d'", "'5'", 'Key.shift', "'q'"]:
                    self.button_open_two = False
                    new_time = time.time()
                    print(f'time.sleep({round(new_time - self.timer,2)} * time_helper)')
                    print(f'self.keyboard.press({'{0}'.format(key)})')
                    self.timer = new_time
            # self.timer_boolean = True
            # print(new_time - self.timer)
        pass

    def on_release(self,key):
        # print('{0}'.format(key))
        if self.timer_boolean and '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift',"'q'"]:
        # if "'5'" == '{0}'.format(key) or "'a'" == '{0}'.format(key) or "'s'" == '{0}'.format(key) or "'d'" == '{0}'.format(key):
        # if self.timer_boolean:
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
        if '`' in '{0}'.format(key):
            self.phase_counter = 0
            if self.do_dungeon:
                print('turning off dungeon')
                self.do_dungeon = False
            else:
                print('turning on dungeon')
                self.do_dungeon = True
        if '+' in '{0}'.format(key): # keypad 2
            if self.do_combo:
                print('turning off combo two')
                self.do_combo = False
            else:
                print('turning on combo two')
                self.do_combo = True
        # if '-' in '{0}'.format(key): # keypad 2
        #     if self.do_nav:
        #         print('turning off combo two')
        #         self.do_nav = False
        #     else:
        #         print('turning on combo two')
        #         self.do_nav = True
        # if '/' in '{0}'.format(key): # keypad 2
        #     if self.do_exit:
        #         print('turning off combo two')
        #         self.do_exit = False
        #     else:
        #         print('turning on combo two')
        #         self.do_exit = True

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
            # for value in gray[0]:
            #     if self.target_check_values_list != value and value != 116:
            #         return False
            return self.target_check_values_list == gray[0]

    # polish crystal farm
    def check_available_skill_list(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        x1 = 1279
        x2 = 1367
        x3 = 1436
        x4 = 1505
        x5 = 1574
        x6 = 1642
        x7 = 1758
        x8 = 1827
        x9 = 1915
        x10 = 1964
        x11 = 2033
        x12 = 2102
        pixel_list = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12]

        skip_skill_slot = []
        attacks_p1 = [1,2,3,4, 5, 6, 7, 8, 9,10,11,12]
        available_attacks_p1 = []
        available_attacks_p2 = []
        available_distances = []
        available_buffs = []
        temp_all = []
        slot_count = 1
        inc_counter = 0
        for inc in pixel_list:
            if slot_count not in skip_skill_slot:
                skill_value = gray[0][inc]
                temp_all.append((slot_count, skill_value))
                # print(f'{slot_count} : {skill_value}')
                if skill_value >= self.skill_list_available[inc_counter] - 10 and skill_value <= self.skill_list_available[inc_counter] + 10:
                    if slot_count in attacks_p1:
                        available_attacks_p1.append((slot_count, skill_value))
            slot_count += 1
            inc_counter += 1
        return_command = [available_attacks_p1,available_attacks_p2, available_distances, available_buffs]
        return return_command

    def check_loading_screen(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(gray[0])
        return gray[0]

    def read_chat(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
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