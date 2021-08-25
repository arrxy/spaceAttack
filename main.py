import pygame
import random
import math
from pygame import mixer
#initializing pygame
pygame.init()
#create the screen
screen = pygame.display.set_mode((950,600))
#Background
background = pygame.image.load('background.jpg')
#Title and icon
pygame.display.set_caption("Cosmic Raider")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
#Player
playerImg = pygame.image.load('player.png')
playerX = 420
playerY = 480
playerX_change = 0
playerY_change = 0

def player(x,y):
    screen.blit(playerImg,(x,y))
#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(1,882))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.8)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bullet_state = "ready"
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow((enemyX-bulletX),2) + math.pow((enemyY-bulletY),2))
    if distance <27: return True
    else: return False

#SCORE
score_val = 0
font = pygame.font.Font('freesansbold.ttf',26)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("SCORE: " +str(score_val),True, (255,255,255))
    screen.blit(score, (x,y))

#GAME OVER
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (270, 250))
#inf loop to keep the game running
running = True
while running:
    #RGB settings
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keystroke is pressed check if left or down
        speed = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
            if event.key == pygame.K_RIGHT:
                playerX_change = speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    #placing boundary on player
    playerX+=playerX_change
    if playerX<0: playerX = 0
    elif playerX>=886: playerX = 886

    # Enemy Movement
    for i in range(no_of_enemies):

        #GAME OVER
        if enemyY[i] > 420:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 886:
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            coll_sound = mixer.Sound('explosion.wav')
            coll_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(1, 882)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY<=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()