import sys
sys.path.insert(0, '/storage/home/django_learn/pygame/src')

import os
import math
from random import random, randint
import imgaud
import core
import time
import pygame
from pygame.locals import *

class SpaceAdvCore(object):
    def __init__(self, *args, **kwargs):
        self._getData()

    def _getData(self):
        self.width, self.height = 1000, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.keys = {
            'up': False,
            'left':False,
            'down': False,
            'right': False,
            'reset': False
        }
        self.playerpos = [100,100]
        self.speed = [0,0]
        self.acc = [0,0]
        self.arrows = []

        self.time = 0
        self.old_time = int(time.time())
        self.time_left = 90000

        self.badtimer = 100
        self.badtimer1 = 0
        self.deads = []
        self.badguys = [{
            'pos': [0,100],
            'img': imgaud.badguyimg1[randint(0,3)]
        }]
        self.healthvalue = 194
        self.font = pygame.font.Font(None, 24)

        # 4 - keep looping through
        self.running = 1
        self.exitcode = 0

    def reset(self):
        self._getData();
        self.main();

    def get_move_pos(self, position, angle, rotate):
        moveX = self.playerpos[0] - rotate.get_rect().width / 2
        moveY = self.playerpos[1] - rotate.get_rect().height / 2
        return (round(moveX, 2), round(moveY, 2))

    def draw_arrows(self):
        for bullet in self.arrows:
            index=0
            velx = math.cos(bullet[0])*20
            vely = math.sin(bullet[0])*20
            bullet[1] += velx
            bullet[2] += vely
            if bullet[1] < -64 or bullet[1] > 1000 or bullet[2] < -64 or bullet[2] > 800:
                self.arrows.pop(index)
            index += 1
            for projectile in self.arrows:
                arrow1 = pygame.transform.rotate(imgaud.arrow, 360 - projectile[0] * 57.29)
                self.screen.blit(arrow1, (projectile[1], projectile[2]))

    def draw_background(self):
        for x in range(int(self.width / imgaud.grass.get_width()+1)):
            for y in range(int(self.height / imgaud.grass.get_height()+1)):
                self.screen.blit(imgaud.grass,(x*100,y*100))

        self.screen.blit(imgaud.castle,(30,700))
        self.screen.blit(imgaud.castle,(135,700))
        self.screen.blit(imgaud.castle,(240,700))
        self.screen.blit(imgaud.castle,(345,700))
        self.screen.blit(imgaud.castle,(450,700))
        self.screen.blit(imgaud.castle,(575,700))
        self.screen.blit(imgaud.castle,(700,700))
        self.screen.blit(imgaud.castle,(815,700))


    def results(self):
        if self.acc[1] != 0:
            self.accuracy = self.acc[0] * 1.0 / self.acc[1] * 100
        else:
            self.accuracy = 0

    #10 - Win/Lose check
        if self.time >= self.time_left:
            self.running = 0
            self.exitcode = 1
            self.win()
        if self.healthvalue <= 0:
            self.running = 0
            self.exitcode = 0
            self.lost()

    def win(self):
        text = self.font.render("Accuracy: "+str(round(self.accuracy, 2))+"%", True, (0,255,0))
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery+24
        self.screen.blit(imgaud.youwin, (0,0))
        self.screen.blit(text, textRect)


    def lost(self):
        text = self.font.render("Accuracy: "+str(round(self.accuracy, 2))+"%", True, (255,0,0))
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery+24
        self.screen.blit(imgaud.gameover, (0,0))
        self.screen.blit(text, textRect)
