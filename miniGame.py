import pygame
import main
import random
import math
WIGHT, HEIGHT = 1920, 1080
Score = 0
class BowPlayer(pygame.sprite.Sprite):
    def __init__(self, num_arrows):
        super().__init__()
        self.num_arrows = num_arrows
        self.rect = pygame.Rect((940, 1020), (60, 60))
        self.image = pygame.Surface(self.rect.size)
        self.speed_l = 0
        self.speed_r = 0
    def update(self):
        if self.rect.x + self.speed_r != 0 and self.rect.x + self.speed_l != WIGHT - self.rect.height:
            self.rect.x += self.speed_l
            self.rect.x += self.speed_r
    def move(self, direction):
        if direction == 0:
            self.speed_l = 5
        elif direction == 1:
            self.speed_r = -5
        elif direction == 2:
            self.speed_l = 0
        elif direction == 3:
            self.speed_r = 0
class Purpose(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.rect = pygame.Rect((random.randint(0, WIGHT - 180 - 1), y), (random.choice([60, 120 , 180]), 60))
        self.image = pygame.Surface(self.rect.size)
        self.speed = random.randint(3, 7)
    def update(self):
        if self.rect.x + self.rect.width + self.speed >= WIGHT or self.rect.x <= 0:
            self.speed = -self.speed
        self.rect.x += self.speed


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, purpose, scene, cord):

        super().__init__()
        self.scene = scene
        self.click = cord
        self.purpose_sprites = purpose
        self.rect = pygame.Rect((x, y), (20, 50))
        self.image = pygame.image.load('arrow.png')
        self.l = ((cord[0] - x)**2 + (cord[1] - y)**2)**0.5
        self.sin = (cord[0] - x) / self.l
        self.cos = (cord[1] - y) / self.l
        print(self.sin)
        self.speed_y = 7 * self.cos
        self.speed_x = 7 * self.sin
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if pygame.sprite.spritecollide(self, self.purpose_sprites, True):
            self.kill()



class MiniGameScene(main.Scene):
    def __init__(self, screen):
        self.score = 0
        self.screen = screen
        self.arrow_sprites = pygame.sprite.Group()
        self.purpose_sprites = pygame.sprite.Group()
        self.b_player = BowPlayer(2222)
        num = 60
        self.ttv = 0
        self.ttv_state = False
        for i in range(5):
            self.purpose_sprites.add(Purpose(num))
            num += 125
    def update(self, time_delta):
        self.purpose_sprites.update()
        self.b_player.update()
        self.arrow_sprites.update()
        if self.ttv_state:
            self.ttv+=1
    def draw(self):
        self.screen.fill((9, 33, 123))
        self.purpose_sprites.draw(self.screen)
        self.screen.blit(self.b_player.image, self.b_player.rect)
        self.arrow_sprites.draw(self.screen)
        f1 = pygame.font.Font('assets\\font\\GorgeousPixel.ttf', 46)
        text1 = f1.render(f"ARROWS: {self.b_player.num_arrows}", False,
                          (0, 0, 0))
        text2 = f1.render(f"SCORE: {self.score}", False,
                          (0, 0, 0))

        self.screen.blit(text1, (0, 46))
        self.screen.blit(text2, (0, 94))
        if 0 < self.ttv < 70:
            self.screen.blit(pygame.Surface((30, self.ttv)), (0, 150))
        elif self.ttv >= 70:
            self.screen.blit(pygame.Surface((30, 70)), (0, 150))
    def event_handle(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == 97:
                    self.b_player.move(1)
                elif event.key == 100:
                    self.b_player.move(0)
            elif event.type == pygame.KEYUP:
                if event.key == 100:
                    self.b_player.move(2)
                elif event.key == 97:
                    self.b_player.move(3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.ttv_state = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.ttv_state = False
                    if self.ttv > 50:
                        if self.b_player.num_arrows:
                            self.arrow_sprites.add(
                                Arrow(self.b_player.rect.x, self.b_player.rect.y, self.purpose_sprites,
                                      self, event.pos))
                            self.b_player.num_arrows -= 1
                    self.ttv = 0


class App():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        self.o = MiniGameScene(self.screen)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            self.o.event_handle(pygame.event.get())
            self.o.update(time_delta)
            self.o.draw()
            pygame.display.update()
            pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()