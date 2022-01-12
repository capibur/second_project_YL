import pygame
import pygame_gui

pygame.init()
screen = pygame.display.set_mode((1920, 1080))


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
        self.v = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((0,0), (300,300)),
            manager=self.manager
        )
        self.bg = pygame.image.load('gog.jpg')
        screen.blit(self.bg, pygame.Rect((0, 0), (1920, 1080)))

    def update(self, time_delta):
        self.manager.update(time_delta)
        self.btn_new_game.set_image(pygame.image.load('pixil-frame-0 (1).png'))

    def draw(self):
        self.manager.draw_ui(self.screen)

    def event_handle(self, events):
        self.manager.process_events(events)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_mute:
                pass
            elif event.ui_element == self.btn_new_game:
                pass
            elif event.ui_element == self.btn_setting:
                pass
            elif event.ui_element == self.btn_saves:
                pass
            elif event.ui_element == self.btn_achievement:
                pass

class GameScene(Scene):
    def draw(self):
        test = pygame.image.load('pixil-frame-0 (1).png')
        screen.blit(test, pygame.Rect((0, 0), (444, 444)))

    def update(self, time_delta):
        pass

    def event_handle(self, events):
        pass


class FinalScene(Scene):
    pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10
        self.speed = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        print(22222222)

    def upd(self, events):
        for event in events:
            print(event.type)


scene_mg = SceneManager(screen)
clock = pygame.time.Clock()
run = True

pygame.display.update()

while run:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        scene_mg.now_scene.event_handle(event)
    scene_mg.now_scene.update(time_delta)
    scene_mg.now_scene.draw()
    pygame.display.update()
    pygame.display.flip()
