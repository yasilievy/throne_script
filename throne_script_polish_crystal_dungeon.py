import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key,Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'

class throne_script:
    def __init__(self):
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.static_bool = True
        self.do_combo = False
        self.do_dungeon = False

        self.start_bool = False
        self.quick_scan = False
        self.button_open = True
        self.button_open_two = True
        self.timer = None
        self.timer_boolean = False
        self.initialize_config = False

        # skill keybinding dictionary
        self.skill_dict = {
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: Key.f7,
            7: Key.f1,
            8: Key.f2,
            9: Key.f4,
            10: 'e',
            11: 'r',
            12: 't',
            13: 'x',
            14: 'c'
        }

        self.combo_sequence = []
        self.phase_counter = 0



        self.yes_button = 'y'
        self.stealth_button = '5'
        self.dodge_button = 'q'
        self.morph_button = Key.shift
        self.open_co_op_menu_button = Key.f11

        # self.manage_party_button = None
        self.manage_party_coord = (19, 12)
        self.manage_party_leave_coord = (445, 330)
        self.exit_dungeon = (1870, 280)
        self.read_chat_coord = (30, 942, 165, 41)
        self.check_loading_screen_coord = (729, 781, 1, 1)
        self.check_loading_screen_value = 255 # need to scan a screenshot
        self.check_target_coord = (1064, 810, 9, 1)
        self.target_check_values = 115 # need to scan a screenshot
        self.enter_dungeon_coord = (960, 1000)

        self.skill_set_one_x1 = 605
        self.skill_set_two_x1 = 1009

        self.skill_pixel_edge = [605,663,720,778,836,894,1009,1067,1125,1183,1241,1298]
        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.check_skill_coord = (0, 1045, 1920, 1)
        self.initialize_config_recalibrate()

    def initialize_config_recalibrate(self):
        time.sleep(0.2)
        pyautogui.hotkey('alt','tab')
        self.config_file = open('throne_script_config.txt','r+')
        config_file_read = self.config_file.read()
        if len(config_file_read) == 0:
            self.initialize_config = True
            write_to = ''
            print('config file is empty\nstarting initialization')
            print('setting target values')
            print('please target something')
            # initial_screenshot = None
            while True:
                time.sleep(0.5)
                initial_target_screenshot = pyautogui.screenshot(region=self.check_target_coord)
                if self.check_target(initial_target_screenshot):
                    print('setting target values completed')
                    write_to += f'target_value={self.target_check_values}\n' # value is set in self.check_target()
                    break
            print('setting skill list values')
            initial_skill_screenshot = pyautogui.screenshot(region=self.check_skill_coord)
            self.initialize_skill_list(initial_skill_screenshot)
            write_to += f'skill_values={','.join(str(v) for v in self.skill_list_available)}\n'  # value is set in self.initialize_skill_list_check()
            print('setting skill list values completed')

            initial_loading_screenshot = pyautogui.screenshot(region=self.check_loading_screen_coord)
            self.check_loading_screen_value = self.check_loading_screen(initial_loading_screenshot)[0]
            write_to += f'loading_screen_value={self.check_loading_screen_value}'
            self.config_file.write(write_to)
            self.config_file.close()
            self.initialize_config = False
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
                if 'loading' in setting:
                    self.check_loading_screen_value = int(value)

            # print('testt4')
            # image_test = Image.open('clients/testt4.jpg')
            # check_target_coord = (1064, 810, 1073, 811)
            # image_test_crop = image_test.crop(check_target_coord)
            # print(self.check_target(image_test_crop))
            #
            # check_skill_coord = (0, 1045, 1920, 1046)
            # image_test_crop = image_test.crop(check_skill_coord)
            # print(self.check_available_skill_list(image_test_crop))



    def enter_dungeon(self):
        self.mouse.position = self.manage_party_coord
        self.mouse.click(Button.left)
        time.sleep(0.7)
        self.mouse.position = self.manage_party_leave_coord
        self.mouse.click(Button.left)
        time.sleep(0.7)
        self.keyboard.press(self.open_co_op_menu_button)
        self.keyboard.release(self.open_co_op_menu_button)
        time.sleep(0.7)
        self.mouse.position = self.enter_dungeon_coord
        self.mouse.click(Button.left)
        time.sleep(6)
        while True:
            screen_shot_check_loading_screen = pyautogui.screenshot(region=self.check_loading_screen_coord)
            if self.check_loading_screen(screen_shot_check_loading_screen)[0] == self.check_loading_screen_value:
                break
            time.sleep(0.5)

    def move_to_boss(self):
        movement_speed = 630
        time_helper = 1 - ((movement_speed - 600) / 600)
        time_helper_two = 1 - ((movement_speed - 600) / 600 /2 )

        self.keyboard.press('a')
        self.keyboard.press(self.dodge_button)
        self.keyboard.release(self.dodge_button)
        self.keyboard.release('a')

        # self.timer_boolean = True
        # self.timer = time.time()
        # self.do_dungeon = False

        time.sleep(0.2)
        print('moving')
        self.keyboard.press('w')
        self.keyboard.press(Key.shift)
        self.keyboard.release(Key.shift)
        time.sleep(5 * time_helper)
        self.keyboard.press('5')
        self.keyboard.release('5')
        time.sleep(15 * time_helper_two)
        self.keyboard.press('d')
        self.keyboard.press(Key.shift)
        self.keyboard.release(Key.shift)
        time.sleep(4.5 * time_helper)
        self.keyboard.release('d')
        time.sleep(8.5 * time_helper)
        self.keyboard.release('w')


    def check_combo_sequence(self):
        combo_sequence_open = open('combo_sequence\\ravager_combo_sequence.txt','r')
        combo_sequence_read_split = combo_sequence_open.read().split('\n')
        rendered_combo_sequence = []
        try:
            rendered_combo_sequence = [int(line.split(',')[0]) for line in combo_sequence_read_split]
        except:
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
                    screen_shot_check_target = pyautogui.screenshot(region=self.check_target_coord)
                    if self.check_target(screen_shot_check_target):
                        current_combo = self.combo_sequence[skill_counter]
                        screen_shot = pyautogui.screenshot(region=self.check_skill_coord)
                        skill_status_p1 = self.check_available_skill_list(screen_shot)
                        if len(skill_status_p1) != 0:
                            current_button_to_press = self.skill_dict[current_combo]
                            rendered_skill_status_p1 = [s_s_p1[0] for s_s_p1 in skill_status_p1]
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

                            # staff combo
                            # elif current_combo == 1:
                            #     self.keyboard.press(Key.shift)
                            #     self.keyboard.press(self.skill_dict[current_combo])
                            #     time.sleep(0.1)
                            #     self.keyboard.release(Key.shift)
                            #     self.keyboard.release(self.skill_dict[current_combo])
                            # elif current_combo == 10:
                            #     self.keyboard.press(self.skill_dict[current_combo])
                            #     time.sleep(1.2)
                            #     self.keyboard.release(self.skill_dict[current_combo])
                            # # elif current_combo == 8:
                            # #     self.keyboard.press(self.skill_dict[current_combo])
                            # #     self.keyboard.release(self.skill_dict[current_combo])
                            # #     # time.sleep(1)
                            #     # self.keyboard.press(self.skill_dict[current_combo])
                            #     # self.keyboard.release(self.skill_dict[current_combo])

                            # else:
                            #     self.keyboard.press(self.skill_dict[current_combo])
                            #     self.keyboard.release(self.skill_dict[current_combo])
                            time.sleep(0.1)
                    else:
                        break
            skill_counter += 1
    def do_kill_confirm(self):
        while self.do_dungeon:
            while self.check_target(pyautogui.screenshot(region=self.check_target_coord))
            # screen_shot_check_target = pyautogui.screenshot(region=self.check_target_coord)
            if self.check_target(screen_shot_check_target):
                self.keyboard.press(self.skill_dict[2])
                self.keyboard.release(self.skill_dict[2])
                self.keyboard.press(self.skill_dict[1])
                self.keyboard.release(self.skill_dict[1])
                self.keyboard.press(self.skill_dict[11])
                self.keyboard.release(self.skill_dict[11])
                self.keyboard.press(self.skill_dict[6])
                self.keyboard.release(self.skill_dict[6])
                time.sleep(0.3)
            else:
                print('boss is dead')
                break
    def do_exit_sequence(self, end_timer):
        # self.keyboard.press(Key.enter)
        # self.keyboard.release(Key.enter)
        have_not_exited = True
        while self.do_dungeon:
            time.sleep(0.1)
            # screen_shot_read_chat = pyautogui.screenshot(region=self.read_chat_coord)
            # chat_read = self.read_chat(screen_shot_read_chat)
            # if 'safe' in chat_read or 'left' in chat_read or 'expire' in chat_read:
            #     print('successfully exited dungeon')
            #     self.start_bool = True
            #     break
            screen_shot_check_loading_screen = pyautogui.screenshot(region=self.check_loading_screen_coord)
            if have_not_exited and self.check_loading_screen(screen_shot_check_loading_screen)[0] == self.check_loading_screen_value:
                if end_timer == 10:
                    time.sleep(0.2)
                    self.keyboard.press(Key.alt)
                    self.keyboard.release(Key.alt)
                    time.sleep(0.2)
                    self.mouse.position = self.exit_dungeon
                    self.mouse.click(Button.left)
                    time.sleep(0.2)
                    self.keyboard.press('y')
                    self.keyboard.release('y')
                    time.sleep(0.2)
                else:
                    time.sleep(0.2)
                    self.keyboard.press('b')
                    self.keyboard.release('b')
                    time.sleep(0.5)
                    self.keyboard.press('y')
                    self.keyboard.release('y')
                    time.sleep(5.1)
            else:
                have_not_exited = False
                if self.check_loading_screen(screen_shot_check_loading_screen)[0] != self.check_loading_screen_value:
                    pass
                else:
                    break
        if end_timer == 10:
            time.sleep(end_timer)
        self.phase_counter = -1

    def while_loop(self):
        pyautogui.hotkey('alt', 'tab')
        while self.static_bool:
            while self.do_combo:
                self.do_combo_sequence()
                self.do_combo = False
                print('combo completed')

            time.sleep(0.1)
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
                    self.enter_dungeon()

                if self.phase_counter == 1: # ------------------------ enter dungeon
                    print('moving to boss')
                    self.move_to_boss()
                    # self.move_to_boss_non_gs()

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
                    # time.sleep(9)

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
            # print(new_time - self.timer)

    def on_release(self,key):
        # print('{0}'.format(key))
        if self.timer_boolean and '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift',"'q'"]:
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
                print('turning off polish crystal dungeon script')
                self.do_dungeon = False
            else:
                print('turning on polish crystal dungeon script')
                self.do_dungeon = True
        if '+' in '{0}'.format(key):
            if self.do_combo:
                print('turning off combo sequence')
                self.do_combo = False
            else:
                print('turning on combo sequence')
                self.do_combo = True
        if '-' in '{0}'.format(key):
            if self.quick_scan:
                print('turning off quick scan')
                self.quick_scan = False
            else:
                print('turning on quick scan and perform one quick scan below:')
                self.quick_scan = True
                screen_shot_check_target = pyautogui.screenshot(region=self.check_target_coord)
                self.check_target(screen_shot_check_target)
                screen_shot = pyautogui.screenshot(region=self.check_skill_coord)
                self.check_available_skill_list(screen_shot)

    def check_available_skill_list(self, ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        skip_skill_slot = []
        attacks_p1 = [1,2,3,4,5,6,7,8,9,10,11,12]
        available_attacks = []
        temp_all = []
        slot_count = 1
        inc_counter = 0
        for x_coord in self.skill_pixel_edge:
            if slot_count not in skip_skill_slot:
                skill_value = gray[0][x_coord]
                temp_all.append((slot_count, int(skill_value)))
                if skill_value == self.skill_list_available[inc_counter]:
                    if slot_count in attacks_p1:
                        available_attacks.append((slot_count, int(skill_value)))
            slot_count += 1
            inc_counter += 1
        if self.quick_scan:
            print(f'check all available skill list: {temp_all}')
            print(f'check available skill list: {available_attacks}')
        return available_attacks

    def initialize_skill_list(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        skip_skill_slot = []
        slot_count = 1
        inc_counter = 0
        for x_coord in self.skill_pixel_edge:
            if slot_count not in skip_skill_slot:
                skill_pixel_value = gray[0][x_coord]
                self.skill_list_available[inc_counter] = skill_pixel_value
            slot_count += 1
            inc_counter += 1

    def check_target(self, ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.quick_scan:
            print(gray[0])
        # print(f'check target {gray[0]}')
        if self.initialize_config:
            constant_value = gray[0][0]
            for value in gray[0]:
                if constant_value != value:
                    return False
            self.target_check_values = constant_value
            return True
        else:
            for value in gray[0]:
                if self.target_check_values != value and value != 116:
                    return False
            return True

    def check_loading_screen(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.quick_scan:
            print(f'check loading screen: {gray[0]}')
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