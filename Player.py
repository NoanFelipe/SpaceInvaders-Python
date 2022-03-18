from turtle import window_width
import pygame
from Bullet import bullet

class player:
    def __init__(self, x, y):
        self.scale = 3
        self.lifes = 4
        self.sprite = pygame.transform.scale(pygame.image.load("PlayerSpritev2.png"), (11 * self.scale, 6 * self.scale))
        self.rect = self.sprite.get_rect().move((x, y))
        self.x = x
        self.y = y
        self.speed = 2.5

    def draw(self, window):
        window.blit(self.sprite, self.rect)

    def move(self, dir, window_width):
        if self.x >= 2: #checks if the player hit the edge of the screen
            if dir == 0: #move left
                self.x -= self.speed
                self.rect[0] = self.x
        if self.x <= window_width - self.rect[2] - 4:
            if dir == 1: #move right
                self.x += self.speed
                self.rect[0] = self.x
    
    def shoot(self, bullets):
        if len(bullets) < 1:
            """print("Olá")"""
            bullets.append(bullet(self.x, self.y, (0,0,0)))

