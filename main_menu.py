import db_manager
import pygame
import pygame_gui
import MainMenuWindows
import configparser
import Test_1
import  sounds_game
class MainMenuScene():
    def __init__(self, screen, s):
        self.scene_manager = s
        self.screen = screen
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.manager = pygame_gui.UIManager((1920, 1080))
        self.btn_new_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((120, 180), (480, 120)),
            text="btn_new_game",
            manager=self.manager
        )
        self.btn_saves = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((120, 360), (480, 120)),
            text="btn_saves",
            manager=self.manager
        )
        self.btn_achievement = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((120, 540), (480, 120)),
            text="btn_achievement",
            manager=self.manager
        )
        self.btn_setting = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((120, 720), (480, 120)),
            text="btn_setting",
            manager=self.manager
        )
        self.btn_mute = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((1860, 1020), (60, 60)),
            text="btn_mute",
            manager=self.manager
        )
        self.bg = pygame.image.load('assets\\app_assets\\bg_img.jpg')
        self.mus_slider = None
        self.sound_slider = None
        self.sound_state = True
        self.saves = []
        self.new_game_btn = None
        screen.blit(self.bg, pygame.Rect((0, 0), (1920, 1080)))

    def update(self, time_delta):
        self.manager.update(time_delta)
        self.btn_new_game.set_image(pygame.image.load('assets\\app_assets\\new_game_btn.png'))
        self.btn_saves.set_image(pygame.image.load('assets\\app_assets\\load_btn.png'))
        self.btn_achievement.set_image(pygame.image.load('assets\\app_assets\\achievement_btn.png'))
        self.btn_setting.set_image(pygame.image.load('assets\\app_assets\\setting_btn.png'))
        if self.sound_state:
            self.btn_mute.set_image(pygame.image.load('assets\\app_assets\\sound_on.png'))
        else:
            self.btn_mute.set_image(pygame.image.load('assets\\app_assets\\sound_off.png'))
        self.screen.blit(self.bg, pygame.Rect((0, 0), (1920, 1080)))

    def draw(self):
        self.manager.draw_ui(self.screen)

    def event_handler(self, event):
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.mus_slider:
                pygame.mixer.music.set_volume(event.value / 100)
                self.config["SETTING"]["Music"] = str(event.value)
            elif event.ui_element == self.sound_slider:
                self.config["SETTING"]["Sound"] = str(event.value)
            with open('config.ini', 'w') as configfile:  # save
                self.config.write(configfile)
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in self.saves:
                res = db_manager.DBManager.get_saves(
                    self=db_manager.DBManager("Game1.db"),
                    save_name=event.ui_element.text
                )
                self.scene_manager.change_scene(Test_1.GameScene(level=res[1],
                                                                 scene_manager=self.scene_manager,
                                                                 save_name=event.ui_element.text, name=res[2]))

            elif event.ui_element == self.btn_mute:
                self.sound_state = not self.sound_state
                if not self.sound_state:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.ui_element == self.btn_new_game:
                new_game_wnd = MainMenuWindows.NewGameWindow(self.manager)
                self.name_line = new_game_wnd.name
                self.save_name_line= new_game_wnd.save_name
                self.new_game_btn = new_game_wnd.btn_start

            elif event.ui_element == self.btn_setting:
                setting_wnd = MainMenuWindows.SettingWindow(self.manager)
                self.mus_slider = setting_wnd.mus_slider
                self.sound_slider = setting_wnd.sound_slider
            elif event.ui_element == self.btn_saves:
                wnd_saves = MainMenuWindows.SavesWindow(self.manager)
                self.saves = wnd_saves.saves_btns
            elif event.ui_element == self.btn_achievement:
                MainMenuWindows.AchievementWindow(self.manager)
            elif event.ui_element == self.new_game_btn:
                print(self.save_name_line.text)
                db_manager.DBManager.set_saves(self=db_manager.DBManager("Game1.db"),
                                               location="level_1",
                                               inventory=[],
                                               save_name=self.save_name_line.text,
                                               murders=0,
                                               score=0,
                                               player_name=self.name_line.text)
                db_manager.DBManager.set_records(self=db_manager.DBManager("Game1.db"),
                                                 score=0,
                                                 murders=0,
                                                 n=self.name_line.text)
                self.scene_manager.change_scene(
                    Test_1.GameScene(scene_manager=self.scene_manager, save_name=self.save_name_line.text,
                                     name=self.name_line.text))
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets\\app_assets\\bg_game.mp3')
                pygame.mixer.music.play(-1)
        self.manager.process_events(event)
