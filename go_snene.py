import pygame
import db_manager
import configparser
import sounds_game
class FinalSene:
    def __init__(self, screen, score, murders, coins, scene_manager):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        pygame.mixer.music.load("assets\\app_assets\\bg_menu.mp3")
        sounds = sounds_game.GameSounds(float(self.config["SETTING"]["sound"]))
        sounds.finish_sound.play()
        self.murders = murders
        self.score = score
        self.screen = screen
        self.achievements = 0
        self.scene_manager = scene_manager
        self.my_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.my_event, 1400, 10)
        self.a = 0
        self.db_mng = db_manager.DBManager("Game1.db")
        self.f1 = pygame.font.Font('assets\\font\\GorgeousPixel.ttf', 90)
        self.f2 = pygame.font.Font('assets\\font\\GorgeousPixel.ttf', 70)
        self.f3 = pygame.font.Font('assets\\font\\GorgeousPixel.ttf', 50)

    def achivment(self):
        if self.murders == 0 and not self.db_mng.request(
                """SELECT achieved FROM achievement_list WHERE name = "Гетте во плоти" """)[0][0]:
            self.db_mng.complete('Гетте во плоти')
            self.achievements += 1
        if self.murders >= 20 and not self.db_mng.request(
                """SELECT achieved FROM achievement_list WHERE name = "Кто украл мою собаку?" """)[0][0]:
            self.db_mng.complete("Кто украл мою собаку?")
            self.achievements += 1
        if self.score >= 300 and not self.db_mng.request(
                """SELECT achieved FROM achievement_list WHERE name = "Странные склонности" """)[0][0]:
            self.db_mng.complete("Странные склонности")
            self.achievements += 1

    def update(self, time_delta):
        pass

    def event_handler(self, events):
        if events.type == pygame.KEYDOWN:
            if events.key == 27:
                pygame.time.set_timer(self.my_event, 0)
                self.scene_manager.set_main_scene()
        if events.type == self.my_event:
            if self.a == 0:
                self.screen.blit(self.f3.render("mгurders -", False,
                                                (234, 0, 0)), (420, 400))
                self.screen.blit(self.f3.render(str(self.murders), False,
                                                (234, 0, 0)), (760, 400))
                self.a += 1
            elif self.a == 1:
                self.screen.blit(self.f3.render("achievements -", False,
                                                (255, 215, 0)), (420, 500))
                self.screen.blit(self.f3.render(str(self.achievements), False,
                                                (255, 215, 0)), (760, 500))
                self.a += 1
            elif self.a == 2:
                self.screen.blit(self.f3.render("time -", False,
                                                (50, 100, 100)), (420, 600))
                self.screen.blit(self.f3.render(str(self.murders), False,
                                                (50, 100, 100)), (760, 600))
                self.a += 1
            elif self.a == 3:
                self.screen.blit(self.f2.render("All Score -", False,
                                                (18, 10, 143)), (930, 730))
                self.a += 1
            elif self.a == 9:
                self.screen.blit(self.f3.render("Press esc", False,
                                                (25, 25, 25)), (770, 1000))
            elif self.a < 9:
                self.a += 1

    def draw(self):
        self.screen.blit(self.f1.render("WIN!", False,
                                        (234, 235, 32)), (850, 100))
        self.screen.blit(self.f2.render("Results:", False,
                                        (234, 235, 32)), (360, 240))
        pygame.draw.line(self.screen,
                         start_pos=[360, 220],
                         end_pos=[1560, 220],
                         color=(225,44,0),
                         width=10)
        pygame.draw.line(self.screen,
                         start_pos=[360, 840],
                         end_pos=[1560, 840],
                         color=(225,44,0),
                         width=10)

