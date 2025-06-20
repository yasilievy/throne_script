import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'

class throne_script:
    def __init__(self):
        self.esc_delay_bool = False
        self.button_press = False
        self.static_bool = True
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.do_combo = False
        self.combo_to_do = 0
        self.do_option = False
        self.second_esc_to_halt = False
        self.do_nav = False
        self.do_exit = False
        self.do_move = False
        self.do_contracts = False
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

        self.check_target_coord = (1064, 810, 9, 1)
        self.target_check_values = 115 # need to scan a screenshot

        self.check_skill_coord = (0, 1045, 1920, 1)

        self.initialize_config()

        self.script_to_do = 0


        self.skill_pause_counter = 0
        self.skill_pause_bool = False
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
        self.skill_charge = [3]
        self.skill_charge_hold_time = 1
        self.second_cast_skill = [11]
        # self.second_cast_skill = []

    def initialize_config(self):
        time.sleep(0.2)
        pyautogui.hotkey('alt','tab')
        self.config_file = open('throne_script_config.txt','r+')
        config_file_read = self.config_file.read()
        if len(config_file_read) == 0:
            self.initial_skill_list_scan = True
            write_to = ''
            print('config file is empty\nstarting initialization')
            # print('setting target values')
            # print('please target something')
            # # initial_screenshot = None
            # while True:
            #     time.sleep(0.5)
            #     initial_screenshot = pyautogui.screenshot(region=self.check_target_coord)
            #     # screen_shot = pyautogui.screenshot(region=(0,1045,1920,1))
            #     if self.check_target(initial_screenshot):
            #         print('setting target values completed')
            #         write_to += f'target_value={self.target_check_values}\n' # value is set in self.check_target()
            #         break
            print('setting skill list values')
            initial_screenshot = pyautogui.screenshot(region=self.check_skill_coord)

            self.initialize_skill_list(initial_screenshot,)
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
    def check_combo_sequence(self):
        combo_sequence_open = open('combo_sequence\\combo_sequence.txt','r')
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
            if skill_counter == len(self.combo_sequence):
                break
            else:
                print(f'need to cast skill: {self.combo_sequence[skill_counter]}')
                while self.do_dungeon or self.do_combo:
                    current_combo = self.combo_sequence[skill_counter]
                    screen_shot = pyautogui.screenshot(region=self.check_skill_coord)
                    # screen_shot_two = pyautogui.screenshot(region=(637,993,1329,1))
                    screen_shot_two = pyautogui.screenshot(region=(0,993,1920,1))
                    # screen_shot_two = pyautogui.screenshot(region=(587,993,1279,1))
                    skill_status_p1 = self.check_available_skill_list(screen_shot,screen_shot_two)[0]
                    if len(skill_status_p1) != 0:
                        rendered_skill_status_p1 = [s_s_p1[0] for s_s_p1 in skill_status_p1]
                        # if current_combo == 12:
                        #     self.skill_pause_counter = True
                        if current_combo not in rendered_skill_status_p1:
                            break
                        elif current_combo in self.skill_charge:  #
                            self.keyboard.press(self.skill_dict[current_combo])
                            time.sleep(self.skill_charge_hold_time)
                            self.keyboard.release(self.skill_dict[current_combo])
                        # elif current_combo == 4:
                        #     self.keyboard.press(self.skill_dict[current_combo])
                        #     self.keyboard.release(self.skill_dict[current_combo])
                        #     time.sleep(0.1)
                        #     self.keyboard.press(self.skill_dict[current_combo])
                        #     self.keyboard.release(self.skill_dict[current_combo])
                        else:
                            self.keyboard.press(self.skill_dict[current_combo])
                            self.keyboard.release(self.skill_dict[current_combo])
                        # time.sleep(0.1)
            skill_counter += 1


    def while_loop(self):
        pyautogui.hotkey('alt', 'tab')


        while self.static_bool:
            while self.do_nav:
                self.keyboard.press(Key.f10)
                self.keyboard.release(Key.f10)
                time.sleep(0.2)
                self.mouse.position = (554,132)
                self.mouse.click(Button.left)
                time.sleep(0.2)
                self.mouse.position = (960,1005)
                self.mouse.click(Button.left)
                self.do_nav = False

            while self.do_option:

                print('esc - halt\n')
                option_counter = 1
                while self.do_option and option_counter <5:
                    print(f'{option_counter} of 5 time lapsed')
                    option_counter+=1
                    time.sleep(1)
                self.do_option = False
            while self.do_combo:
                self.do_combo_sequence()
                self.do_combo = False
                print('combo completed')
            # print(f'test distance {self.check_distDance(pyautogui.screenshot(region=(1024, 821, 16, 1)))}')
            # print(f'read distance {self.read_distance(pyautogui.screenshot(region=(1022, 819, 27, 13)))}')
            # self.check_distancet(pyautogui.screenshot(region=(1037, 825, 1, 1)))
            # self.check_distancet(pyautogui.screenshot(region=(1026, 821, 3, 1)))

            time.sleep(0.1)
            unstuck_sequence_one = [('a', 1.5)]
            unstuck_sequence_two = [('d', 1.5)]
            unstuck_sequence_bool = True
            unstuck_sequence_to_do = []

            no_target_counter = 0
            jump_counter = 0
            next_target_counter = 0
            truly_stuck_counter = 0
            alter_bool_two = True
            alter_camera_bool = True
            unstuck_time_counter = 0
            locked_boolean = False
            while self.do_bot:
                temp_time = time.time()
                time_sleep = 0.1
                # if 'sight' in self.check_target_out_sight(
                #         pyautogui.screenshot(region=(820, 250, 280, 20))):
                # if 'sight' in self.check_target_out_sight(
                #         pyautogui.screenshot(region=(825, 255, 7,1))):
                #     print('sight, detected')
                    # if locked_boolean:
                    #     pass
                    # else:
                    #     time.sleep(0.1)
                    #     self.mouse.position = (
                    #     1200, 775)  # ------------------- require attention here -------------------
                    #     self.mouse.click(Button.left)
                    #     # self.keyboard.press(Key.alt)
                    #     # self.keyboard.release(Key.alt)
                    # self.keyboard.press('w')
                    # self.keyboard.press(Key.shift)
                    # self.keyboard.release(Key.shift)
                    # # self.keyboard.press(Key.space)
                    # # self.keyboard.release(Key.space)
                    # unstuck_boolean = True
                    # locked_boolean = True
                    # # while unstuck_boolean and self.do_bot:
                    # #     if self.check_target_health(pyautogui.screenshot(region=(1216, 802, 1, 1))) < 20:
                    # #         self.keyboard.release('w')
                    # #         unstuck_boolean = False
                    #
                    #         # break
                    #     # print(unstuck_time_counter)
                    # if unstuck_sequence_bool:
                    #     unstuck_sequence_to_do = unstuck_sequence_one
                    #     unstuck_sequence_bool = False
                    # else:
                    #     unstuck_sequence_to_do = unstuck_sequence_two
                    #     unstuck_sequence_bool = True
                    # for unstuck_move in unstuck_sequence_to_do:
                    #     next_target_counter += 1
                    #     self.keyboard.press(unstuck_move[0])
                    #     self.keyboard.press(Key.space)
                    #     self.keyboard.release(Key.space)
                    #     time.sleep(unstuck_move[1])
                    #     self.keyboard.release(unstuck_move[0])
                    #     # self.keyboard.press(skill_dict[12])
                    #     # self.keyboard.release(skill_dict[12])
                    #     # if self.check_target_health(pyautogui.screenshot(region=(1216, 802, 1, 1))) < 20:
                    #     #     self.keyboard.release('w')
                    #     #         unstuck_boolean = False
                    #     #         break
                    #
                    #     unstuck_time_counter += 0.5

                # if truly_stuck_counter == 50:
                #     self.keyboard.press('s')
                #     time.sleep(1)
                #     self.keyboard.press(Key.space)
                #     self.keyboard.release(Key.space)
                #     time.sleep(1)
                #     self.keyboard.release('s')
                #     truly_stuck_counter= 0
                # if next_target_counter == 2:
                #     locked_boolean = False
                #     if alter_bool_two:
                #         self.keyboard.press(Key.right)
                #         alter_bool_two = False
                #     else:
                #         self.keyboard.press(Key.left)
                #         alter_bool_two = False
                #     alter_bool = True
                #     while self.do_bot:
                #         if alter_bool:
                #             self.mouse.click(Button.right)
                #             alter_bool = False
                #         else:
                #             self.keyboard.press(Key.tab)
                #             self.keyboard.release(Key.tab)
                #             alter_bool = True
                #         self.mouse.click(Button.right)
                #         if self.check_target(pyautogui.screenshot(region=(1064, 810, 9, 1))):
                #             self.keyboard.release(Key.right)
                #             self.keyboard.release(Key.left)
                #             break
                #     next_target_counter = 0
                screen_shot = pyautogui.screenshot(region=(0,1045,1920,1))
                skill_status_p1,  skill_status_p2, distance_status, buff_status,  = self.initialize_skill_list_check(screen_shot,2)
                if buff_status != 0:
                    # print(f'casting buff {buff_status}')
                    self.keyboard.press(self.skill_dict[buff_status])
                    self.keyboard.release(self.skill_dict[buff_status])
                    time_sleep = 0
                if self.check_target(pyautogui.screenshot(region=(1064, 810, 9, 1))):
                    truly_stuck_counter +=1
                    no_target_counter = 0
                    if self.check_target_health(pyautogui.screenshot(region=(1216, 802, 1, 1))) < 20:
                        # print('damaged health, using attack skill')
                        unstuck_time_counter = 0
                        jump_counter = 0
                        if skill_status_p1 != 0:
                            skill_to_use = self.skill_dict[skill_status_p1]
                            if skill_status_p1 == 20 or skill_status_p1 == 3:
                                self.keyboard.press(skill_to_use)
                                time.sleep(1)
                                self.keyboard.release(skill_to_use)
                            else:
                                self.keyboard.press(skill_to_use)
                                self.keyboard.release(skill_to_use)
                        elif skill_status_p2 != 0:
                            skill_to_use = self.skill_dict[skill_status_p2]
                            # print(f'casting attack skill {skill_to_use}')
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                        else:
                            self.keyboard.press(Key.f5)
                            self.keyboard.release(Key.f5)



                #     else:
                #         # print('undamaged, using distance skill')
                #         # distance_scan = self.check_distance(pyautogui.screenshot(region=(1039, 827, 7, 1)))
                #         distance_scan = self.check_distancet(pyautogui.screenshot(region=(1026, 821, 3, 1)))
                #         # distance_scan_two = self.check_distancet(pyautogui.screenshot(region=(1037, 825, 1, 1)))
                #         # print(distance_scan)
                #
                #         # print(f'test distance {self.check_distance(pyautogui.screenshot(region=(1024, 830, 15, 1)))}')
                #         # print(f'read distance {self.read_distance(pyautogui.screenshot(region=(1022, 819, 27, 13)))}')
                #         # read_distance = self.read_distance(pyautogui.screenshot(region=(1022, 819, 27, 13)))
                #         # print(read_distance)
                #         # print(f'test distance {self.check_distance(pyautogui.screenshot(region=(1024, 825, 22, 1)))}')
                #         # print(f'target distance {distance_scan}')
                #         if distance_scan > 2 and distance_status != 0:
                #             # print(distance_scan)
                #         # if read_distance >15 and distance_status !=0:
                #             skill_to_use = skill_dict[distance_status]
                #             # print(f'casting distance skill {skill_to_use}')
                #             if distance_status == 4:
                #                 self.keyboard.press(skill_to_use)
                #                 self.keyboard.release(skill_to_use)
                #                 time.sleep(0.1)
                #                 self.keyboard.press(skill_to_use)
                #                 self.keyboard.release(skill_to_use)
                #
                #                 time.sleep(0.1)
                #                 self.keyboard.press(skill_to_use)
                #                 self.keyboard.release(skill_to_use)
                #             else:
                #                 self.keyboard.press(skill_to_use)
                #                 self.keyboard.release(skill_to_use)
                #         else:
                #             # if skill_status_p1 != 0:
                #             #     skill_to_use = skill_dict[skill_status_p1]
                #             #     self.keyboard.press(skill_to_use)
                #             #     self.keyboard.release(skill_to_use)
                #             # elif skill_status_p2 != 0:
                #             #     skill_to_use = skill_dict[skill_status_p2]
                #             #     self.keyboard.press(skill_to_use)
                #             #     self.keyboard.release(skill_to_use)
                #             # else:
                #                 self.keyboard.press(Key.f5)
                #                 self.keyboard.release(Key.f5)
                #         jump_counter += 1
                #     if jump_counter == 20:
                #         if locked_boolean:
                #             pass
                #         else:
                #             time.sleep(0.1)
                #             self.keyboard.press(Key.alt)
                #             self.keyboard.release(Key.alt)
                #             self.mouse.position = (
                #             1200, 775)  # ------------------- require attention here -------------------
                #             self.mouse.click(Button.left)
                #             self.keyboard.press(Key.alt)
                #             self.keyboard.release(Key.alt)
                #             self.keyboard.press(Key.tab)
                #             self.keyboard.release(Key.tab)
                #         if unstuck_sequence_bool:
                #             unstuck_sequence_to_do = unstuck_sequence_one
                #             unstuck_sequence_bool = False
                #         else:
                #             unstuck_sequence_to_do = unstuck_sequence_two
                #             unstuck_sequence_bool = True
                #         for unstuck_move in unstuck_sequence_to_do:
                #             next_target_counter += 1
                #             self.keyboard.press(unstuck_move[0])
                #             self.keyboard.press(Key.space)
                #             self.keyboard.release(Key.space)
                #             time.sleep(unstuck_move[1])
                #             self.keyboard.release(unstuck_move[0])
                #         # time.sleep(0.1)
                #         # self.mouse.position = (
                #         # 1200, 775)  # ------------------- require attention here -------------------
                #         # self.mouse.click(Button.left)
                #         # self.keyboard.press('w')
                #         # self.keyboard.press(Key.space)
                #         # self.keyboard.release(Key.space)
                #         # self.keyboard.release('w')
                #         # jump_counter = 0
                # else:
                #     locked_boolean = False
                #     unstuck_time_counter = 0
                #     jump_counter = 0
                #     no_target_counter +=1
                #     truly_stuck_counter = 0
                #     # self.keyboard.press(Key.f5)
                #     # self.keyboard.release(Key.f5)
                #     self.keyboard.press(Key.tab)
                #     self.keyboard.release(Key.tab)
                #     time.sleep(0.05)
                #     if no_target_counter > 2:
                #         if alter_camera_bool:
                #             self.keyboard.press(Key.right)
                #             alter_camera_bool = False
                #         else:
                #             self.keyboard.press(Key.left)
                #             alter_camera_bool = True
                #         alter_target_bool = True
                #         while self.do_bot:
                #             if alter_target_bool:
                #                 self.mouse.click(Button.right)
                #                 alter_target_bool = False
                #             else:
                #                 self.keyboard.press(Key.tab)
                #                 self.keyboard.release(Key.tab)
                #                 alter_target_bool = True
                #             if self.check_target(pyautogui.screenshot(region=(1064, 810, 9, 1))):
                #             # if self.check_target(pyautogui.screenshot(region=(1228, 795, 12, 1))):
                #                 self.keyboard.release(Key.right)
                #                 self.keyboard.release(Key.left)
                #                 break
                # print(time.time() - temp_time)

            while self.do_contracts:
                skill_set = 1
                screen_shot = pyautogui.screenshot(region=(0,1045,1920,1))
                skill_status_p1,  skill_status_p2, distance_status, buff_status,  = self.initialize_skill_list_check(screen_shot,skill_set)
                if buff_status != 0:
                    self.keyboard.press(self.skill_dict[buff_status])
                    self.keyboard.release(self.skill_dict[buff_status])
                if self.check_target(pyautogui.screenshot(region=(1064, 810, 9, 1))):
                    truly_stuck_counter +=1
                    if skill_status_p1 != 0:
                        skill_to_use = self.skill_dict[skill_status_p1]
                        # self.keyboard.press(skill_to_use)
                        # self.keyboard.release(skill_to_use)
                        if skill_status_p1 == 10: # or skill_status_p1 == 3:
                            self.keyboard.press(skill_to_use)
                            time.sleep(1.1)
                            self.keyboard.release(skill_to_use)
                        elif skill_status_p1 == 4:
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                            time.sleep(0.1)
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                        else:
                            self.keyboard.press(skill_to_use)
                            self.keyboard.release(skill_to_use)
                    elif skill_status_p2 != 0:
                        skill_to_use = self.skill_dict[skill_status_p2]
                        self.keyboard.press(skill_to_use)
                        self.keyboard.release(skill_to_use)
                    else:
                        self.keyboard.press(Key.f5)
                        self.keyboard.release(Key.f5)
                    time.sleep(0.2)

    # mob farm
    def check_distance(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)# | cv2.THRESH_OTSU)
        bw_count = 0
        for x in im_bw[0]:
            if x == 255:
                bw_count +=1
        return bw_count

    def check_distancet(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh, im_bw = cv2.threshold(gray, 7, 255, cv2.THRESH_BINARY)# | cv2.THRESH_OTSU)
        # print(thresh)
        bw_count = 0
        for x in im_bw[0]:
            if x == 255:
                bw_count +=1
        print(f'{bw_count} {im_bw[0]} ')
        return bw_count

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
        # if '4' in '{0}'.format(key):
        #     if self.button_press:
        #         self.button_press = False
        #     else:
        #         self.button_press = True
        #         self.keyboard.press('4')
        #         self.keyboard.release('4')
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
            if self.do_option:
                print('second esc pressed, halting script')
                self.static_bool = False
                self.do_option = False
                return False
            else:
                print('esc pressed, select option below:')
                self.do_option = True



        # if '`' in '{0}'.format(key):
        #     if self.do_contracts:
        #         print('turning off contracts')
        #         self.do_contracts = False
        #     else:
        #         print('turning on contracts')
        #         self.do_contracts = True
            # if self.do_bot:
            #     print('turning off script')
            #     self.do_bot = False
            # else:
            #     print('turning on script')
            #     self.do_bot = True


        if '`' in '{0}'.format(key):

            if self.do_combo:
                print('turning off bot')
                self.do_combo = False
            else:
                print('turning on bot')
                self.do_combo = True
        if '/' in '{0}'.format(key):

            if self.do_nav:
                print('turning off nav')
                self.do_nav = False
            else:
                print('turning on nav')
                self.do_nav = True


    # polish crystal farm
    def check_available_skill_list(self, ss,sst):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_two = cv2.cvtColor(np.array(sst), cv2.COLOR_RGB2BGR)
        gray_two = cv2.cvtColor(img_two, cv2.COLOR_BGR2GRAY)
        party_box_x1 = 605
        second_skill_cast_x1 = 620
        first_inc = [0, 58, 57, 58, 58, 59, 0, 58, 58, 58, 58, 57]
        skip_skill_slot = []
        available_attacks_p1 = []
        temp_all = []
        slot_count = 1
        accum = 0
        inc_counter = 0
        for inc in first_inc:
            if slot_count == 7:
                party_box_x1 = 1009
                second_skill_cast_x1 = 1025
                accum = 0
            if slot_count not in skip_skill_slot:
                accum += inc
                skill_value = gray[0][party_box_x1 + accum]
                temp_all.append((slot_count,int(skill_value)))
                # print(f'{slot_count} : {skill_value}')
                if skill_value == self.skill_list_available[inc_counter]:
                    if slot_count in self.second_cast_skill:
                        second_skill_cast_value = gray_two[0][second_skill_cast_x1 + accum]
                        if second_skill_cast_value >= 100 and second_skill_cast_value <= 240:
                            print(f'passed slot count: {slot_count}')
                            print(f'passed cast value: {second_skill_cast_value}')
                            # pass
                        else:
                            print(f'use slot count: {slot_count}')
                            print(f'use cast value: {second_skill_cast_value}')
                            available_attacks_p1.append((slot_count, int(skill_value)))
                    else:
                        available_attacks_p1.append((slot_count, int(skill_value)))

            slot_count += 1
            inc_counter += 1
        # print(temp_all)
        return_command = [available_attacks_p1]#,available_attacks_p2, available_distances, available_buffs]
        # print(f'time: {round(time.time()-temp_time,6)}')
        return return_command

    def initialize_skill_list(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        initialize_inc = [0,58,57,58,58,59,0,58,58,58,58,57]
        skip_skill_slot = []
        x1 = 605 # is a config
        slot_count = 1
        inc_counter = 0
        x1_accum = 0
        for inc in initialize_inc:
            if slot_count == 7:
                x1 = 1009 # is a config
                x1_accum = 0
            if slot_count not in skip_skill_slot:
                x1_accum += inc
                skill_pixel_value = gray[0][x1 + x1_accum]
                self.skill_list_available[inc_counter] = skill_pixel_value
            slot_count += 1
            inc_counter += 1
        self.initial_skill_list_scan = False

    # mob farm
    def read_distance(self,ss):
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        # img2 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        distance_read = pytesseract.image_to_string(im_bw)
        print(distance_read)
        if len(distance_read) !=0 and distance_read.isdigit():
            return int(distance_read)
        # return pytesseract.image_to_string(im_bw)
        return 15

    # mob farm / polish crystal farm
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

    # mob farm
    def initialize_skill_list_check(self, ss, skill_set):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if skill_set == 1:
            # contracts
            attacks_p1 = [7,1,6,5,2,3,9]
            attacks_p2 = []
            distances = []
            buffs = [8]
        elif skill_set == 2:
            # skill set 3 nebula pve manual solo
            attacks_p1 = [4,5,6,7,8,9]
            attacks_p2 = [10,11,12]
            distances = []
            buffs = [1,2,3]

            attacks_p1 = [4,5,6,7,8,9,10,11,12]
            attacks_p2 = []
            distances = []
            buffs = [1,2,3]
        else:
            # skill set 4 field auto
            attacks_p1 = [9, 1, 2, 3, 6, 7, 5]
            attacks_p2 = []
            distances = [4, 10, 11, 12]
            buffs = [8]
            # buffs = [8,9]

            # skill set 10 spear
            attacks_p1 = [1,7,6,5,2,3,9]
            attacks_p2 = []
            # distances = [4,10,11,12]
            distances = []
            buffs = [8]
            # buffs = [8]


            # attacks_p1 = [2,3,4,5]
            # attacks_p2 = [6,7,8]
            # distances = [9,10,11,12]
            # buffs = [1]
            #
            # attacks_p1 = [6,5,2,3]
            # attacks_p2 = [1,7]

            # pvp attempt for now
            # attacks_p1 = [4,5,6,7,8,9]
            # attacks_p2 = [3,10,11]
            # distances = [12]
            # buffs = [1,2]

            # attacks_p1 = [4,5,6,7,8,9,10,11,12]
            # attacks_p2 = []
            # distances = []
            # buffs = [1,2]

        # available_attacks_p1 = []
        # available_attacks_p2 = []
        # available_distances = []
        # available_buffs = []
        # available_skill_set_list = [available_attacks_p1,available_attacks_p2,available_distances,available_buffs]

        skill_set_list = [attacks_p1,attacks_p2,distances,buffs]
        available_skill_set_list = [0,0,0,0]
        first_inc = [0,58,57,58,58,59]
        second_inc = [0,58,58,58,58,57]

        skip_skill_slot = []
        temp_skill_skill_value = []
        skill_set_counter = 0
        for skill_set in skill_set_list:
            for skill in skill_set:
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
            skill_set_counter +=1
        # print(temp_skill_skill_value)
        return available_skill_set_list

    def check_mana(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 750
        party_box_y1 = 825
        party_box_x2 = 751
        party_box_y2 = 826
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        return gray[0]

    def check_health(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        party_box_x1 = 785
        party_box_y1 = 805
        party_box_x2 = 786
        party_box_y2 = 806
        img = img[party_box_y1:party_box_y2, party_box_x1:party_box_x2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        return gray[0]

    def check_target_health(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        return gray[0]

    def check_target_out_sight(self,ss):
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(f'health time check {time.time()-temp_time}')
        return gray[0]

    def start_assist(self):
        print("started throne script")
        # self.one_execute(self.mouse,self.keyboard)
        t1 = threading.Thread(target=self.while_loop)
        listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()

if __name__ =="__main__":

    melee_assist = throne_script()
    melee_assist.start_assist()