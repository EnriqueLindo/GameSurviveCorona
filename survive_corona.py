import random
import pygame
from math import atan, degrees, radians, cos, sin, sqrt
import time
pygame.init()

width = 900
height = 900

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Survive Corona")

white = 255, 255, 255
black = 0, 0, 0
red = 150, 0, 0
green = 0, 150, 0
blue = 173, 216, 230

e_dist = sqrt( (width//2)**2 + (height//2)**2 )

class Enemy():
    def __init__(self):
        self.angle = -random.randrange(0, 360)
        self.speed_x = -cos( radians(self.angle) )
        self.speed_y = -sin( radians(self.angle) )
        self.img = pygame.image.load("enemy.png")
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = cos( radians(self.angle) ) * e_dist + width//2 - self.w//2
        self.y = sin( radians(self.angle) ) * e_dist + height//2 - self.h//2

def collided(enemy, shot):
    shot_radius = 10
    shot_center = (shot[0]+shot_radius, shot[1]+shot_radius)

    enemy_radius = 40
    enemy_center = (enemy.x + enemy_radius, enemy.y + enemy_radius)

    dist = sqrt( (shot_center[0]-enemy_center[0])**2 + (shot_center[1]-enemy_center[1])**2 )

    if dist < shot_radius + enemy_radius:
        return True

    return False

def message(msg, size, x, y, color, display):
    font = pygame.font.Font("freesansbold.ttf", size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect()
    display.blit(text, (x-text_rect[2]//2, y-text_rect[3]//2))

def death(points):
    dead = True

    while dead:
        screen.fill(red)

        message("GAME OVER", 100, width//2, 200, white, screen)
        message("POINTS = "+str(points), 60, width//2, 300, white, screen)
        message("Press R to try again", 60, width//2, height - height//4, white, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_loop()

        pygame.display.update()

def main_loop():
    loop = True

    player = pygame.image.load("player.png")
    player_w = player.get_size()[0]
    player_h = player.get_size()[1]

    angle = 0

    player_x = width//2-player_w//2
    player_y = height//2-player_h//2

    shots = []

    enemies = [Enemy()]

    enemy_time = time.time()
    enemy_rate = 1

    points = 0

    hp = 5

    lifebar = pygame.image.load("lifebar5.png")

    while loop:
        screen.fill(black)

        pygame.draw.ellipse(screen, green, (0, 0, width, height))

        #Display lifebar
        lifebar = pygame.image.load("lifebar" + str(hp) + ".png")
        screen.blit(lifebar, (0, 0))

        #Display points
        message("Points="+str(points), 30, width-width//8, 50, white, screen)

        #Display and update enemies
        for c in enemies:
            screen.blit(c.img, (c.x, c.y))
            c.x += c.speed_x
            c.y += c.speed_y
            dist = sqrt( (c.x - width//2)**2 + (c.y - height//2)**2 )
            if dist < 100:
                hp -= 1
                if hp == 0:
                    death(points)
                    loop = False
                enemies.remove(c)

        #Call enemies every a certain time
        if time.time() - enemy_time >= enemy_rate:
            enemies.append(Enemy())
            enemy_time = time.time()

        #Shots display and collision with enemies
        for c in shots:
            for d in enemies:
                if collided(d, c):
                    enemies.remove(d)
                    shots.remove(c)
                    points += 10
            pygame.draw.ellipse(screen, blue, (c[0], c[1], 20, 20))
            c[0] += cos( radians(c[2]) ) * 2
            c[1] += sin( radians(c[2]) ) * 2
            if c[0] < 0 or c[0] + 20 > width or c[1] < 0 or c[1] + 20 > height:
                shots.remove(c)

        #Update the angle according to the mouse's position
        mouse = pygame.mouse.get_pos()

        if mouse[0] > width//2:
            angle = degrees(atan( (mouse[1] - height//2) / (mouse[0] - width//2) )    )
        elif mouse[0] < width//2:
            angle = 180 + degrees(atan( (mouse[1] - height//2) / (mouse[0] - width//2) )    )

        #Display the rotated player
        player_rot = pygame.transform.rotate(player, -angle-90)
        player_rect = player_rot.get_rect()
            #This is complicated because we must adjust its center       
        screen.blit(player_rot, (player_x - player_rect[2]//2 + player_w//2, player_y - player_rect[3]//2 + player_h//2))

        #Aim
        endx = cos(radians(angle)) * 100 + width//2
        endy = sin(radians(angle)) * 100 + height//2

        pygame.draw.line(screen, red, (width//2, height//2), (endx, endy))

        #Damage Circle:

        pygame.draw.ellipse(screen, white, (width//2-100, height//2-100, 200, 200), 1)
    
        #Increase the difficulty
        if 200 > points > 100:
            enemy_rate = 0.8
        elif 300 > points > 200:
            enemy_rate = 0.5
        elif points > 300:
            enemy_rate = 0.3

        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shots.append([width//2-10, height//2-10, angle])

        
        pygame.display.update()

main_loop()