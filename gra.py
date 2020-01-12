# 1 - Import library
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
from src import core

class SpaceAdv(core.SpaceAdvCore):
    def menu(self):
        positionsText = self.font.render("{}".format('New Game'), True, (0,0,0))
        textRect = positionsText.get_rect()
        textRect.topright=[935,5]
        self.screen.blit(positionsText, textRect)

    def main(self):
        while self.running:
            if self.old_time < int(time.time()):
                self.old_time = int(time.time())
                self.time += 1000

            self.badtimer -= 1
            # 5 - clear the screen before drawing it again
            self.screen.fill(0)

            # 6 - draw the screen elements
            self.draw_background()

            # 6.1 - Set player position and rotation
            self.playerpos[0] += self.speed[0]
            self.playerpos[1] += self.speed[1]

            position = pygame.mouse.get_pos()
            angle = math.atan2(position[1] - (self.playerpos[1] + 32),position[0] - (self.playerpos[0] + 26))
            playerRot = pygame.transform.rotate(imgaud.player, 360-angle*57.29)
            move = self.get_move_pos(position, angle, playerRot)
            if move[0] >= self.width - 80 or move[0] <= 20:
                self.speed[0] = 0

            if move[1] >= self.height- 80 or move[1] <= 20:
                self.speed[1] = 0

            playerpos1 = (move[0], move[1])
            self.screen.blit(playerRot, playerpos1)


            # Draw position of ship
            positionsText = self.font.render("({}, {})".format(move[0], move[1]), True, (0,0,0))
            textRect = positionsText.get_rect()
            textRect.topright=[935,5]
            self.screen.blit(positionsText, textRect)
            # 6.2 - Draw arrows
            self.draw_arrows()

            # 6.3 - Draw badgers
            if self.badtimer == 0:
                tmp = {
                    "pos": [randint(50,800), 0],
                    "img": imgaud.badguyimg1[randint(0,3)]
                }
                self.badguys.append(tmp)
                self.badtimer = 100 - (self.badtimer1 * 2)
                if self.badtimer1 >= 35:
                    self.badtimer1 = 35
                else:
                    self.badtimer1 += 5
            index = 0

            for badguy in self.badguys:
                if badguy['pos'][1] < -750:
                    self.badguys.pop(index)
                badguy['pos'][1] += 10

                # 6.3.1 - Attack castle
                badrect = pygame.Rect(badguy['img'].get_rect())
                badrect.top = badguy['pos'][1]
                badrect.left = badguy['pos'][0]
                if badrect.top > 750:
                    self.healthvalue -= randint(5,20)
                    self.badguys.pop(index)
                    imgaud.hit.play()

                #6.3.2 - Check for collisions
                index1 = 0
                for bullet in self.arrows:
                    bullrect = pygame.Rect(imgaud.arrow.get_rect())
                    bullrect.left = bullet[1]
                    bullrect.top = bullet[2]
                    if badrect.colliderect(bullrect):
                        self.acc[0]+=1
                        self.badguys.pop(index)
                        self.arrows.pop(index1)
                        #sound
                        imgaud.enemy.play()
                        tmp = {
                            "pos": badguy['pos'],
                            "img": imgaud.deadimg1[randint(0,2)]
                        }

                        self.screen.blit(imgaud.explode, badguy['pos'])
                        self.deads.append(tmp)
                    index1 += 1

                # 6.3.3 - Next bad guy
                index += 1

            for dead in self.deads:
                self.screen.blit(dead['img'], dead['pos'])

            for badguy in self.badguys:
                self.screen.blit(badguy['img'], badguy['pos'])

            # 6.4 - Draw clock
            survivedText = self.font.render(str(int((self.time_left - self.time) / 60000)) + ":" + str(round((self.time_left - self.time) / 1000 % 60)).zfill(2), True, (0,0,0))
            textRect = survivedText.get_rect()
            textRect.topright = [635,5]
            self.screen.blit(survivedText, textRect)

            # 6.5 - Draw health bar
            self.screen.blit(imgaud.healthbar, (5,5))
            for health1 in range(self.healthvalue):
                self.screen.blit(imgaud.health, (health1+8,8))

            # 7 - update the screen
            pygame.display.flip()
            # 8 - loop through the events
            for event in pygame.event.get():
                # check if the event is the X button
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key==pygame.K_UP:
                        self.keys['up'] = True
                    elif event.key == pygame.K_a or event.key==pygame.K_LEFT:
                        self.keys['left'] = True
                    elif event.key == pygame.K_s or event.key==pygame.K_DOWN:
                        self.keys['down'] = True
                    elif event.key == pygame.K_d or event.key==pygame.K_RIGHT:
                        self.keys['right'] = True
                    elif event.key == pygame.K_r:
                        self.keys['reset'] = True

                if event.type == pygame.KEYUP:
                    if event.key==pygame.K_w or event.key==pygame.K_UP:
                        self.keys['up'] = False
                    elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
                        self.keys['left'] = False
                    elif event.key==pygame.K_s or event.key==pygame.K_DOWN:
                        self.keys['down'] = False
                    elif event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                        self.keys['right'] = False
                    elif event.key==pygame.K_r:
                        self.keys['reset'] = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    self.acc[1] += 1
                    self.arrows.append([math.atan2(position[1] - (playerpos1[1] + 32),position[0] - (playerpos1[0] + 26)), playerpos1[0] + 32, playerpos1[1] + 32])
                    imgaud.shoot.play()
                if event.type==pygame.QUIT:
                    # if it is quit the game
                    pygame.quit()
                    exit(0)

            # 9 - Move player
            if self.keys['up']:
                self.speed[1] -= 0.1
            elif self.keys['down']:
                self.speed[1] += 0.1
            if self.keys['left']:
                self.speed[0] -= 0.1
            elif self.keys['right']:
                self.speed[0] += 0.1
            if self.keys['reset']:
                return self.reset()

            self.results()

            while not self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                pygame.display.flip()



pygame.init()
game = SpaceAdv()
# game.menu()
game.main()
