import pytesseract, pyautogui, time, numpy as np, threading,cv2
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'C:\\OCR\\tesseract.exe'

class throne_script:
    def __init__(self):
        self.double_click_bool = False
        self.button_press = False # double click for target skills
        self.static_bool = True
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.button = mouse.Button
        self.do_combo = False
        self.do_option = False
        self.do_nav = False
        self.do_contracts = False
        self.timer = time.time()
        self.initial_skill_list_scan = True
        self.skill_list_available = [0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.check_target_coord = (1064, 810, 9, 1)
        self.target_check_values = 115 # need to scan a screenshot

        self.check_skill_coord = (0, 1045, 1920, 1)

        self.initialize_config()

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


        self.skill_charges = [3]
        self.skill_charges_hold_time = 1
        self.second_cast_skills = [11]
        self.current_do_option = 1
        self.option_dict = {
            1:'combo sequence',
            2:'manual auto-fire'
        }
        self.selected_skill_set = 0

    def on_release(self,key):
        if self.double_click_bool and '4' in '{0}'.format(key):
            if self.button_press:
                self.button_press = False
            else:
                self.button_press = True
                self.keyboard.press('4')
                self.keyboard.release('4')
        # print('{0}'.format(key))
        if self.do_option:
            if key == keyboard.Key.f5:
                self.current_do_option = 1
                self.do_option = False
            if key == keyboard.Key.f6:
                self.current_do_option = 2
                self.do_option = False
            if key == keyboard.Key.f7:
                if self.double_click_bool:
                    self.double_click_bool = False
                else:
                    self.double_click_bool = True
        if key == keyboard.Key.esc:
            if self.do_option:
                print('second esc pressed, halting script')
                self.static_bool = False
                self.do_option = False
                return False
            else:
                print('esc pressed, select option below:')
                self.do_option = True

        elif '/' in '{0}'.format(key):
            if self.do_nav:
                print('turning off nav')
                self.do_nav = False
            else:
                print('turning on nav')
                self.do_nav = True

        elif '`' in '{0}'.format(key):
            if self.current_do_option == 1:
                if self.do_combo:
                    print('turning off combo sequence')
                    self.do_combo = False
                else:
                    print('turning on combo sequence')
                    self.do_combo = True
            elif self.current_do_option == 2:
                if self.do_contracts:
                    print('turning off manual auto-fire')
                    self.do_contracts = False
                else:
                    print('turning on manual auto-fire')
                    self.do_contracts = True


    def while_loop(self):
        # pyautogui.hotkey('alt', 'tab')
        #
        print(f'current option: {self.option_dict[self.current_do_option]}')
        while self.static_bool:
            while self.do_nav: # secret dungeon auto
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
                print('esc - halt\nf5 - perform skill combo\nf6 - manual auto-fire\nf7 - enable double click')
                option_counter = 1
                while self.do_option and option_counter <= 5:
                    print(f'{option_counter} of 5 time lapsed')
                    option_counter+=1
                    time.sleep(1)
                self.do_option = False
            while self.do_combo:
                self.do_combo_sequence()
                self.do_combo = False
                print('combo completed')

            while self.do_contracts:
                skill_set = 1
                screen_shot = pyautogui.screenshot(region=(0,1045,1920,1))
                skill_status_p1,  skill_status_p2, distance_status, buff_status,  = self.check_available_skills(screen_shot,self.selected_skill_set)
                if buff_status != 0:
                    self.keyboard.press(self.skill_dict[buff_status])
                    self.keyboard.release(self.skill_dict[buff_status])
                if self.check_target(pyautogui.screenshot(region=(1064, 810, 9, 1))):
                    if skill_status_p1 != 0:
                        skill_to_use = self.skill_dict[skill_status_p1]
                        if skill_status_p1 in self.skill_charges:
                            self.keyboard.press(skill_to_use)
                            time.sleep(self.skill_charges_hold_time)
                            self.keyboard.release(skill_to_use)
                        elif skill_status_p1 in self.second_cast_skills:
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


    def on_press(self,key):
        pass

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
                initial_screenshot = pyautogui.screenshot(region=self.check_target_coord)
                if self.check_target(initial_screenshot):
                    print('setting target values completed')
                    write_to += f'target_value={self.target_check_values}\n' # value is set in self.check_target()
                    break
            print('setting skill list values')
            initial_screenshot = pyautogui.screenshot(region=self.check_skill_coord)

            self.initialize_skill_list(initial_screenshot)
            write_to += f'skill_values={','.join(str(v) for v in self.skill_list_available)}'  # value is set in self.check_available_skills()
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

        while self.do_combo:
            if skill_counter == len(self.combo_sequence):
                break
            else:
                print(f'need to cast skill: {self.combo_sequence[skill_counter]}')
                while self.do_combo:
                    current_combo = self.combo_sequence[skill_counter]
                    screen_shot = pyautogui.screenshot(region=self.check_skill_coord)
                    # screen_shot_two = pyautogui.screenshot(region=(637,993,1329,1))
                    screen_shot_two = pyautogui.screenshot(region=(0,993,1920,1))
                    # screen_shot_two = pyautogui.screenshot(region=(587,993,1279,1))
                    skill_status_p1 = self.check_available_skill_list(screen_shot,screen_shot_two)[0]
                    if len(skill_status_p1) != 0:
                        rendered_skill_status_p1 = [s_s_p1[0] for s_s_p1 in skill_status_p1]
                        if current_combo not in rendered_skill_status_p1:
                            break
                        elif current_combo in self.skill_charges:
                            self.keyboard.press(self.skill_dict[current_combo])
                            time.sleep(self.skill_charges_hold_time)
                            self.keyboard.release(self.skill_dict[current_combo])
                        elif current_combo in self.second_cast_skills:
                            self.keyboard.press(self.skill_dict[current_combo])
                            self.keyboard.release(self.skill_dict[current_combo])
                            time.sleep(0.1)
                            self.keyboard.press(self.skill_dict[current_combo])
                            self.keyboard.release(self.skill_dict[current_combo])
                        else:
                            self.keyboard.press(self.skill_dict[current_combo])
                            self.keyboard.release(self.skill_dict[current_combo])
            skill_counter += 1


    def check_available_skill_list(self, ss,sst): # skill check for combo
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
                    if slot_count in self.second_cast_skills:
                        second_skill_cast_value = gray_two[0][second_skill_cast_x1 + accum]
                        if second_skill_cast_value >= 100 and second_skill_cast_value <= 240:
                            print(f'passed slot count: {slot_count}')
                            print(f'passed cast value: {second_skill_cast_value}')
                        else:
                            print(f'use slot count: {slot_count}')
                            print(f'use cast value: {second_skill_cast_value}')
                            available_attacks_p1.append((slot_count, int(skill_value)))
                    else:
                        available_attacks_p1.append((slot_count, int(skill_value)))

            slot_count += 1
            inc_counter += 1
        # print(temp_all)
        return_command = [available_attacks_p1]
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
                    return False
            return True

    def check_available_skills(self, ss, selected_skill_set): # skill check for auto-fire
        temp_time = time.time()
        img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        skill_sets =[
            #[p skill set],[s skill set],[d skill set],[b skill set]
            [[7,1,6,5,2,3,9],[],[],[8]], # manual auto-fire
            [[4,5,6,7,8,9],[10,11,12],[],[1,2,3]], # nebula manual solo
            [[9, 1, 2, 3, 6, 7, 5],[],[4, 10, 11, 12],[8]], # full-auto-farm
        ]
        attacks_p1, attacks_p2, distances, buffs = skill_sets[selected_skill_set]

        skill_set_list = [attacks_p1,attacks_p2,distances,buffs]
        available_skill_set_list = [0,0,0,0]
        first_inc = [0,58,57,58,58,59]
        second_inc = [0,58,58,58,58,57]

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