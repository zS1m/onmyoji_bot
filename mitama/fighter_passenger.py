from gameLib.fighter import Fighter
from tools.game_pos import TansuoPos
import tools.utilities as ut

import logging
import time


class FighterPassenger(Fighter):
    '''御魂战斗乘客程序，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Passenger: ', emyc, hwnd)

    def start(self):
        '''单人御魂乘客'''
        # 设定点击疲劳度
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # 战斗主循环
        while self.run:
            # 检测是否进入战斗
            self.check_battle()

            # 在战斗中，标记己方式神
            self.mitama_team_click()

            # 已经进入战斗，乘客自动点怪
            self.click_monster()

            # 检测是否打完
            state = self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.get_reward(mood3, state)

            # 等待下一轮
            logging.info('Passenger: 等待下一轮')
            start_time = time.time()
            while time.time() - start_time <= 5 and self.run:
                # 检测是否回到队伍中
                if(self.yys.wait_game_img('img\\XIE-ZHAN-DUI-WU.png', 1, False)):
                    self.log.writeinfo('Passenger: 进入队伍')
                    break

                # 检测是否有御魂邀请
                yuhun_loc = self.yys.wait_game_img(
                    'img\\YU-HUN.png', 1, False)
                if yuhun_loc:
                    # 点击自动接受邀请
                    if self.yys.find_game_img('img\\ZI-DONG-JIE-SHOU.png'):
                        self.yys.mouse_click_bg((210, yuhun_loc[1]))
                        self.log.writeinfo('Passenger: 自动接受邀请')

                    # 点击普通接受邀请
                    elif self.yys.find_game_img('img\\JIE-SHOU.png'):
                        self.yys.mouse_click_bg((125, yuhun_loc[1]))
                        self.log.writeinfo('Passenger: 接受邀请')
            
            # 检查游戏次数
            self.check_times()
