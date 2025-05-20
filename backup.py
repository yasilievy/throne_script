# move around and attack
def while_loop(self, mouse_c, keyboard_c):
    pyautogui.hotkey('alt', 'tab')

    skill_dict = {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: Key.f7,
        7: Key.f1,
        8: Key.f2
    }

    counter = 0
    counter_two = 0
    health_counter = 0
    unstuck_counter_has_target = 0
    unstuck_counter_no_target = 0
    self.keyboard.press('r')
    self.keyboard.release('r')
    time.sleep(0.2)
    self.keyboard.press(Key.f1)
    self.keyboard.release(Key.f1)
    # self.static_bool = False

    alter_move = True

    while self.static_bool:

        if counter_two == 12:
            self.keyboard.press('r')
            self.keyboard.release('r')
            # time.sleep(0.2)
            # self.keyboard.press(Key.f1)
            # self.keyboard.release(Key.f1)
            time.sleep(0.2)
            self.keyboard.press('c')
            self.keyboard.release('c')
            counter_two = 0
        screen_shot = pyautogui.screenshot()
        check_target = self.check_target(screen_shot)
        if check_target[0] == 32 or check_target[0] == 31 and check_target[1] == 20 or check_target[1] == 19:

            skill_status = self.check_skills(screen_shot)
            if len(skill_status) != 0:
                # print(f'available skills: {skill_status}')
                skill_to_use = skill_dict[skill_status[0]]
                print(f'casting skill {skill_to_use}')
                self.keyboard.press(skill_to_use)
                self.keyboard.release(skill_to_use)
                if self.check_mana(screen_shot)[0] < 20:
                    # if 'mana' in self.check_mana().lower():
                    print('mana recovering')
                    self.keyboard.press(Key.f2)
                    time.sleep(9.2)
                    self.keyboard.release(Key.f2)
                if self.check_health(screen_shot)[0] < 20:
                    print('health recovery')
                    self.keyboard.press('6')
                    self.keyboard.release('6')
                    time.sleep(0.2)
                    self.keyboard.press('x')
                    self.keyboard.release('x')
                    time.sleep(0.2)
                    # self.keyboard.press('c')
                    # self.keyboard.release('c')
            else:
                print('auto attacking')
                self.keyboard.press(Key.f5)
                self.keyboard.release(Key.f5)
            time.sleep(0.7)
            counter_two += 1
            unstuck_counter_no_target = 0
        else:
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)
            time.sleep(0.2)
            self.mouse.position = (1200, 775)
            self.mouse.click(Button.left)
            self.mouse.position = (1250, 775)
            self.mouse.click(Button.left)
            unstuck_counter_no_target += 1

        if unstuck_counter_no_target == 10:
            if alter_move:
                print('moving forward')
                self.keyboard.press('w')
                time.sleep(8)
                self.keyboard.release('w')
                alter_move = False
            else:
                print('moving back')
                self.keyboard.press('s')
                time.sleep(8)
                self.keyboard.release('s')
                alter_move = True
            unstuck_counter_no_target = 0
        counter += 1

# stationary staff
def while_loop(self, mouse_c, keyboard_c):
    pyautogui.hotkey('alt', 'tab')

    skill_dict = {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: Key.f7,
        7: Key.f1,
        8: Key.f2
    }

    counter = 0
    counter_two = 0
    health_counter = 0
    unstuck_counter_has_target = 0
    unstuck_counter_no_target = 0
    self.keyboard.press('r')
    self.keyboard.release('r')
    time.sleep(0.2)
    self.keyboard.press(Key.f1)
    self.keyboard.release(Key.f1)
    # self.static_bool = False

    alter_move = True

    while self.static_bool:
        # if unstuck_counter_no_target == 7:
        #     print('walking back')
        #     self.keyboard.press('s')
        #     time.sleep(1)
        #     self.keyboard.release('s')
        #     unstuck_counter_no_target = 0
        while self.do_bot:
            if counter_two == 5:
                time.sleep(0.2)
                self.keyboard.press(Key.f1)
                self.keyboard.release(Key.f1)
                time.sleep(0.3)
                self.keyboard.press('r')
                self.keyboard.release('r')
                time.sleep(0.2)
                self.keyboard.press('c')
                self.keyboard.release('c')
                time.sleep(0.2)
                self.keyboard.press('x')
                self.keyboard.release('x')
                time.sleep(0.2)
                counter_two = 0
            screen_shot = pyautogui.screenshot()
            check_target = self.check_target(screen_shot)
            if check_target[0] == 32 or check_target[0] == 31 and check_target[1] == 20 or check_target[1] == 19:

                skill_status = self.check_skills(screen_shot)
                if len(skill_status) != 0:
                    # print(f'available skills: {skill_status}')
                    skill_to_use = skill_dict[skill_status[0]]
                    print(f'casting skill {skill_to_use}')
                    self.keyboard.press(skill_to_use)
                    self.keyboard.release(skill_to_use)
                    if self.check_mana(screen_shot)[0] < 20:
                        # if 'mana' in self.check_mana().lower():
                        print('mana recovering')
                        self.keyboard.press(Key.f2)
                        time.sleep(9.2)
                        self.keyboard.release(Key.f2)
                    if self.check_health(screen_shot)[0] < 20:
                        print('health recovery')
                        time.sleep(0.5)
                        self.keyboard.press('6')
                        self.keyboard.release('6')
                        time.sleep(0.5)
                        self.keyboard.press('x')
                        self.keyboard.release('x')
                        time.sleep(0.5)
                        self.keyboard.press('c')
                        self.keyboard.release('c')
                else:
                    print('auto attacking')
                    self.keyboard.press(Key.f5)
                    self.keyboard.release(Key.f5)

                time.sleep(0.7)
                # counter_two += 1
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)
            time.sleep(0.2)
            self.mouse.position = (1200, 775)
            self.mouse.click(Button.left)
            self.mouse.position = (1250, 775)
            self.mouse.click(Button.left)
            counter_two += 1
            counter += 1


# check_skills backup
def check_skills(self, ss):
    temp_time = time.time()
    # ss = pyautogui.screenshot() # region=(0,0,1920,1080)
    # ss.save(loc+name)
    img = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)

    party_box_x1 = 612
    party_box_y1 = 996
    party_box_x2 = 613
    party_box_y2 = 997

    # first_cooldown_fade = [37,25,34,69,18,29] #,34]
    first_cooldown_fade = [37,25,34,69,22,29] #,34]
    # first_cooldown_fade = [35,25,34,69,22,29] #,34]
    first_inc = [0,58,58,58,58,59] #,0]
    # second_cooldown_fade = [,39]#,34,69,18,29]
    second_inc = [0,59] #,58,59,59,59]
    non_cooldown = []
    slot_count = 1
    accum = 0
    for inc in first_inc:
        if slot_count == 7:
            party_box_x1 = 1016
            party_box_x2 = 1017
            accum = 0
        accum += inc
        img_cropped = img[party_box_y1:party_box_y2, party_box_x1 + accum:party_box_x2 + accum]
        gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
        print(f'{slot_count} : {gray[0][0]}')
        if first_cooldown_fade[slot_count-1] == gray[0][0]:
            pass
        else:
            non_cooldown.append(slot_count)
        slot_count +=1
    # print(f'skill time check {time.time()-temp_time}')
    return non_cooldown