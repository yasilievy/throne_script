import time, pyautogui, pynput, threading, cv2, pytesseract
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput import keyboard, mouse

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\yvyan\\OneDrive\\Documents\\Saint Thomas Courses\\SEIS739\\django_demo\\clicklate\\Tesseract-OCR\\tesseract.exe'
class Throne_Initialize_Config:
    def __init__(self):
        self.initialize_bool = True
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.coordinate_dict = {}

    def define_coordinates(self):
        coordinate_values_file = open('coordinate_values.txt','r')
        coordinate_names_file = open('coordinate_names.txt','r')
        coordinate_names = coordinate_names_file.read().split('\n')
        coordinate_names_file.close()
        if len(coordinate_values_file.read()) == 0:
            print('initiating coordinate setup')
    #
    def start_initialize(self):

        while self.initialize_bool:
            pass



    # def initialize_config(self):
    #     time.sleep(0.2)
    #     pyautogui.hotkey('alt', 'tab')
    #     self.config_file = open('throne_script_config.txt', 'r+')
    #     config_file_read = self.config_file.read()
    #     if len(config_file_read) == 0:
    #         self.initial_skill_list_scan = True
    #         write_to = ''
    #         print('config file is empty\nstarting initialization')
    #         print('setting target values')
    #         print('please target something')
    #         # initial_screenshot = None
    #         while True:
    #             time.sleep(0.5)
    #             initial_screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    #             if self.check_target(initial_screenshot):
    #                 print('setting target values completed')
    #                 write_to += f'target_value={self.target_check_values}\n'  # value is set in self.check_target()
    #                 break
    #         print('setting skill list values')
    #         self.initialize_skill_list_check(initial_screenshot)
    #         write_to += f'skill_values={','.join(str(v) for v in self.skill_list_available)}'  # value is set in self.initialize_skill_list_check()
    #         print('setting skill list values completed')
    #
    #         self.config_file.write(write_to)
    #         self.config_file.close()
    #         self.initial_skill_list_scan = False
    #     else:
    #         print('config file exists, skipping initialization')
    #         self.config_file.close()
    #         config_file_read_split = config_file_read.split('\n')
    #         for line in config_file_read_split:
    #             print(line)
    #             setting, value = line.split('=')
    #             if 'target' in setting:
    #                 self.target_check_values = int(value)
    #             if 'skill' in setting:
    #                 config_skill_counter = 0
    #                 for skill_value in value.split(','):
    #                     self.skill_list_available[config_skill_counter] = int(skill_value)
    #                     config_skill_counter += 1
    def on_release(self,key):
        if key == keyboard.Key.esc:
            # self.static_bool = False
            return False
        if '+' in '{0}'.format(key):  # ------------------- require attention here -------------------
            print(self.mouse.position)
            print(self.scan_coordinate())
    def on_press(self, key):
        pass

    def scan_coordinate(self):
        screen_shot = pyautogui.screenshot(region=(25,1120,95,25))
        screen_shot.save('test1.png')
        return pytesseract.image_to_string(screen_shot)

    def start_assist(self):
        print("started throne script")
        t1 = threading.Thread(target=self.start_initialize)
        listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        t1.start()
        listener_key.start()
        t1.join()
        listener_key.join()
    #



if __name__ =="__main__":
    script = Throne_Initialize_Config()
    script.start_assist()

