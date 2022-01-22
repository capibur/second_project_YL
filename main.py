import pygame
import main_menu
import miniGame
import configparser
pygame.init()


class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.now_scene = main_menu.MainMenuScene(screen, self)
        self.main_scene = main_menu.MainMenuScene(screen, self)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        pygame.mixer.music.load("assets\\app_assets\\bg_menu.mp3")
        pygame.mixer.music.play(-1)
    def change_scene(self, scene):
        self.now_scene = None
        self.now_scene = scene

    def set_main_scene(self):
        self.now_scene = self.main_scene
        pygame.mixer.music.set_volume(float(self.config["SETTING"]["Music"]))
    def set_mini_game(self, save_name, name):
        self.now_scene = miniGame.MiniGameScene(self.screen, save_name, name, self)


    def get_scene(self):
        return self.now_scene




class App():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        pygame.mixer.music.load("assets\\app_assets\\bg_menu.mp3")
        pygame.mixer.music.set_volume(float(self.config["SETTING"]["Music"]))
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
                self.scene_mg.now_scene.event_handler(event)
            self.scene_mg.now_scene.update(time_delta)
            self.scene_mg.now_scene.draw()
            pygame.display.update()
            pygame.display.flip()


app = App()
app.run()
