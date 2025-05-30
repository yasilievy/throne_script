import pytesseract, pyautogui, time, numpy as np, threading,cv2, random, datetime
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
        self.button_open_three = True
        self.movement_record_timer = None
        self.movement_record_bool = False
        self.initialize_config = False
        self.diagnostic_write_to = ''
        self.active_duration = time.time()



        self.combo_sequence = []
        self.phase_counter = 0

        # start ------- Configure variables
        self.skill_dict = {
            1: [Key.shift,'f'],
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

        self.yes_button = 'y'
        self.stealth_button = 'r'
        self.dodge_button = 'q'
        self.morph_button = 'y'
        self.open_co_op_menu_button = Key.f11

        self.manage_party_coord = (879, 998)
        self.manage_party_leave_coord = (536, 470)
        self.exit_dungeon = (3378, 328)
        self.read_chat_coord = (30, 942, 165, 41)
        self.check_loading_screen_coord = (1318, 1008, 1, 1)
        self.check_loading_screen_value = 255 # need to scan a screenshot
        self.check_target_coord = (1503, 791, 9, 1)
        self.target_check_values = 115 # need to scan a screenshot
        self.enter_dungeon_coord = (1716, 1352)

        self.skill_pixel_edge = [1279,1367,1436,1505,1574,1642,1758,1827,1915,1964,2033,2102]
        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.check_skill_coord = (0, 1268, 3440, 1)

        self.movement_speed = 687

        # end --------- Configure variables

        self.initialize_config_recalibrate()


    def initialize_config_recalibrate(self):
        time.sleep(0.2)
        pyautogui.hotkey('alt','tab')
        self.config_file = open('throne_script_config.txt','r+')
        config_file_read = self.config_file.read()
        if len(config_file_read) == 0:
            self.initialize_config = True
            write_to = ''
            print('config file is empty, starting configuration calibration')
            print('setting {target values}')
            print('please target something')
            while True:
                time.sleep(0.5)
                initial_target_screenshot = pyautogui.screenshot(region=self.check_target_coord)
                if self.check_target(initial_target_screenshot):
                    print('setting {target values} completed')
                    write_to += f'target_value={self.target_check_values}\n' # value is set in self.check_target()
                    break
            print('setting {skill list values}')
            initial_skill_screenshot = pyautogui.screenshot(region=self.check_skill_coord)
            self.initialize_skill_list(initial_skill_screenshot)
            write_to += f'skill_values={','.join(str(v) for v in self.skill_list_available)}\n'  # value is set in self.initialize_skill_list_check()
            print('setting {skill list values} completed')
            print('setting {loading screen value}')
            initial_loading_screenshot = pyautogui.screenshot(region=self.check_loading_screen_coord)
            self.check_loading_screen_value = self.check_loading_screen(initial_loading_screenshot)[0]
            write_to += f'loading_screen_value={self.check_loading_screen_value}'
            self.config_file.write(write_to)
            print('setting {loading screen value} completed ')
            self.config_file.close()

            self.initialize_config = False
        else:
            print('config file exists, configuration calibration')
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

    def get_diagnostic_write_to_string(self,action):
        self.diagnostic_write_to += f'{round(time.time() - self.active_duration,5)} - {action}\n\n'
    def enter_dungeon(self):
        print('entering dungeon')
        self.get_diagnostic_write_to_string('entering dungeon')
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

    # def do_movements(self,movement_string):
    #
    #     movement_list = movement_string.split('\n')
    #     for movement in movement_list:
    #         command, action = movement.split(' ')
    #         if 'hold' in movement:

    def move_to_boss(self):
        self.get_diagnostic_write_to_string('moving to boss')
        movement_speed = self.movement_speed
        time_helper = 1 - ((movement_speed - 600) / 600)
        time_helper_two = 1 - ((movement_speed - 600) / 600 /2 )

        self.keyboard.press('a')
        self.keyboard.press(self.dodge_button)
        self.keyboard.release(self.dodge_button)
        self.keyboard.release('a')

        path_number = random.randint(0,1)
        print(f'taking path {path_number}')
        time.sleep(0.2)
        print('moving')

        # path_number = 1

        # self.movement_record_bool = True
        if self.movement_record_bool:
            self.movement_record_timer = time.time()
            self.do_dungeon = False
        elif path_number == 0:
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
            time.sleep(8.2 * time_helper)
            self.keyboard.release('w')
        elif path_number == 1:
            time_helper = 1
            self.keyboard.press('w')
            self.keyboard.press(Key.shift)
            self.keyboard.release(Key.shift)
            time.sleep(4.56 * time_helper)
            self.keyboard.press('5')
            self.keyboard.release('5')
            time.sleep(4.17 * time_helper)
            self.keyboard.press('a')
            time.sleep(1.24 * time_helper)
            self.keyboard.release('a')
            time.sleep(6.76 * time_helper)
            self.keyboard.press(Key.shift)
            self.keyboard.release(Key.shift)
            time.sleep(2.76 * time_helper)
            self.keyboard.press('d')
            time.sleep(4.81 * time_helper)
            self.keyboard.release('d')
            time.sleep(5.43 * time_helper)
            self.keyboard.release('w')
        else:
            time_helper = 1



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
        self.get_diagnostic_write_to_string('performing combo sequence')
        skill_counter = 0
        self.combo_sequence = self.check_combo_sequence()
        while self.do_dungeon or self.do_combo:
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
                            if current_combo not in skill_status_p1:
                                break
                            self.do_skill(current_combo)
                            time.sleep(0.1)
                    else:
                        break
            skill_counter += 1
    def do_clear_monsters(self):
        self.get_diagnostic_write_to_string('clearing monsters')
        idle_counter = 0
        while self.do_dungeon:
            if self.check_target(pyautogui.screenshot(region=self.check_target_coord)):
                idle_counter = 0
                screen_shot = pyautogui.screenshot(region=self.check_skill_coord)
                skill_status_p1 = self.check_available_skill_list(screen_shot)
                if skill_status_p1[0] == 0:
                    self.keyboard.press(Key.f5)
                else:
                    self.do_skill(skill_status_p1[0])
            else:
                self.keyboard.press(Key.tab)
                self.keyboard.release(Key.tab)
                idle_counter +=1
            if idle_counter == 10:
                break
    def do_skill(self,skill_slot_to_do):
        charge_skills = [2,3] # need to config or possibly self.
        skill_key_to_do = self.skill_dict[skill_slot_to_do]
        if isinstance(skill_key_to_do, list):
            self.keyboard.press(skill_key_to_do[0])
            self.keyboard.press(skill_key_to_do[1])
            if skill_slot_to_do in charge_skills:
                time.sleep(1)
            self.keyboard.release(skill_key_to_do[0])
            self.keyboard.release(skill_key_to_do[1])
        else:
            self.keyboard.press(skill_key_to_do)
            if skill_slot_to_do in charge_skills:
                time.sleep(1)
            self.keyboard.release(skill_key_to_do)
    def do_exit_sequence(self, end_timer):
        self.get_diagnostic_write_to_string('exiting dungeon')
        have_not_exited = True
        while self.do_dungeon:
            time.sleep(0.1)
            screen_shot_check_loading_screen = pyautogui.screenshot(region=self.check_loading_screen_coord)
            if have_not_exited and self.check_loading_screen(screen_shot_check_loading_screen)[0] == self.check_loading_screen_value:
                if end_timer == 10:
                    time.sleep(0.2)
                    self.keyboard.press('b')
                    self.keyboard.release('b')
                    time.sleep(5.1)
                else:
                    time.sleep(0.2)
                    self.keyboard.press('b')
                    self.keyboard.release('b')
                    teleport_counter = 0
                    while self.do_dungeon:
                        teleport_counter +=1
                        if teleport_counter > 5:
                            break
                        self.keyboard.press(Key.tab)
                        self.keyboard.release(Key.tab)
                        if self.check_target(pyautogui.screenshot(region=self.check_target_coord)):
                            self.phase_counter = 2
                            break
                        time.sleep(1.02)
            else:
                have_not_exited = False
                screen_shot_check_loading_screen = pyautogui.screenshot(region=self.check_loading_screen_coord)
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
                        self.do_clear_monsters()
                    else:
                        print('boss is dead')

                if self.phase_counter == 4: # ------------------------ exit the dungeon
                    self.do_exit_sequence(3)
                    print(f'raid time complete: {time.time() - timer}')
                self.phase_counter += 1

    def on_press(self,key):
        # print('{0}'.format(key))
        if self.movement_record_bool:
            if self.button_open:
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift', "'q'"]:
                    self.button_open = False
                    new_time = time.time()
                    print(f'time.sleep({round(new_time - self.movement_record_timer,2)} * time_helper)')
                    print(f'self.keyboard.press({'{0}'.format(key)})')
                    self.movement_record_timer = new_time
            elif self.button_open_two:
                if '{0}'.format(key) in ["'w'", "'a'", "'s'", "'d'", "'5'", 'Key.shift', "'q'"]:
                    self.button_open_two = False
                    new_time = time.time()
                    print(f'time.sleep({round(new_time - self.movement_record_timer,2)} * time_helper)')
                    print(f'self.keyboard.press({'{0}'.format(key)})')
                    self.movement_record_timer = new_time
            # print(new_time - self.timer)

    def on_release(self,key):
        # print('{0}'.format(key))
        if self.movement_record_bool and '{0}'.format(key) in ["'w'","'a'","'s'","'d'","'5'", 'Key.shift',"'q'"]:
        # if self.movement_record_bool:
            if not self.button_open:
                self.button_open = True
                new_time = time.time()
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'"]:
                    print(f'time.sleep({round(new_time - self.movement_record_timer,2)} * time_helper)')
                print(f'self.keyboard.release({'{0}'.format(key)})')
                self.movement_record_timer = new_time
            elif not self.button_open_two:
                self.button_open_two = True
                new_time = time.time()
                if '{0}'.format(key) in ["'w'","'a'","'s'","'d'"]:
                    print(f'time.sleep({round(new_time - self.movement_record_timer,2)} * time_helper)')
                print(f'self.keyboard.release({'{0}'.format(key)})')
                self.movement_record_timer = new_time

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
        skip_skill_slot = [5]
        attacks_p1 = [1,2,3,4,5,6,7,8,9,10,11,12]
        available_skills = []
        temp_all = []
        slot_count = 1
        inc_counter = 0
        for x_coord in self.skill_pixel_edge:
            if slot_count not in skip_skill_slot:
                skill_value = gray[0][x_coord]
                temp_all.append((slot_count, int(skill_value)))
                if skill_value == self.skill_list_available[inc_counter]:
                    if slot_count in attacks_p1:
                        # available_attacks.append((slot_count, int(skill_value)))
                        available_skills.append(slot_count)
            slot_count += 1
            inc_counter += 1
        if len(available_skills) ==0:
            available_skills.append(0)
        if self.quick_scan:
            print(f'check all available skill list: {temp_all}')
            print(f'check available skill list: {available_skills}')
        self.get_diagnostic_write_to_string(f'check skills {round(time.time()-temp_time,6)} {available_skills}')
        return available_skills

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
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.quick_scan:
            print(f'check target {gray[0]}')

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
                    self.get_diagnostic_write_to_string(f'check target {round(time.time() - temp_time, 6)} {gray[0]}')
                    return False
            self.get_diagnostic_write_to_string(f'check target {round(time.time() - temp_time, 6)} {gray[0]}')
            return True

    def check_loading_screen(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.quick_scan:
            print(f'check loading screen: {gray[0]}')
        return gray[0]

    def start_assist(self):
        print("started throne script")
        try:
            t1 = threading.Thread(target=self.while_loop)
            listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
            t1.start()
            listener_key.start()
            t1.join()
            listener_key.join()
        except Exception as e:
            print(e)
        print('ending script')
        time_stamp_str = datetime.datetime.now().__str__().split('.')[0].replace(' ','_',).replace(':','_')
        diagnostic_file = open(f'debug\\{time_stamp_str}_diagnostic.txt','w')
        diagnostic_file.write(self.diagnostic_write_to)

if __name__ =="__main__":

    melee_assist = throne_script()
    melee_assist.start_assist()