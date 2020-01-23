import pygame
import random

# globals
windowwidth = 600
windowheight = 480
snakewidth = 25
snakeheight = 25
snakex = 10
snakey = 10
snakespeed = 10
dotradius = 10
snakepathmaxlen = 500
checkdistancefortailhit = 10
numoflasttailpiecestocheck = 10

pygame.init()
screen = pygame.display.set_mode((windowwidth, windowheight))
clock = pygame.time.Clock()
quit = False
dotcoord = (random.randint(0, windowwidth), random.randint(0, windowheight))
collecteddots = 0
snakepath = []
oldsnakex = snakex
oldsnakey = snakey
lastkey = 0

while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    # Keypresses
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] or lastkey == pygame.K_UP:
        lastkey = pygame.K_UP
        snakey -= snakespeed
    if pressed[pygame.K_DOWN] or lastkey == pygame.K_DOWN:
        lastkey = pygame.K_DOWN
        snakey += snakespeed
    if pressed[pygame.K_LEFT] or lastkey == pygame.K_LEFT:
        lastkey = pygame.K_LEFT
        snakex -= snakespeed
    if pressed[pygame.K_RIGHT] or lastkey == pygame.K_RIGHT:
        lastkey = pygame.K_RIGHT
        snakex += snakespeed

    # Rember old position
    if snakex != oldsnakex or snakey != oldsnakey:
        snakepath.append((oldsnakex, oldsnakey))
        # Remove old entries
        snakepath = snakepath[-snakepathmaxlen:]

    # Blank screen
    screen.fill((0, 0, 0))

    # Draw the snake
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(snakex, snakey, snakewidth, snakeheight))

    # Draw the snakes tail
    for i in range(0, collecteddots * numoflasttailpiecestocheck):
        try:
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect(snakepath[len(snakepath) - i][0], snakepath[len(snakepath) - i][1], snakewidth,
                                         snakeheight))
        except:
            pass

    if not dotcoord:
        # Get new dotcoords
        dotcoord = (random.randint(0, windowwidth), random.randint(0, windowheight))
    else:
        # Draw the dot
        pygame.draw.circle(screen, (255, 0, 0), dotcoord, dotradius)

        # Check for collision with a dot
    if ((snakex + snakewidth) >= dotcoord[0] - dotradius and (snakex - snakewidth) <= dotcoord[0] + dotradius) and \
            ((snakey + snakeheight) >= dotcoord[1] - dotradius and (snakey - snakeheight) <= dotcoord[1] + dotradius):
        dotcoord = False
        collecteddots += + 1

    # Check for collision with self -> gameover
    for i in range(checkdistancefortailhit, collecteddots * numoflasttailpiecestocheck):
        try:
            if ((snakex + snakewidth) >= snakepath[len(snakepath) - i][0] - dotradius and (snakex - snakewidth) <=
                snakepath[len(snakepath) - i][0] + dotradius) and \
                    ((snakey + snakeheight) >= snakepath[len(snakepath) - i][1] - dotradius and (
                            snakey - snakeheight) <= snakepath[len(snakepath) - i][1] + dotradius):
                print("Collected: " + str(collecteddots) + " dots!")
                quit = True
                break
        except:
            pass

    # Check for end of the world
    if snakex < 0: snakex = windowwidth - snakewidth
    if (snakex + snakewidth) > windowwidth: snakex = 0
    if snakey < 0: snakey = windowheight - snakeheight
    if (snakey + snakeheight) > windowheight: snakey = 0

    # Remember old position
    oldsnakex = snakex
    oldsnakey = snakey

    # Show new Screen
    pygame.display.flip()

    # Wait until 1/60 second has passed
    clock.tick(60)
