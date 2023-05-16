import pygame
pygame.init()

# Screen
WIDTH = 1000
HEIGHT = 800
BACKGROUND_IMAGE = pygame.image.load('images/back.jpg')
BACKGROUND_IMAGE = pygame.transform.rotate(BACKGROUND_IMAGE, 90)
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Fruits
FRUIT_NAMES = ['apple', 'banana', 'basaha', 'peach', 'sandia', 'boom']
FRUIT_ANGLE = 0
FRUIT_TIME = 0
FRUIT_IMAGES = []
FRUIT_SIZES = []
FRUIT_SURFACES = []
FRUIT_X_MOVEMENTS = []
FRUIT_ANGLES = []
FRUIT_TIMES = []
FRUIT_X0S = []
random_fruit_names = []
HIT_IMAGE = pygame.image.load('images/hit.png')
EXPLOSION_IMAGE = pygame.image.load('images/explosion.png')
# SCORE BOARD
SB_COLOR = (0,100,255)
SCORE_BOARD_HEIGHT = int(HEIGHT/15)
POINTS = 0

# Texts
FONT = pygame.font.SysFont('comicsans', 40)


# Audios
BOOM_SOUND = pygame.mixer.Sound("sound/boom.mp3")
HIT_SOUND = pygame.mixer.Sound("sound/splatter.mp3")