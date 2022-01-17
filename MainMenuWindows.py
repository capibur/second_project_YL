import pygame
import pygame_gui
from db_manager import DBManager
import configparser

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

        pygame_gui.elements.UITextBox
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
                text="test",
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
        s = pygame.Surface((720,720))
        s.fill((150,75,0))
        self.window.image = s
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


