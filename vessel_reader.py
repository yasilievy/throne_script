import time, cv2, numpy as np, pyautogui

class vessel_reader:
    def __init__(self):
        self.target_health_x1 = 362
        self.target_health_y1 = 745
        self.target_health_x2 = 490
        self.target_health_y2 = 746

        self.self_health_x1 = 890
        self.self_health_y1 = 535
        self.self_health_x2 = 891
        self.self_health_y2 = 536

        self.self_mana_x1 = 650
        self.self_mana_y1 = 551
        self.self_mana_x2 = 940
        self.self_mana_y2 = 552

        self.target_health = ((362,745),(490,746))
        self.self_health = ((0,0),(0,0))
        self.self_mana = ((0,0),(0,0))
        # self.first_party_member_health =


    # def flash_vessel(self,x1,y1,x2,y2,type):
    def flash_vessel(self,input_type):
        temp_time = time.time()
        if input_type == 'target':
            x1 = self.target_health_x1
            y1 = self.target_health_y1
            x2 = self.target_health_x2
            y2 = self.target_health_y2
        img = pyautogui.screenshot()
        # loc = "ss\\"
        # name = "study3.png"
        # img = cv2.imread(loc+name)
        ss = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        ss_crop = ss[y1:y2,x1:x2]
        ss_gray = cv2.cvtColor(ss_crop, cv2.COLOR_BGR2GRAY)
        # print(ss_gray)
        # print(f'size: {len(ss_gray[0])} time elapsed: {time.time() - temp_time}')
        return ss_gray[0]
    def define_coord(self):
        pass