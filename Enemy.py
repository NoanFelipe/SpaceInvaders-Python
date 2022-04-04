import pygame
from Bullet import bullet
from random import randint

class enemy:
    def __init__(self, x, y):
        self.scale = 3
        self.type = 1
        self.color = "green"
        self.bullet_color = (255,255,255)
        self.current_sprite = 1
        self.sprite = pygame.transform.scale(pygame.image.load(f"Sprites/Enemy{self.type}pos{self.current_sprite}{self.color}.png"), (11 * self.scale, 8 * self.scale))
        self.rect = self.sprite.get_rect().move((x, y))
        self.life = 1

        self.has_died = False
        self.death_timer_length = 8
        self.death_timer = 0

        self.isRed = False

        self.is_paused = False
        self.pause_timer_length = 0
        self.pause_timer = 0

        self.timer = 0
        self.timer_length = 40

        self.has_shot = False
        self.has_shot_timer = 0
        self.has_shot_timer_length = 10
        
        self.dir = 1
        self.is_shooter = False
        self.can_move_down = True
        self.is_on_player_layer = False
        self.speed = 4

    def draw(self, window):
        if self.rect[1] == 295-20 or self.rect[1] == 340-20:
            self.color = "green"
            self.bullet_color = (0, 255, 0)
        elif self.rect[1] == 385-20 or self.rect[1] == 430-20:
            self.color = "cyan"
            self.bullet_color = (0, 255, 255)
        elif self.rect[1] == 475-20 or self.rect[1] == 520-20:
            self.color = "pink"
            self.bullet_color = (255, 0 ,255)
        elif self.rect[1] == 565-20 or self.rect[1] == 610-20:
            self.color = "yellow"
            self.bullet_color = (255, 255, 0)
        elif self.rect[1] >= 655-20:
            self.color = "red"
            self.bullet_color = (255, 0, 0)

        if self.current_sprite > 2:
            self.current_sprite = 1
        
        self.sprite =  pygame.transform.scale(pygame.image.load(f"Sprites/Enemy{self.type}pos{self.current_sprite}{self.color}.png"), (11 * self.scale, 8 * self.scale))

        if self.isRed:
            self.sprite =  pygame.transform.scale(pygame.image.load(f"Sprites/Enemy{self.type}pos{self.current_sprite}red.png"), (11 * self.scale, 8 * self.scale))

        window.blit(self.sprite, self.rect)

    def shoot(self, enemy_bullets):
        if not self.is_shooter: return
        if self.is_paused: return

        if self.has_shot:
            self.has_shot_timer += 1
            if self.has_shot_timer > self.has_shot_timer_length:
                self.has_shot = False
                self.has_shot_timer = 0

        if not self.has_shot:
            chance_of_shooting = randint(0, 350)
            if chance_of_shooting == 7:
                if len(enemy_bullets) <= 3:
                    """print("Olá")"""
                    self.has_shot = True
                    enemy_bullets.append(bullet(self.rect[0], self.rect[1] + 10 * self.scale, self.bullet_color))

    def check_move_down(self, enemies_list): #checks if enemy is on the players "layer" and changes enemy "dir" and "can_move_down" variables
        can_move = True
        if self.rect[1] > 725:
            can_move = False
            self.is_on_player_layer = True
        
        if not(can_move):
            for column in enemies_list:
                for enemy in column:
                    enemy[1].can_move_down = False

    def updateDeadEnemy(self, index, deadEnemiesList, window):
        if self.death_timer > self.death_timer_length:
            deadEnemiesList.pop(index)
            return
        self.sprite = pygame.transform.scale(pygame.image.load(f"Sprites/explosion{self.color}.png"), (16 * self.scale, 8 * self.scale))
        window.blit(self.sprite, self.rect)
        self.death_timer += 1

    def move(self, enemy_hit_wall, player_x, texts):
        if self.is_paused:
            if self.pause_timer > self.pause_timer_length:
                self.pause_timer = 0
                self.pause_timer_length = 0
                self.is_paused = False
                if self.isRed:
                    self.isRed = False
                for text in texts:
                    text.isRed = False
            self.pause_timer += 1
            return

        self.timer += 1

        if not(self.is_on_player_layer):
            if enemy_hit_wall:
                enemy_hit_wall = False
                self.dir += 1
                if self.can_move_down:
                    self.rect[1] += 45
                
                if self.dir > 2:
                    self.dir = 1

                if self.dir == 1:
                    self.rect[0] += 5
                elif self.dir == 2:
                    self.rect[0] -= 5
        else:
            if player_x > self.rect[0]:
                self.dir = 1
            else:
                self.dir = 2
            
            if self.timer_length > 2.5:
                self.timer_length = 2.5

            if enemy_hit_wall:
                enemy_hit_wall = False
                if self.dir == 1:
                    self.rect[0] += 5
                elif self.dir == 2:
                    self.rect[0] -= 5


        if self.timer > self.timer_length:
            self.current_sprite += 1

            if self.dir == 1:
                self.rect[0] += self.speed
            elif self.dir == 2:
                self.rect[0] -= self.speed
                
            self.timer = 0       
    