import pygame
import random
import math

# Intialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('forest.png')

# Title and Icon
pygame.display.set_caption("Fire Slayer")
# icon = pygame.image.load("dragon.png")
# pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('satyr.png')
playerX = 370
playerY = 480
move_X = 0

# Enemy
enemyImg = pygame.image.load('monster.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 3
enemyY_change = 40

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# ready - you cant see bullet
# fire - the bullet is moving
bullet_state = "ready"








# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 25, y))




def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
working = True
while working:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            working = False

        # Check if button pressed is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                move_X = -3
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                move_X = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)







        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                move_X = 0
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                move_X = 0

    playerX += move_X
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 3
        enemyY += enemyY_change

    elif enemyX >= 736:
        enemyX_change = -3
        enemyY += enemyY_change

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        print(score_value)
        enemyX = random.randint(0, 800)
        enemyY = random.randint(50, 150)


    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, testY)
    pygame.display.update()
