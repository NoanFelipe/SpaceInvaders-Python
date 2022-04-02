import pygame
from Bullet import bullet
import SoundEffect

class player:
    def __init__(self, x, y):
        self.scale = 3
        self.lifes = 4
        self.sprite = pygame.transform.scale(pygame.image.load("Sprites/PlayerSpritev2.png"), (13 * self.scale, 8 * self.scale))
        self.rect = self.sprite.get_rect().move((x, y))
        self.x = x
        self.y = y
        self.speed = 2.5
        self.se = SoundEffect.SoundEffect()
        self.was_hit = False
        self.was_hit_timer = 0
        self.was_hit_timer_length = 110 #length of explosion sound effect
        self.not_draw = False

    def draw(self, window):
        if self.was_hit:
            self.sprite = pygame.transform.scale(pygame.image.load("Sprites/destroyedShip1.png"), (16 * self.scale, 8 * self.scale))

            if self.was_hit_timer >= 5 and self.was_hit_timer < 10 or self.was_hit_timer >= 15 and self.was_hit_timer < 20 or self.was_hit_timer >= 25 and self.was_hit_timer < 30 or self.was_hit_timer >= 35 and self.was_hit_timer < 40 or self.was_hit_timer >= 45:
                self.sprite = pygame.transform.scale(pygame.image.load("Sprites/destroyedShip2.png"), (16 * self.scale, 8 * self.scale))

            if self.was_hit_timer > 50:
                self.not_draw = True

            if self.was_hit_timer > self.was_hit_timer_length:
                self.not_draw = False
                self.was_hit = False
                self.was_hit_timer = 0
                self.rect[0] = 50
                self.x = 50
                self.sprite = pygame.transform.scale(pygame.image.load("Sprites/PlayerSpritev2.png"), (13 * self.scale, 8 * self.scale))
                return

            self.was_hit_timer += 1

        if not self.not_draw:
            window.blit(self.sprite, self.rect)

    def move(self, dir, window_width):
        if self.was_hit: return

        if self.x >= 2: #checks if the player hit the edge of the screen
            if dir == 0: #move left
                self.x -= self.speed
        if self.x <= window_width - self.rect[2] - 4:
            if dir == 1: #move right
                self.x += self.speed
        
        self.rect[0] = self.x
    
    #shoots bullet if player hits space bar, gets called in function "check_for_inputs"
    def shoot(self, bullets):
        if self.was_hit: return

        if len(bullets) < 1:
            """print("Olá")"""
            self.se.shoot.play()
            bullets.append(bullet(self.x, self.y, (0,0,0)))
    
    def damage(self, pauseEnemies, enemies):
        if self.was_hit: return
        
        pauseEnemies(self.was_hit_timer_length, enemies)
        self.se.explosion.play()
        self.was_hit = True
        self.lifes -= 1


