import pygame
import pygame_gui
from db_manager import DBManager
import configparser
class NewGameWindow:
    def __init__(self, manager):
        self.manager = manager
        self.size = (480, 300)
        self.window = pygame_gui.elements.UIWindow(
            manager=self.manager,
            rect=pygame.Rect((420, 180), self.size))
        self.window.set_blocking(True)
        s = pygame.Surface((480,850))
        s.fill((150,75,0))

        pygame_gui.elements.UILabel(
            manager=self.manager,
            container=self.window,
            relative_rect=pygame.Rect((165, 0), (120, 80)),
            text="Your Name"
        )
        self.name  = pygame_gui.elements.UITextEntryLine(
            manager=self.manager,
            relative_rect= pygame.Rect((115, 66),(210,40)),
            container=self.window
        )
        pygame_gui.elements.UILabel(
            manager=self.manager,
            container=self.window,
            relative_rect=pygame.Rect((165, 115), (120, 15)),
            text="Save"
        )
        self.save_name = self.text_l = pygame_gui.elements.UITextEntryLine(
            manager=self.manager,
            relative_rect= pygame.Rect((115, 140),(210,40)),
            container=self.window
        )
        self.btn_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((125, 190), (190, 50)),
            text="start",
            manager=self.manager,
            container=self.window
        )
class AchievementWindow:
    def __init__(self, manager):
        self.manager = manager
        self.size = (480, 850)
        self.window = pygame_gui.elements.UIWindow(
            manager=self.manager,
            rect=pygame.Rect((420, 180), self.size))
        self.window.set_blocking(True)
        s = pygame.Surface((480,850))
        s.fill((150,75,0))
        self.window.image = s
        a = DBManager.request(DBManager("Game1.db"),
                              """SELECT * FROM achievement_list"""
                              )
        print(a)
        self.load_ach(a)

    def load_ach(self, a):
        hight = 0
        for i in a:
            pygame_gui.elements.UIImage(
                manager=self.manager,
                relative_rect=pygame.Rect((0, hight), (100, 100)),
                image_surface=pygame.image.load(i[4]),
                container=self.window
            )
            pygame_gui.elements.UILabel(
                manager=self.manager,
                relative_rect=pygame.Rect((100, hight), (150, 100)),
                container=self.window,
                text=i[1]
            )
            pygame_gui.elements.UILabel(
                manager=self.manager,
                relative_rect=pygame.Rect((250, hight), (100, 100)),
                container=self.window,
                text="Получена" if i[2] else "Не получена"
            )

            self.inf = pygame_gui.elements.UIButton(
                manager=self.manager,
                relative_rect=pygame.Rect((350, hight), (100, 100)),
                container=self.window,
                text="info",
                tool_tip_text=i[3])
            hight += 100

class SettingWindow:
    def __init__(self, manager):
        self.manager = manager
        self.size = (720, 720)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.pops = pygame.sprite.Group()
        self.window = pygame_gui.elements.UIWindow(
            manager=self.manager,
            rect=pygame.Rect((420, 180), self.size))
        bg = pygame.Surface((720,720))
        bg.fill((150,75,0))
        self.window.image = bg
        self.window.set_blocking(True)
        self.mus_lable = pygame_gui.elements.UIImage(
            manager=self.manager,
            image_surface=pygame.image.load('assets\\app_assets\\mus.png'),
            relative_rect=pygame.Rect((45, 45),(225, 45)),
            container=self.window,

        )
        self.sound_lable = pygame_gui.elements.UIImage(
            manager=self.manager,
            image_surface=pygame.image.load('assets\\app_assets\\sound.png'),
            relative_rect=pygame.Rect((45, 270),(225, 45)),
            container=self.window,

        )
        self.mus_slider = pygame_gui.elements.UIHorizontalSlider(
            manager=self.manager,
            relative_rect=pygame.Rect((45,135),(450, 45)),
            container=self.window,
            start_value=int(self.config["SETTING"]["Music"]),
            value_range=(0, 100)
        )
        self.sound_slider = pygame_gui.elements.UIHorizontalSlider(
            manager=self.manager,
            relative_rect=pygame.Rect((45, 360), (450, 45)),
            container=self.window,
            start_value=int(self.config["SETTING"]["Sound"]),
            value_range=(0, 100)
        )


class SavesWindow:
    def __init__(self, manager):
        self.manager = manager
        self.size = (380, 850)
        self.window = pygame_gui.elements.UIWindow(
            manager=self.manager,
            rect=pygame.Rect((430, 180), self.size))
        self.window.set_blocking(True)
        s = pygame.Surface((380,850))
        s.fill((150,75,0))
        self.window.image = s

        pygame_gui.elements.UITextBox
        a = DBManager.request(DBManager("Game1.db"),
                              """SELECT * FROM save_list"""
                              )
        self.saves_btns = []
        self.load_svs(a)
    def load_svs(self, a):
        hight = 0
        for i in a:
            pygame_gui.elements.UILabel(
                manager=self.manager,
                relative_rect=pygame.Rect((0, hight), (150, 100)),
                container=self.window,
                text=str(i[3])
            )
            pygame_gui.elements.UILabel(
                manager=self.manager,
                relative_rect=pygame.Rect((150, hight), (100, 100)),
                container=self.window,
                text=str(i[1])
            )

            save_btn = pygame_gui.elements.UIButton(
                manager=self.manager,
                relative_rect=pygame.Rect((250, hight), (100, 100)),
                container=self.window,
                text=str(i[3]),)
            self.saves_btns.append(save_btn)
            hight += 100
