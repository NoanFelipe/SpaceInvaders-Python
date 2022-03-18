import sys, pygame
from Player import player
from Bullet import bullet
from Enemy import enemy
from Text import text
from file_func import create_file, file_exists, write_on_file, read_file
from Wall import wall
from Menu import menu

pygame.init()

window_width = 670
window_height = 900

def check_for_inputs(bullets): #checks for inputs i think
    global Player
    global window
    global window_width

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player.shoot(bullets)
            if event.key == pygame.K_ESCAPE:
                Menu.menu_loop(game_loop)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        Player.move(0, window_width)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        Player.move(1, window_width)

def draw_game_window(window, bullets, enemies, enemy_bullets, texts, score, hi_score, walls): 
    global Player
    window.fill((0,0,0))
    for text in texts:
        text.draw(window)
        texts[0].update_text(f"SCORE: {score}")
        texts[1].update_text(f"{Player.lifes}")
        texts[2].update_text(f"HI-SCORE: {hi_score}")
    for bullet in enemy_bullets:
        bullet.draw(window,1)
    for bullet in bullets:
        bullet.draw(window,2)
    for wall in walls:
        wall.draw(window)
    for column in enemies:
        for enemy in column:
            enemy[1].draw(window)
    for lifes in range(0, Player.lifes - 1):
        window.blit(Player.sprite, ((50 + 40 * lifes, window_height - 35), (11 * Player.scale, 6 * Player.scale)))
    #pygame.draw.line(window, (255,0,0), (0, window_height - 50), (window_width, window_height - 50))
    
    Player.draw(window)
    pygame.display.update()

def check_for_bullets(bullets, enemies): #checks if bullet hit the wall and if bullet hit enemy
    score = 0
    for bullet in bullets:
        if bullet.y > 150 and bullet.y < window_height:
            bullet.move(1)
        else:
            bullets.pop(bullets.index(bullet))

        for column in enemies:
            for enemy in column:
                for bullet in bullets:
                    if is_colliding(bullet.rect, enemy[1].rect):
                        bullets.pop(bullets.index(bullet))
                        enemy[1].life -= 1
                        if enemy[1].life <= 0:
                            score += enemies[enemies.index(column)][column.index(enemy)][2]
                            enemies[enemies.index(column)].pop(enemies[enemies.index(column)].index(enemy))
                            if len(column) == 0:
                                enemies.pop(enemies.index(column))
                            update_columns_list(enemies)
                            update_enemy_speed(enemies)
                            update_shooter(enemies)
    
    return score

def check_enemy_bullets(player_bullets, enemy_bullets, Player): #checks if enemy bullet hit the wall or the player
    for enemy_bullet in enemy_bullets:
        if is_colliding(enemy_bullet.rect, Player.rect):
            Player.lifes -= 1
            enemy_bullets.pop(enemy_bullets.index(enemy_bullet))

        if enemy_bullet.y > 0 and enemy_bullet.y < window_height - 60:
            enemy_bullet.move(2)
        else:
            enemy_bullets.pop(enemy_bullets.index(enemy_bullet))

def check_if_bullet_hit_bullet(enemy_bullets, player_bullets):
    for enemy_bullet in enemy_bullets:
        for player_bullet in player_bullets:
            if is_colliding(enemy_bullet.rect, player_bullet.rect):
                enemy_bullets.pop(enemy_bullets.index(enemy_bullet))
                player_bullets.pop(player_bullets.index(player_bullet))

def enemy_hit_wall(enemies): #checks if one enemy hits the wall, and returns boolean value 
    hit = False
    wall_distance = 25
    for column in enemies:
        for enemy in column:
            if enemy[1].rect[0] + enemy[1].rect[2] > window_width - wall_distance or enemy[1].rect[0] < wall_distance:
                hit = True
                break

    return hit

def create_enemies(won_counter):
    x = 50
    y = 230 + 45 * won_counter

    arr = [[[0] for i in range(5)] for j in range(11)]
    column = 0
    element = 0

    for columns in arr:
        column += 1
        x += 45
        for elements in columns:
            y += 45
            element += 1
            arr[column-1][element-1].append(enemy(x,y))

            if element == 1:
                arr[column-1][element-1][1].type = 2
                arr[column-1][element-1].append(30)
            elif element > 1 and element < 4:
                arr[column-1][element-1][1].type = 1
                arr[column-1][element-1].append(20)
            else:
                arr[column-1][element-1][1].type = 3
                arr[column-1][element-1].append(10)

            if element == 5:
                y = 230 + 45 * won_counter
                arr[column-1][element-1][0] = 1
                element = 0

    update_shooter(arr)

    return arr

def is_colliding(rect1, rect2): # checks if 2 rects are colliding, useful as fuck
    is_colliding = rect1.colliderect(rect2)
    if is_colliding == 1:
        return True
    else:
        return False

def update_enemy_speed(enemies): # updates enemy speed every time one enemy dies, if there is only 1 enemy left, he becomes sonic
    for column in enemies:
        for enemy in column:
            enemy[1].speed += 0.1
            enemy[1].timer_length *= 0.97
            if len(enemies) == 1:
                if len(column) == 1:
                    enemy[1].timer_length = 1.5

