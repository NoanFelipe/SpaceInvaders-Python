from tkinter import Scale
import pygame

class bullet:
    bullet_width = 1
    bullet_height = 4
    color = (0,255,255)
    speed = 10
    enemy_bullet_speed = 4.5
    scale = 3 

    def __init__(self, x, y, color2):
        self.x = x + self.bullet_width * self.scale * 6
        self.y = y - self.bullet_height * self.scale
        self.color2 = color2
        self.rect = pygame.Rect((self.x, self.y), (self.bullet_width * self.scale, self.bullet_height * self.scale))
     
    def move(self, bullet_type):
        if bullet_type == 1:
            self.y -= self.speed
            self.rect[1] = self.y
        if bullet_type == 2:
            self.y += self.enemy_bullet_speed
            self.rect[1] = self.y

    def draw(self, window, bullet_type):
        if bullet_type == 1:
            pygame.draw.rect(window, self.color2, self.rect)
        if bullet_type == 2:
            pygame.draw.rect(window, self.color, self.rect)
    