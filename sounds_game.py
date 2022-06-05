import pygame
class GameSounds:
    def __init__(self, vol):
        self.hit_sound = pygame.mixer.Sound("assets\\sounds\\hit.wav")
        self.chest_sound = pygame.mixer.Sound("assets\\sounds\\chest.mp3")
        self.save_sound = pygame.mixer.Sound("assets\\sounds\\save.mp3")
        self.finish_sound = pygame.mixer.Sound("assets\\sounds\\finish.mp3")
        self.hit_sound.set_volume(vol)
        self.chest_sound.set_volume(vol)
        self.save_sound.set_volume(vol)
        self.finish_sound.set_volume(vol)
    def set_vol(self, vol):
        self.hit_sound.set_volume(vol)
        self.chest_sound.set_volume(vol)
        self.save_sound.set_volume(vol)
        self.finish_sound.set_volume(vol)