def update_shooter(enemies): # sets "is_shooter" value based on the value in enemies list
    for column in enemies:
        for enemy in column:
            if enemies[enemies.index(column)][column.index(enemy)][0] == 1:
                enemy[1].is_shooter = True
            else:
                enemy[1].is_shooter = False

def check_for_game_over(Player, enemies):
    if Player.lifes <= 0:
        return True
    for column in enemies:
        for enemy in column:
            if is_colliding(enemy[1].rect, Player.rect):
                return True
    return False

def check_for_win(enemies):
    if enemies == []:
        return True
    return False
            

def update_columns_list(enemies): # checks if list needs to update the enemy shooter
    column = -1

    for columns in enemies:
        column += 1
        if enemies[column][len(columns)-1][0] != 1:
            enemies[column][len(columns)-1][0] = 1
    
def create_walls(): # create the fucking walls
    global window_width
    y = 700
    arr = []
    space_between_walls = window_width / 5

    for i in range(4):
        arr.append(wall(space_between_walls*(i+1) - 17*3/2, y))
    
    for Wall in arr:
        Wall.create_pixel_rects()

    return arr

def check_wall_colliding_with_bullet(walls, bullets): # checks if player bullets are colliding with wall and destroys wall
    for wall in walls:
        for row in wall.pixels:
            for pixel in row:
                for bullet in bullets:
                    if pixel[0] == 1 and is_colliding(bullet.rect, pixel[1]):
                        index = [wall.pixels.index(row), row.index(pixel)]
                        bullets.pop(bullets.index(bullet))
                        wall.destroy_nearby_pixels(index)
                        pixel[0] = 0 

def check_wall_colliding_with_enemy_bullet(walls, enemy_bullets): # checks if enemy bullets are colliding with wall and destroys wall
    for wall in walls:
        for row in wall.pixels:
            for pixel in row:
                for enemy_bullet in enemy_bullets:
                    if pixel[0] == 1 and is_colliding(enemy_bullet.rect, pixel[1]):
                        index = [wall.pixels.index(row), row.index(pixel)]
                        enemy_bullets.pop(enemy_bullets.index(enemy_bullet))
                        wall.destroy_nearby_pixels(index)
                        pixel[0] = 0

def check_wall_colliding_with_enemies(walls, enemies):
    for row in enemies:
        for enemy in row:
            if enemy[1].rect[1] >= 655 - 20:
                for wall in walls:
                    for row in wall.pixels:
                        for pixel in row:
                            if pixel[0] == 1 and is_colliding(enemy[1].rect, pixel[1]):
                                pixel[0] = 0


def reset_player_lifes(Player):
    Player.lifes = 4

def game_loop():
    global Player
    global clock
    global window
    texts = []
    score = 0
    if not(file_exists("hi_score.txt")):
        create_file("hi_score.txt")
        write_on_file("0", "hi_score.txt")
    hi_score = read_file("hi_score.txt")
    texts.append(text(f"SCORE: {score}", 120, 60, (0,255,255), (0,0,0), "pixelated.ttf", 45))
    texts.append(text(f"{Player.lifes}", 25, 876, (0,255,0), (0,0,0), "pixelated.ttf", 28))
    texts.append(text(f"HI-SCORE: {hi_score}", 470, 60, (0,0,255), (0,0,0), "pixelated.ttf", 45))
    bullets = []
    enemy_bullets = []
    walls = create_walls()
    can_move_down_timer = 60
    won_counter = 0
    enemies = create_enemies(won_counter)
    while True:
        draw_game_window(window, bullets, enemies, enemy_bullets, texts, score, hi_score, walls)
        check_for_inputs(bullets)
        check_if_bullet_hit_bullet(enemy_bullets, bullets)
        score += check_for_bullets(bullets, enemies)
        check_enemy_bullets(bullets, enemy_bullets, Player)
        check_wall_colliding_with_enemies(walls, enemies)
        if bullets != []:
            check_wall_colliding_with_bullet(walls, bullets)
        if enemy_bullets != []:
            check_wall_colliding_with_enemy_bullet(walls, enemy_bullets)
        

        if can_move_down_timer == 60:
            enemy_move_down = enemy_hit_wall(enemies)
        else:
            can_move_down_timer += 1

        for column in enemies:
            for enemy in column:
                enemy[1].check_move_down(enemies)
                enemy[1].move(enemy_move_down, Player.x)
                enemy[1].shoot(enemy_bullets)

        if enemy_move_down:
            enemy_move_down = False
            can_move_down_timer = 0
        
        check_if_bullet_hit_bullet(enemy_bullets, bullets)
        if check_for_win(enemies):
            if won_counter < 3:
                won_counter += 1
            walls = create_walls()
            bullets = []
            enemy_bullets = []
            enemies = create_enemies(won_counter)

        if int(read_file("hi_score.txt")) < score:
            write_on_file(str(score), "hi_score.txt")
            hi_score = score

        if check_for_game_over(Player, enemies):
            reset_player_lifes(Player)
            Menu.game_over = True
            Menu.menu_loop(game_loop)
        
        clock.tick(60)


clock = pygame.time.Clock()
Player = player(322, 780)
window = pygame.display.set_mode((window_width, window_height)) #creates window and stores window object
pygame.display.set_caption("Space Invaders") #sets up window name
Menu = menu()
Menu.menu_loop(game_loop)