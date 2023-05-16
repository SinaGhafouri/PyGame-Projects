import pygame
pygame.init()
# pygame.font.init()
pygame.mixer.init()
from CNST import *
from functions import *
import random
import numpy as np

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Score board:
SCORE_BOARD = pygame.draw.rect(SCREEN, SB_COLOR, (0, HEIGHT-SCORE_BOARD_HEIGHT, WIDTH, SCORE_BOARD_HEIGHT))

COUNTER = 0
clock = pygame.time.Clock()
running = True
while running:
    COUNTER += 1
    clock.tick(60)
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    if COUNTER%random.randint(40, 100)==0:
        FRUIT_ENTERED = True
        random_fruit_names.append(FRUIT_NAMES[random.randint(0, len(FRUIT_NAMES)-1)])
        FRUIT_IMAGES.append(pygame.image.load(f'images/{random_fruit_names[-1]}.png'))
        FRUIT_SIZES.append(FRUIT_IMAGES[-1].get_size())
        FRUIT_X0S.append(random.randint(0, WIDTH))
        FRUIT_SURFACES.append(pygame.draw.rect(SCREEN, (0,0,0), (FRUIT_X0S[-1], HEIGHT, FRUIT_SIZES[-1][0], FRUIT_SIZES[-1][1])))
        FRUIT_X_MOVEMENTS.append(np.sign(WIDTH/2-FRUIT_X0S[-1])*random.randint(1,5))
        FRUIT_ANGLES.append(0)
        FRUIT_TIMES.append(0)

    ms = pygame.mouse.get_pressed()[0]
    for i in range(len(FRUIT_SURFACES)):
        m = pygame.mouse.get_pos()
        pygame.draw.circle(SCREEN, (255,100,100), (m[0],m[1]), 40, 10) # mouse
        if ms==True and FRUIT_SURFACES[i].collidepoint(m) and random_fruit_names[i]!='boom':
            HIT_SOUND.play()
            POINTS += 1
            SIZE_X, SIZE_Y = FRUIT_SURFACES[i].size
            FRUIT_IMAGES[i] = pygame.transform.scale(HIT_IMAGE, (SIZE_X, SIZE_Y))
        elif ms==True and FRUIT_SURFACES[i].collidepoint(m) and random_fruit_names[i]=='boom':
            BOOM_SOUND.play()
            POINTS -= 1
            SIZE_X, SIZE_Y = FRUIT_SURFACES[i].size
            FRUIT_IMAGES[i] = pygame.transform.scale(EXPLOSION_IMAGE, (SIZE_X, SIZE_Y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    for i in range(len(FRUIT_IMAGES)):
        try:
            FRUIT_SURFACES[i], FRUIT_ANGLES[i], FRUIT_TIMES[i] = fruit_movement(SCREEN, 1, FRUIT_IMAGES[i], FRUIT_SURFACES[i], FRUIT_X_MOVEMENTS[i], FRUIT_TIMES[i], FRUIT_ANGLES[i])
            if FRUIT_SURFACES[i].y > HEIGHT: del FRUIT_IMAGES[i], FRUIT_SURFACES[i], FRUIT_X_MOVEMENTS[i], FRUIT_TIMES[i], FRUIT_ANGLES[i], FRUIT_X0S[i], random_fruit_names[i]
        except: pass

    pygame.draw.rect(SCREEN, SB_COLOR, (0, HEIGHT-SCORE_BOARD_HEIGHT, WIDTH, SCORE_BOARD_HEIGHT)) # score board
    score_text = FONT.render(f"Points: {POINTS}", 1, (0,0,0))
    SCREEN.blit(score_text, (10, HEIGHT-SCORE_BOARD_HEIGHT/2))
    pygame.display.update()

pygame.quit()
