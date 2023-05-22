"""
    PyFT Engine 1
    Copyright (C) 2023  DonTSmi1e

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    DESCRIPTION: A helper rendering script. Stores game objects that will later be used in the game.
"""

import random
import pygame

import common as c

pygame.mixer.init()
pygame.font.init()
font = pygame.font.Font(None, 25)

sprites = {"background": [pygame.image.load("assets/sprites/background-day.png"),
                          pygame.image.load("assets/sprites/background-night.png")],
           "ground": pygame.image.load("assets/sprites/base.png"),
           "pipe": [pygame.image.load("assets/sprites/pipe-green.png"),
                    pygame.image.load("assets/sprites/pipe-red.png")],
           "player": [[pygame.image.load("assets/sprites/yellowbird-upflap.png"),
                       pygame.image.load("assets/sprites/yellowbird-downflap.png")],
                      [pygame.image.load("assets/sprites/redbird-upflap.png"),
                       pygame.image.load("assets/sprites/redbird-downflap.png")],
                      [pygame.image.load("assets/sprites/bluebird-upflap.png"),
                       pygame.image.load("assets/sprites/bluebird-downflap.png")],],
           "ui": [pygame.image.load("assets/sprites/message.png"),
                  pygame.image.load("assets/sprites/gameover.png"),
                  pygame.image.load("assets/sprites/victory.png"),
                  pygame.image.load("assets/sprites/icon.ico")],
           "hud": [pygame.image.load("assets/sprites/0.png"),
                   pygame.image.load("assets/sprites/1.png"),
                   pygame.image.load("assets/sprites/2.png"),
                   pygame.image.load("assets/sprites/3.png"),
                   pygame.image.load("assets/sprites/4.png"),
                   pygame.image.load("assets/sprites/5.png"),
                   pygame.image.load("assets/sprites/6.png"),
                   pygame.image.load("assets/sprites/7.png"),
                   pygame.image.load("assets/sprites/8.png"),
                   pygame.image.load("assets/sprites/9.png")]
          }

sounds = [pygame.mixer.Sound("assets/audio/die.wav"),    # 0
          pygame.mixer.Sound("assets/audio/hit.wav"),    # 1
          pygame.mixer.Sound("assets/audio/point.wav"),  # 2
          pygame.mixer.Sound("assets/audio/swoosh.wav"), # 3
          pygame.mixer.Sound("assets/audio/wing.wav")]   # 4

c.ypos = {}

class Player(pygame.sprite.Sprite):
    dead = False
    jump_height = 0
    angle = 0.1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skin = random.randint(0, 2)

        self.image = sprites["player"][self.skin][1]
        self.rect = self.image.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))

        self.rect.x += (c.g_width/2)-24
        self.rect.y = (c.g_height/2)
    
    def jump(self):
        if not self.dead:
            self.jump_height = 0
            pygame.mixer.Sound.play(sounds[4])
            self.jump_height += 18
    
    def animation(self):
        if self.angle > 0:
            self.image = sprites["player"][self.skin][1]
        elif self.angle < 0:
            self.image = sprites["player"][self.skin][0]

    def update(self):
        if self.rect.y > c.g_height:
            c.gamestate = "GAMEOVER"

        self.animation()
        self.image = pygame.transform.rotate(self.image, self.angle)

        if not self.dead:
            if self.rect.y < 0 or self.rect.y > c.g_height-34-112 or pygame.sprite.spritecollideany(self, c.r_objgroups["enemy"]) and not c.p_noclip:
                pygame.mixer.Sound.play(sounds[1])
                self.dead = True
                self.jump_height = 0
                pygame.mixer.Sound.play(sounds[0])

            if self.jump_height > 0:
                self.jump_height -= c.lvl_velocity
                self.rect.y -= self.jump_height
                self.angle += self.jump_height

            if self.angle < c.p_angle_min_ph2:
                self.angle = c.p_angle_min_ph2
            elif self.angle < c.p_angle_min_ph1:
                self.angle -= 0.5
            else:
                self.angle -= 2.5
            if self.angle > c.p_angle_max:
                self.angle = c.p_angle_max

            self.rect.y += c.lvl_velocity+1
        else:
            self.angle += c.lvl_speed
            self.jump_height += 0.25
            if self.jump_height > 10:
                self.jump_height = 10
            self.rect.y += self.jump_height

class Pipe(pygame.sprite.Sprite):
    flipped = False
    pipe_skin = 0

    def __init__(self, flipped, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.flipped = flipped

        try:
            c.lvl_ypos[self.pos]
        except KeyError:
            c.lvl_ypos[self.pos] = 0
        
        self.image = sprites["pipe"][self.pipe_skin]
        self.rect = self.image.get_rect()
        self.rect.x = c.g_width + 52 * self.pos

        if self.flipped:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.y = -170 + c.lvl_ypos[self.pos]
        else:
            self.image = pygame.transform.rotate(self.image, 0)
            self.rect.y = 270 + c.lvl_ypos[self.pos]

    def update(self):
        self.rect.x -= c.lvl_speed

        if self.rect.x < -52:
            if c.gamestate == "INGAME" and not self.flipped:
                c.lvl_ypos[self.pos] = random.randint(-100, 100)
                c.lvl_score += 1
                pygame.mixer.Sound.play(sounds[2])

                #if c.lvl_score in [5, 10, 15]:
                #    c.lvl_ppos += 3
                #    c.r_objgroups["enemy"].add(Pipe(False, 1 + c.lvl_ppos))
                #    c.r_objgroups["enemy"].add(Pipe(True, 1 + c.lvl_ppos))

            if c.gamestate == "INGAME":
                self.pipe_skin = 1 if c.lvl_score >= 1000 else 0
                self.__init__(self.flipped, 1)

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = sprites["ground"]
        self.rect = self.image.get_rect()
        self.rect.x += 336*self.pos
        self.rect.y = c.g_height-112

    def update(self):
        self.rect.x -= c.lvl_speed
        if self.rect.x < -336:
            self.rect.x = 335
