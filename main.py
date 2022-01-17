import pygame
import pygame_gui
import MainMenuWindows

import configparser


class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.now_scene = MainMenuScene(screen)

    def change_scene(self, scene):
        self.now_scene = scene

    def get_scene(self):
        return self.now_scene


class Scene:
    def __init__(self, screen):
        self.screen = screen

    def update(self, time_delta):
        pass

    def draw(self):
        pass

    def event_handle(self, events):
        pass


class MainMenuScene(Scene):
    def __init__(self, screen):
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

    def event_handle(self, events):
        self.manager.process_events(events)
        if events.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if events.ui_element == self.mus_slider:
                pygame.mixer.music.set_volume(events.value /100)
                self.config["SETTING"]["Music"] = str(events.value)
            elif events.ui_element == self.sound_slider:
                self.config["SETTING"]["Sound"] = str(events.value)
            with open('config.ini', 'w') as configfile:  # save
                self.config.write(configfile)
        if events.type == pygame_gui.UI_BUTTON_START_PRESS:
            if events.ui_element == self.btn_mute:
                self.sound_state = not self.sound_state
                if not self.sound_state:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif events.ui_element == self.btn_new_game:
                pass
            elif events.ui_element == self.btn_setting:
                setting_wnd = MainMenuWindows.SettingWindow(self.manager)
                self.mus_slider = setting_wnd.mus_slider
                self.sound_slider = setting_wnd.sound_slider
            elif events.ui_element == self.btn_saves:
                print(33333)
            elif events.ui_element == self.btn_achievement:
                MainMenuWindows.AchievementWindow(self.manager)


class GameScene(Scene):
    def __init__(self, level_map: Map):
        self.map = level_map

    def draw(self):
        pass

    def update(self, time_delta):
        pass

    def event_handle(self, events):
        pass


class FinalScene(Scene):
    pass



class App():
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load("test_m2.wav")
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.scene_mg = SceneManager(self.screen)
        self.clock = pygame.time.Clock()
        self.run_state = True

    def run(self):
        while self.run_state:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_state = False
                self.scene_mg.now_scene.event_handle(event)
            self.scene_mg.now_scene.update(time_delta)
            self.scene_mg.now_scene.draw()
            pygame.display.update()
            pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
