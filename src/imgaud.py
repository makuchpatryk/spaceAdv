import pygame
import os

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path
audio_path = os.path.join(resource_path, 'audio') # The image folder path

player = pygame.image.load(os.path.join(image_path, 'dude.png'))
castle = pygame.image.load(os.path.join(image_path, 'castle.png'))
grass = pygame.image.load(os.path.join(image_path, 'grass.png'))
arrow = pygame.image.load(os.path.join(image_path, 'bullet.png'))
health = pygame.image.load(os.path.join(image_path, 'health.png'))
healthbar = pygame.image.load(os.path.join(image_path, 'healthbar.png'))
gameover = pygame.image.load(os.path.join(image_path, 'gameover.png'))
youwin = pygame.image.load(os.path.join(image_path, 'youwin.png'))
explode = pygame.image.load(os.path.join(image_path, 'explode.png'))
deadimg1 = [
    pygame.image.load(os.path.join(image_path, 'dead1.png')),
    pygame.image.load(os.path.join(image_path, 'dead2.png')),
    pygame.image.load(os.path.join(image_path, 'dead3.png')),
    ]

badguyimg1 = [
    pygame.image.load(os.path.join(image_path, 'badguy.png')),
    pygame.image.load(os.path.join(image_path, 'badguy2.png')),
    pygame.image.load(os.path.join(image_path, 'badguy3.png')),
    pygame.image.load(os.path.join(image_path, 'badguy4.png')),
    ]


# 3.1 - Load audio
pygame.mixer.init()

hit = pygame.mixer.Sound(os.path.join(audio_path, 'explode.wav'))
enemy = pygame.mixer.Sound(os.path.join(audio_path, 'enemy.wav'))
shoot = pygame.mixer.Sound(os.path.join(audio_path, 'shoot.wav'))

hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

pygame.mixer.music.load(os.path.join(audio_path, 'background.mp3'))
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
