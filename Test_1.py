import pygame
import sys
import os
import pytmx
from random import random, choice
from time import sleep
import go_snene
import db_manager
import sounds_game
import configparser
DBMANGER = db_manager.DBManager("Game1.db")
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
chests_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
exit_sprites = pygame.sprite.Group()
key_sprites = pygame.sprite.Group()

active_objects = pygame.sprite.Group()

WINDOW_SIZE = 1920, 1080
TILE_SIZE = 60
MURDERS = 0

pygame.init()

SCREEN = pygame.display.set_mode(WINDOW_SIZE)
SCREEN_INTERFACE = pygame.display.set_mode(WINDOW_SIZE)
ENEMIES_ID = {130: 'Goblin',
              274: 'Flying eye',
              224: 'Mushroom',
              29: 'Knight',
              28: 'Skeleton'}
CHEST_ID = 203
EXT_ID = 298
KEY_ID = 572
DOOR_ID = 442
HERO_ID = 466
CROWN_ID = 142

ENEMIES_CHARACTERISTIC = {'Goblin': [30, 10, 1, 0.09, 5],
                          'Flying eye': [10, 2, 1, 0.01, 11],
                          'Mushroom': [40, 5, 0, 0, 7],
                          'Knight': [40, 6, 3, 0.09, 8],
                          'Skeleton': [30, 4, 1, 0.06, 6]}

SIZES_OF_ANIMATIONS = {
    'Hero': {'Idle': (35, 60), 'Run': (49, 60), 'Attack': (146, 64), 'Death': (61, 60), 'Take hit': (50, 60)},
    'Goblin': {'Idle': (37, 60), 'Run': (37, 60), 'Attack': (90, 60), 'Death': (54, 60), 'Take hit': (45, 60)},
    'Skeleton': {'Idle': (50, 60), 'Run': (50, 60), 'Attack': (82, 60), 'Death': (60, 60), 'Take hit': (52, 60)},
    'Flying eye': {'Idle': (55, 60), 'Run': (55, 60), 'Attack': (55, 60), 'Death': (60, 60), 'Take hit': (50, 60)},
    'Mushroom': {'Idle': (55, 60), 'Run': (60, 60), 'Attack': (60, 60), 'Death': (60, 60), 'Take hit': (50, 60)},
    'Knight': {'Idle': (60, 60), 'Run': (60, 60), 'Attack': (90, 60), 'Death': (60, 60), 'Take hit': (60, 60)}}

Object = []


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def cut_sheet(sheet, columns, rows):
    spis = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            spis.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
    return spis


def rewrite_screen():
    SCREEN.fill((0, 0, 0))
    all_sprites.draw(SCREEN)
    pygame.display.flip()


