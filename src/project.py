import math
import random
import pygame
from PIL import Image
from pygame import mixer

def main():

    # Initialize the mixer
    mixer.init()

    # Initialize the pygame
    pygame.init()

    # Declare nonlocal variables
    # Create the screen in full screen mode
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)

    # Intro Screen
    intro = True
    while intro:
        screen.fill((0, 0, 0))
        intro_font = pygame.font.Font('freesansbold.ttf', 64)
        intro_text = intro_font.render("Welcome to Weirdmageddon", True, (255, 255, 255))
        instructions_font = pygame.font.Font('freesansbold.ttf', 32)
        instructions_text = instructions_font.render("Press ENTER to Start, ESC to Quit", True, (255, 255, 255))
        
        screen.blit(intro_text, (screen.get_width() // 2 - intro_text.get_width() // 2, screen.get_height() // 2 - intro_text.get_height() // 2 - 50))
        screen.blit(instructions_text, (screen.get_width() // 2 - instructions_text.get_width() // 2, screen.get_height() // 2 - instructions_text.get_height() // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start
                    intro = False
                if event.key == pygame.K_ESCAPE:  # Press Escape to quit
                    pygame.quit()
                    exit()

    # Background
    background = pygame.image.load('background.png')
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))


    # Sound
    mixer.music.load("background.wav")
    mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Weirdmageddon")
    icon = pygame.image.load('bill.png')
    pygame.display.set_icon(icon)

    # Player
    playerImg = pygame.image.load('md.png')
    playerX = screen.get_width() // 2 - playerImg.get_width() // 2
    playerY = screen.get_height() - playerImg.get_height() - 20
    playerX_change = 0

    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('bill.png'))
        enemyX.append(random.randint(0, screen.get_width() - 64))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    # Bullet
    bulletImg = pygame.image.load('nyan_cat.png')
    bulletX = 0
    bulletY = playerY
    bulletY_change = 10
    bullet_state = "ready"

    # Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (screen.get_width() // 2 - over_text.get_width() // 2, screen.get_height() // 2 - over_text.get_height() // 2))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        return distance < 27


    # Initialize global variables
    bulletY = playerY
    bullet_state = "ready"
    score_value = 0

    # Game Loop
    running = True
    while running:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))

        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If keystroke is pressed check whether it's right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()

                        # Get the current x coordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= screen.get_width() - playerImg.get_width():
            playerX = screen.get_width() - playerImg.get_width()

        # Enemy Movement
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > screen.get_height() - 100:
                for j in range(num_of_enemies):
                    enemyY[j] = screen.get_height() + 1000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= screen.get_width() - enemyImg[i].get_width():
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = playerY
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, screen.get_width() - enemyImg[i].get_width())
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()

if __name__ == "__main__":
    main()
