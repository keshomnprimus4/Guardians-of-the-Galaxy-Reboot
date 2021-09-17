import pygame
from pygame import mixer
import random
import math

#initialize pygame
pygame.init()

#create the screen and background
screen = pygame.display.set_mode((1540,800))
background = pygame.image.load(r'venv/spacebackground.jpg')

#Background Music
mixer.music.load(r'venv/backgroundmusic.mp3')
mixer.music.play()

#Title
pygame.display.set_caption("Galaxy Guardians")
icon = pygame.image.load(r'venv/ufo.png')
pygame.display.set_icon(icon)

#Player
playerimage = pygame.image.load(r'venv/spaceship.png')
playerX = 750
playerY = 625

#Enemies
enemy1image = []
enemy1X = []
enemy1Y = []
enemy1Xchange = []
enemy1Ychange = []
numofenemy1 = 6
for i in range(numofenemy1):
    enemy1image.append(pygame.image.load(r'venv/alien1.png'))
    enemy1X.append(random.randint(40, 1390))
    enemy1Y.append(random.randint(-150, 0))
    enemy1Xchange.append(1)
    enemy1Ychange.append(0.1)


enemy2image = []
enemy2X = []
enemy2Y = []
enemy2Xchange = []
enemy2Ychange = []
numofenemy2 = 6
for i in range(numofenemy2):
    enemy2image.append(pygame.image.load(r'venv/alien2.png'))
    enemy2X.append(random.randint(1088, 1390))
    enemy2Y.append(random.randint(-150, 0))
    enemy2Xchange.append(1.5)
    enemy2Ychange.append(0.2)

#Bullets
#Ready - bullet not on screen
#Fire - bullet moving on screen
bullet1image = pygame.image.load(r'venv/bullet.png')
bullet1X = 0
bullet1Y = 625
bullet1Xchange = 0
bullet1Ychange = 4
bullet1state = 'ready'

bullet2image = pygame.image.load(r'venv/bullet.png')
bullet2X = 0
bullet2Y = 625
bullet2Ychange = 4
bullet2state = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 1375
texty = 100

gameoverfont = pygame.font.Font('freesansbold.ttf', 512)

def printscore(x, y):
    totalscore = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(totalscore, (x, y))

def gameovertext(x,y):
    gameover = font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(gameover, (x, y))

def firebullets(x,y):
    global bullet1state
    bullet1state = "fire"
    screen.blit(bullet1image,(x, y))

    global bullet2state
    bullet2state = "fire"
    screen.blit(bullet2image, (x, y))

def player():
    screen.blit(playerimage,(playerX,playerY))

def enemy1(x, y, i):
    screen.blit(enemy1image[i],(x, y))

def enemy2(x, y, i):
    screen.blit(enemy2image[i],(x, y))

def collision1(bullet1X, bullet1Y, bullet2X, bullet2Y, enemy1X, enemy1Y):
    distance1 = math.sqrt(((enemy1X - bullet1X)**2)+((enemy1Y - bullet1Y)**2))
    distance2 = math.sqrt(((enemy1X - bullet2X)**2)+((enemy1Y - bullet2Y)**2))

    if (distance1 < 25) or (distance2 < 25):
        return True
    else:
        return False

def collision2(bullet1X, bullet1Y, bullet2X, bullet2Y, enemy2X, enemy2Y):
    distance3 = math.sqrt(((enemy2X - bullet1X)**2)+((enemy2Y - bullet1Y)**2))
    distance4 = math.sqrt(((enemy2X - bullet2X)**2)+((enemy2Y - bullet2Y)**2))

    if (distance3 < 25) or (distance4 < 25):
        return True
    else:
        return False

#Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,150)) #Red, Green, Blue

    # Background Image
    screen.blit(background, (0, 0))

    #Enemy movement
    for i in range(numofenemy1):
        if enemy1Y[i] > 700:
            for j in range(numofenemy1):
                enemy1Y[j] = 1000
            break
        enemy1X[i] += enemy1Xchange[i]
        enemy1Y[i] += enemy1Ychange[i]
        if enemy1X[i] <= 0:
            enemy1Xchange[i] = 1
        if enemy1X[i] >= 1400:
            enemy1Xchange[i] = -1

        isitacollision1 = collision1(bullet1X, bullet1Y, bullet2X, bullet2Y, enemy1X[i], enemy1Y[i])
        if isitacollision1:
            bulletsound = mixer.Sound(r'venv/explosion.wav')
            bulletsound.play()
            bullet1Y = 625
            bullet2Y = 625
            bullet1state = 'ready'
            bullet2state = 'ready'
            score = score + 1
            print(score)
            enemy1X[i] = random.randint(40, 1390)
            enemy1Y[i] = random.randint(-150, 0)
        enemy1(enemy1X[i], enemy1Y[i], i)

    for i in range(numofenemy2):
        if enemy2Y[i] > 700:
            for j in range(numofenemy2):
                enemy2Y[j] = 1000
            gameovertext(700, 400)
            break
        enemy2X[i] += enemy2Xchange[i]
        enemy2Y[i] += enemy2Ychange[i]
        if enemy2X[i] <= 0:
            enemy2Xchange[i] = 2
        if enemy2X[i] >= 1400:
            enemy2Xchange[i] = -2

        isitacollision2 = collision2(bullet1X, bullet1Y, bullet2X, bullet2Y, enemy2X[i], enemy2Y[i])
        if isitacollision2:
            bulletsound = mixer.Sound(r'venv/explosion.wav')
            bulletsound.play()
            bullet1Y = 625
            bullet2Y = 625
            bullet1state = 'ready'
            bullet2state = 'ready'

            score = score + 1
            print(score)

            enemy2X[i] = random.randint(1088, 1390)
            enemy2Y[i] = random.randint(-150, 0)
        enemy2(enemy2X[i], enemy2Y[i], i)

    #if a keystroke is pressed, check whether the left or right keystroke is pressed, then move the player
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= 2
            if playerX <= 5:
                playerX = 5

        if event.key == pygame.K_RIGHT:
            playerX += 2
            if playerX >= 1400:
                playerX = 1400

        if event.key == pygame.K_UP:
            if bullet1state == "ready" and bullet2state == "ready":
                bulletsound = mixer.Sound(r'venv/laser.wav')
                bulletsound.play()
            #bullet = current x-coordinate of the ship, not a moving coordinate
            bullet1X = playerX
            bullet2X = playerX + 64
            #fire the bullets from the current position
            firebullets(bullet1X,bullet1Y)
            firebullets((bullet2X),bullet2Y)

    # Bullet Movement
    if bullet1Y <= -50 or bullet2Y <= -50:
        bullet1Y = 625
        bullet2Y = 625
        bullet1state = 'ready'
        bullet2state = 'ready'

    if bullet1state == "fire":
        firebullets(bullet1X, bullet1Y)
        bullet1Y -= bullet1Ychange
    if bullet2state == "fire":
        firebullets((bullet2X), bullet2Y)
        bullet2Y -= bullet2Ychange

    player()
    enemy1(enemy1X[i], enemy1Y[i], i)
    enemy2(enemy2X[i], enemy2Y[i], i)
    printscore(textx, texty)
    pygame.display.update()