def work_with_photoes(name):
    animations = {'Idle': load_image(f'{name}\Idle.png', -1),
                  'Attack': load_image(f'{name}\Attack.png', -1),
                  'Run': load_image(f'{name}\Run.png', -1),
                  'Take hit': load_image(f'{name}\Take hit.png', -1),
                  'Death': load_image(f'{name}\Death.png', -1)}
    for i in animations:
        try:
            x, y = SIZES_OF_ANIMATIONS[name][i]
            animations[i] = cut_sheet(animations[i], animations[i].get_width() // x, animations[i].get_height() // y)
        except Exception:
            animations[i] = cut_sheet(animations[i], animations[i].get_width() // TILE_SIZE,
                                      animations[i].get_height() // TILE_SIZE)
    return animations
def next_level(level_now, scene_manager, hp, inventory, num, save_name, name):
    all_sprites.empty()
    enemy_sprites.empty()
    chests_sprites.empty()
    door_sprites.empty()
    exit_sprites.empty()
    key_sprites.empty()
    active_objects.empty()
    db_m = db_manager.DBManager("Game1.db")
    d_lvl = {"level_1": "mini_game",
             "level_2": "level_3",
             "level_3": "level_4",
             "level_4": False}
    record = db_m.request(f"""
    SELECT murders, score FROM record_list WHERE name = "{name}" """)[0]

    if d_lvl[level_now] and d_lvl[level_now] != "mini_game":
        db_m.update_records(score=2,
                            murders=record[0] + num,
                            n=name, )

        text = f"""UPDATE save_list 
                    SET location = "{d_lvl[level_now]}"
                    WHERE save_name = "{save_name}" """

        db_m.request(text)
        scene_manager.change_scene(GameScene(level=d_lvl[level_now],
                                             hp=hp,
                                             scene_manager=scene_manager,
                                             save_name=save_name,
                                             name=name))
    elif d_lvl[level_now] == "mini_game":
        scene_manager.set_mini_game(save_name, name)
    else:
        scene_manager.change_scene(go_snene.FinalSene(SCREEN, record[1], record[0],  scene_manager=scene_manager))
def death(scene_mg, save_name):
    all_sprites.empty()
    enemy_sprites.empty()
    chests_sprites.empty()
    door_sprites.empty()
    exit_sprites.empty()
    key_sprites.empty()
    active_objects.empty()
    scene_mg.change_scene(GameScene(scene_manager=scene_mg, save_name=save_name))


class Map:
    def __init__(self, filename, finish_tile, free_tiles=[1, 5, 17, 69]):
        self.map = pytmx.load_pygame(f'Maps/{filename}.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile
        self.level_name = filename

    def create_a_level(self):
        places = {'Hero': None, 'Enemies': [], 'Chests': [], 'Exit': None, 'Key': None, 'Door': [], 'Crown': None}
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                Part_of_land((x, y), image)
                if self.map.get_tile_image(x, y, 1):
                    id = self.get_tile_id((x, y), 1)
                    if id == HERO_ID:
                        places['Hero'] = (x, y)
                    elif id in ENEMIES_ID:
                        places['Enemies'].append((x, y, ENEMIES_ID[id]))
                    elif id == CHEST_ID:
                        places['Chests'].append((x, y))
                    elif id == EXT_ID:
                        places['Exit'] = (x, y)
                    elif id == CROWN_ID:
                        places['Crown'] = (x, y)
                    elif id == KEY_ID:
                        places['Key'] = (x, y)
                    elif id == DOOR_ID:
                        places['Door'].append((x, y))
        return places

    def get_tile_id(self, position, level):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, level)]

    def is_free(self, position):
        try:
            return self.get_tile_id(position, 0) in self.free_tiles
        except ValueError:
            return False


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WINDOW_SIZE[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - WINDOW_SIZE[1] // 2)


class Part_of_land(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(TILE_SIZE * position[0], TILE_SIZE * position[1])


class Hero(pygame.sprite.Sprite):
    def __init__(self, position, hp=100, dm=10, df=1, mp=100, ev=0.08, inventory=None, location="level_1",
                 scene_manager=None, save_name="", hp_bar=None):
        self.animations = work_with_photoes('Hero')
        self.location = location
        self.save_name = save_name
        self.hp_bar = hp_bar
        self.scene_manager = scene_manager
        super().__init__(all_sprites)
        self.x, self.y = 0, 1
        self.hp, self.dm, self.df, self.mp, self.ev = hp, dm, df, mp, ev
        self.inventory = inventory
        self.key = False

        self.cur_frame = 0
        self.image = self.animations['Idle'][self.cur_frame]
        self.rect = self.animations['Idle'][0].get_rect()
        self.rect = self.rect.move(TILE_SIZE * self.x, TILE_SIZE * self.y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.animations['Idle'])
        self.image = self.animations['Idle'][self.cur_frame]

    def get_key(self):
        self.key = True

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        move_x, move_y = position[0] - self.x, position[1] - self.y
        reversal = (position[0] - self.x) < 0 or (position[1] - self.y) < 0
        self.rect = self.rect.move(60 * move_x, 60 * move_y)
        connecting = pygame.sprite.spritecollide(self, active_objects, False)
        if not connecting:
            self.rect = self.rect.move(60 * (- move_x), 60 * (- move_y))
            cur_frame = 0
            for _ in range(20):
                cur_frame = (cur_frame + 1) % len(self.animations['Run'])
                self.image = self.animations['Run'][cur_frame]
                self.image = pygame.transform.flip(self.image, flip_x=reversal, flip_y=False)
                self.rect = self.rect.move(3 * move_x, 3 * move_y)
                sleep(1 / 60)
                rewrite_screen()
            self.x, self.y = position
            self.image = self.animations['Idle'][self.cur_frame]
            return None
        else:
            self.rect = self.rect.move(60 * (- move_x), 60 * (- move_y))
            return connecting[0]

    def attack(self, attack_to):
        reversal = (attack_to[0] - self.x) < 0 or (attack_to[1] - self.y) < 0
        if reversal:
            size_x = SIZES_OF_ANIMATIONS['Hero']['Attack'][0]
            if size_x > TILE_SIZE:
                self.rect = self.rect.move(TILE_SIZE - size_x, 0)
        for i in range(len(self.animations['Attack'])):
            self.image = self.animations['Attack'][i]
            self.image = pygame.transform.flip(self.image, flip_x=reversal, flip_y=False)
            rewrite_screen()
            sleep(1 / 20)
        if reversal and size_x > TILE_SIZE:
            self.rect = self.rect.move(size_x - TILE_SIZE, 0)
        self.image = self.animations['Idle'][self.cur_frame]

    def take_gamage(self, damage):
        if random() > self.ev:
            self.hp -= damage - self.df
            self.hp_bar.set_hp(self.hp)
            if self.hp <= 0:
                for i in range(len(self.animations['Death'])):
                    self.image = self.animations['Death'][i]
                    rewrite_screen()
                    sleep(1 / 20)
                death(self.scene_manager, self.save_name)
            else:
                for i in range(len(self.animations['Take hit'])):
                    self.image = self.animations['Take hit'][i]
                    rewrite_screen()
                    sleep(1 / 20)

    def get_an_item(self):
        self.inventory.update("sword")
        DBMANGER.append_thing("sword", self.save_name)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, position, scene):
        self.name = name
        self.scene = scene
        self.animations = work_with_photoes(name)
        super().__init__(all_sprites, enemy_sprites, active_objects)
        self.x, self.y = position
        self.hp, self.dm, self.df, self.ev, self.attack_range = ENEMIES_CHARACTERISTIC[name]

        self.cur_frame = 0
        self.image = self.animations['Idle'][self.cur_frame]
        self.rect = self.animations['Idle'][0].get_rect()
        self.rect = self.rect.move(TILE_SIZE * self.x, TILE_SIZE * self.y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.animations['Idle'])
        self.image = self.animations['Idle'][self.cur_frame]

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        move_x, move_y = position[0] - self.x, position[1] - self.y
        reversal = (position[0] - self.x) < 0 or (position[1] - self.y) < 0
        self.rect = self.rect.move(60 * move_x, 60 * move_y)
        connecting = pygame.sprite.spritecollide(self, active_objects, False)
        if len(connecting) > 1:
            self.rect = self.rect.move(60 * (- move_x), 60 * (- move_y))
        else:
            self.rect = self.rect.move(60 * (- move_x), 60 * (- move_y))
            cur_frame = 0
            for _ in range(20):
                cur_frame = (cur_frame + 1) % len(self.animations['Run'])
                self.image = self.animations['Run'][cur_frame]
                self.image = pygame.transform.flip(self.image, flip_x=reversal, flip_y=False)
                self.rect = self.rect.move(3 * move_x, 3 * move_y)
                sleep(1 / 50)
                rewrite_screen()
            self.x, self.y = position
        self.image = self.animations['Idle'][self.cur_frame]

    def attack(self, attack_to):
        reversal = (attack_to[0] - self.x) < 0 or (attack_to[1] - self.y) < 0
        if reversal:
            size_x = SIZES_OF_ANIMATIONS[self.name]['Attack'][0]
            if size_x > TILE_SIZE:
                self.rect = self.rect.move(TILE_SIZE - size_x, 0)
        for i in range(len(self.animations['Attack'])):
            self.image = self.animations['Attack'][i]
            self.image = pygame.transform.flip(self.image, flip_x=reversal, flip_y=False)
            rewrite_screen()
            sleep(1 / 20)
        if reversal and size_x > TILE_SIZE:
            self.rect = self.rect.move(size_x - TILE_SIZE, 0)
        self.image = self.animations['Idle'][self.cur_frame]

    def take_gamage(self, damage):
        self.scene.sounds.hit_sound.play()
        if random() > self.ev:
            self.hp -= damage - self.df
            if self.hp <= 0:
                for i in range(len(self.animations['Death'])):
                    self.image = self.animations['Death'][i]
                    rewrite_screen()
                    sleep(1 / 20)
                self.kill()
                self.scene.murders += 1
                return True
            else:
                for i in range(len(self.animations['Take hit'])):
                    self.image = self.animations['Take hit'][i]
                    rewrite_screen()
                    sleep(1 / 20)
        return False


class Chest(pygame.sprite.Sprite):
    def __init__(self, position):
        self.image = load_image('chest closed.png', -1)
        super().__init__(all_sprites, chests_sprites, active_objects)
        self.x, self.y = position
        self.rect = self.image.get_rect().move(60 * self.x, 60 * self.y)
        self.close = True

    def get_position(self):
        return self.x, self.y

    def try_to_open(self):
        if self.close:
            self.close = not self.close
            self.image = load_image('chest open.png', -1)
            return True
        return False


class Exit(pygame.sprite.Sprite):
    def __init__(self, position, name):
        self.image = load_image(name + '.png', -1)
        super().__init__(all_sprites, active_objects, exit_sprites)
        self.x, self.y = position
        self.rect = self.image.get_rect().move(60 * self.x, 60 * self.y)

    def get_position(self):
        return self.x, self.y


class Key(pygame.sprite.Sprite):
    def __init__(self, position):
        self.image = load_image('key.png', -1)
        super().__init__(all_sprites, active_objects, key_sprites)
        print(position)
        self.x, self.y = position
        self.rect = self.image.get_rect().move(60 * self.x, 60 * self.y)

    def get_position(self):
        return self.x, self.y


class Door(pygame.sprite.Sprite):
    def __init__(self, position):
        self.image = load_image('door.png')
        super().__init__(all_sprites, door_sprites, active_objects)
        self.x, self.y = position
        self.rect = self.image.get_rect().move(60 * self.x, 60 * self.y)

    def get_position(self):
        return self.x, self.y


def path(end, map, now_level, previous_level):
    next_level = set()
    for x, y in now_level:
        for x_b, y_b in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if map.is_free((x + x_b, y + y_b)):
                if not (x + x_b, y + y_b) in previous_level:
                    if end == (x + x_b, y + y_b):
                        return x, y
                    next_level.add((x + x_b, y + y_b))
    step = path(end, map, next_level, now_level)
    if previous_level:
        for x_b, y_b in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (step[0] + x_b, step[1] + y_b) in now_level:
                return step[0] + x_b, step[1] + y_b
    else:

        return step

class Game:
    def __init__(self, map, hero, enemies, chests, out, key, door, save_name, name, scene):
        self.map, self.hero, self.enemies, self.chests, self.out, self.key, self.door = map, hero, enemies, chests, out, key, door
        self.save_name = save_name
        self.name = name
        self.scene = scene
    def update_hero(self, next_x, next_y):
        was_x, was_y = self.hero.get_position()
        if self.map.is_free((was_x + next_x, was_y + next_y)):
            connect_object = self.hero.set_position((was_x + next_x, was_y + next_y))
            if connect_object:
                if connect_object in chests_sprites:
                    if connect_object.try_to_open():
                        self.scene.sounds.chest_sound.play()
                        self.hero.get_an_item()
                elif connect_object in enemy_sprites:
                    self.hero.attack(connect_object.get_position())
                    if connect_object.take_gamage(
                            self.hero.dm + DBMANGER.get_spec(self.hero.inventory.get_select())["dmg"]):
                        self.enemies.remove(connect_object)
                elif connect_object in key_sprites:
                    connect_object.kill()
                    self.hero.get_key()
                elif connect_object in door_sprites:
                    if self.hero.key:
                        connect_object.kill()
                elif connect_object in exit_sprites:
                    self.scene.sounds.save_sound.play()
                    next_level(level_now=self.map.level_name,
                               scene_manager=self.hero.scene_manager,
                               hp=self.hero.hp,
                               inventory=self.hero.inventory,
                               save_name=self.save_name,
                               name=self.name,
                               num = self.scene.murders)
                    # конец уровня
            end_x, end_y = self.hero.get_position()
            for enemy in self.enemies:
                start_x, start_y = enemy.get_position()
                hero_x, hero_y = self.hero.get_position()
                if abs(hero_x - start_x) <= WINDOW_SIZE[0] // TILE_SIZE // 2 and abs(hero_y - start_y) <= WINDOW_SIZE[
                    1] // TILE_SIZE // 2:
                    if (start_x - end_x) ** 2 + (start_y - end_y) ** 2 <= enemy.attack_range ** 2:
                        new_x, new_y = path((end_x, end_y), self.map, {(start_x, start_y)}, [])
                        if new_x != start_x or new_y != start_y:
                            enemy.set_position((new_x, new_y))
                        else:
                            enemy.attack(self.hero.get_position())
                            self.hero.take_gamage(enemy.dm)
                    else:
                        next_x, next_y = choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
                        if self.map.is_free((start_x + next_x, start_y + next_y)):
                            enemy.set_position((start_x + next_x, start_y + next_y))








class HPBar:
    def __init__(self, hp):
        self.hp_now = hp
    def set_hp(self, hp):
        self.hp_now = hp
    def draw(self):
        hp_slots = self.hp_now // 10
        y = 1050
        for i in range(hp_slots):
            pygame.draw.rect(SCREEN_INTERFACE, (255,0,20), (0, y, 60, 30))
            y -= 35






class Inventory:
    def __init__(self, inv_content: list):
        self.selected_th = 0
        self.inv_content = inv_content
        self.inv_slots = {
            "0": "",
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": "",}
        for i, j in enumerate(self.inv_content):
            self.inv_slots[str(i)] = j
    def draw(self):
        x = 1800
        for i in range(6):
            if i == self.selected_th:
                pygame.draw.rect(SCREEN_INTERFACE,(45,12,0), (x, 960, 120, 120), 5 )
            else:
                pygame.draw.rect(SCREEN_INTERFACE, (45, 12, 233), (x, 960, 120, 120), 5)
            if self.inv_slots[str(i)]:

                img = db_manager.DBManager.get_img(db_manager.DBManager("Game1.db"), self.inv_slots[str(i)])

                SCREEN_INTERFACE.blit(pygame.image.load(img), pygame.Rect((x, 960), (120, 120)))
            x -= 120
    def get_select(self):
        return self.inv_slots[str(self.selected_th)]
    def set_select(self, num):
        self.selected_th = num
    def update(self, thing):
        self.inv_content.append(thing)
        for i, j in enumerate(self.inv_content):
            self.inv_slots[str(i)] = j
    def delete_thing(self):
        self.inv_slots[str(self.selected_th)] = ""
        self.inv_content.clear()
        for i in self.inv_slots.values():
            if i != "":
                self.inv_content.append(i)


        for i, j in enumerate(self.inv_content):
            self.inv_slots[str(i)] = j





class GameScene:
    def __init__(self, level="level_1", hp=100, scene_manager=None, save_name="", name=""):
        self.map = Map(level, 90)
        self.murders = 0
        self.inventory = Inventory(DBMANGER.get_saves(save_name)[0])

        self.hp_bar = HPBar(hp)
        self.scene_manager = scene_manager
        self.places = self.map.create_a_level()
        self.hero = Hero(self.places['Hero'], hp=hp, inventory=self.inventory, scene_manager=scene_manager,
                         save_name=save_name, hp_bar=self.hp_bar)
        self.enemies = [Enemy(i[2], (i[0], i[1]), self) for i in self.places['Enemies']]
        self.chests = [Chest((i[0], i[1])) for i in self.places['Chests']]
        if self.places['Crown']:
            self.out = Exit(self.places['Crown'], 'crown')
        else:
            self.out = Exit(self.places['Exit'], 'exit')
        self.key = Key(self.places['Key'])
        self.door = [Door((i[0], i[1])) for i in self.places['Door']]

        self.camera = Camera()
        self.clock = pygame.time.Clock()
        self.game = Game(self.map, self.hero, self.enemies, self.chests, self.out, self.key, self.door, save_name, name, self)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.sounds = sounds_game.GameSounds(float(self.config["SETTING"]["Sound"]))
    def update(self, time_delta):
        self.camera.update(self.hero)
        for sprite in all_sprites:
            self.camera.apply(sprite)
        all_sprites.update()
        self.clock.tick(10)
        pass

    def draw(self):
        rewrite_screen()
        self.hp_bar.draw()
        self.inventory.draw()

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.game.update_hero(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.game.update_hero(1, 0)
            elif event.key == pygame.K_UP:
                self.game.update_hero(0, -1)
            elif event.key == pygame.K_DOWN:
                self.game.update_hero(0, 1)
            elif 49 <= event.key <= 54:
                self.inventory.set_select(event.key - 49)
            elif event.key == 55:
                self.inventory.delete_thing()

