import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo1.png")
pygame.display.set_icon(icon)

#creating background
background = pygame.image.load("space_invaders_background.jpg")

#loading the background music and playing it
mixer.music.load("background.wav")
#-1 makes it play forever
mixer.music.play(-1)


#create the screen
screen= pygame.display.set_mode((800,600)) #width, height

#creating the player image
playerImg = pygame.image.load("spaceship.png")
#giving it coordinates
#top left of screen is (0,0)
playerX = 370
playerY = 480
playerX_change = 0

#creating a list that stores all of the enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

#creating multiples enemies and storing the enemies in a list
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    
    #randint includes 736
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.3)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = random.randint(0, 800)
bulletY = 480
bulletX_change = 0
#when we press the bullet its going to change y coordinates by 10
bulletY_change = 5
#states: fire and ready
bullet_state = "ready"

#tracks the users change when using keys


#creating a fucntion to call the player in the while loop
def player(x, y):
    #painting the player on the screen using the blit method 
    screen.blit(playerImg, (x, y))

#enemy function
def enemy(x, y, i):
    #enemyImg[i] because there are 6 images
    screen.blit(enemyImg[i],(x, y))

#firing the bullet
def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    #+16 and +10 bc we're shooting from the middle of the spaceship
    screen.blit(bulletImg, (x + 16, y + 10))

#bullet hitting the enemy
def if_collision(enemyX, enemyY, bulletX, bulletY):
    #using the distance formaula to see if the bullet is close enought to the enemy
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    #if it's close by 25 pixels, return True
    if distance <= 25:
        return True


score_value = 0
#where the score will appear
textX = 0
textY = 0

#creating the style of the text
#freesansbold.ttf is the font and 32 is the size
font = pygame.font.Font('freesansbold.ttf', 32)
def show_score(x, y):
    #creating and rendering score, RGB color
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    #showing the rendered score on the screen
    screen.blit(score, (x, y))

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 100)
#middle


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (150, 250))

#infinate game loop so the game always runs and window doesn't close down
loop = True
while loop:

    #the screen is the first thing we create
    screen.fill((0,0,0))

    #painting the background 
    screen.blit(background, (0,0))
    
    #pygame.event.get() GETS all of the events and we for loop through them
    for event in pygame.event.get():
        #if one of the events == quit(exit) then infinate loop stops
        if event.type == pygame.QUIT:
            loop = False
        
        #pygame.KEYDOWN checks if any key is down
        if event.type == pygame.KEYDOWN:
            #pygame.K_LEFT checks if the left arrow is pressed down
            if event.key == pygame.K_LEFT:
                #if it's pressed down playerX goes to the left bc its negative
                playerX_change = -1.5
                #checks if right arrow is pressed down
            if event.key == pygame.K_RIGHT:
                #playerX is going to right because it's adding a positive number
                playerX_change = 1.5
            #if space bar is pressed fire bullet
            if event.key == pygame.K_SPACE:
                #makes bullet_state = "fire" and creates the bullet
                    #should only shoot bullets when bullet_state == "ready"(ready when y = 0 or out of screen)
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    #gets x-cor of spaceship and stores it, bc playerX changes when we hit the arrow keys
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        #pygame.KEYUP checks if any key is released
        if event.type == pygame.KEYUP:
            #using mixer.Sound() to play laser sound
            

            #if left or right arrow key is released then there is no change 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #no change == 0 so spaceship stops
                playerX_change = 0
        

    #changing playerX by adding playerX_change(neg or pos)
    #its an infinate loop so it keep checking and moving
    playerX += playerX_change

    #adding bounds
        #736 bc the spaceship is 64 pixels
        #if playerX ever goes above 736 it will autimatically bring it back to 736
    if playerX >= 736:
        playerX = 736
    #left bound
    elif playerX <= 0:
        playerX = 0
    #added the player in the while loop to make sure its always shown
    player(playerX, playerY)
    
    #created a for loop to run through all the enemies
        #checks if one of the enemies hits the border
        #checks if one of the enemies collided with a bullet
        #creates an enemy with specific coordinates and picture
    for i in range(num_of_enemies):

        #game over (enemies hit spaceship)
        if enemyY[i] > 470:
            #j because we want all of the enemies to disapear instead of one i that hit 470
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.3
            enemyY[i] += enemyY_change[i]

        #added colision here so we know which enemy we're talking about
            #if there's a collision then enemies respawn randomly and bullet restarts
        collision = if_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            #bullet restarts and set to ready
            bulletY = 480
            bullet_state = "ready"

            #score increases
            score_value += 1
            #enemy respawns somewhere else
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        #specifiess which image and which coordinates we're creating since there's 6
        enemy(enemyX[i], enemyY[i], i)


    #allow us to have multiple bullets 
    #if it goes beyond 0 bullet resets to 480 and bullet_state is ready so we can't run the if statement below 
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    #x will always be where the player is
    #y always 480 bc that's where it starts
    #the space bar would have turned buller_state into "fire"
    if bullet_state == "fire":
        #makes the bullet and changes the y
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    #slows down everything so have to speed it up
    show_score(textX, textY)
    pygame.display.update()
