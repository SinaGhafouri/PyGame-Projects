import warnings
warnings.filterwarnings("ignore")
import numpy as np
import os
from glob import glob
os.makedirs('temp', exist_ok=True)
import cv2
from scipy.ndimage import zoom
from PIL import Image
#########################################################
"""Loading the sklearn model"""
import joblib
# loading the SVC model
clf_loaded = joblib.load("theModel/model.pkl")
"""Loading the TF model"""
# import tensorflow as tf
# clf_loaded = tf.keras.models.load_model('theModel/my_TF_CNN_model.h5')
#########################################################
import pygame
pygame.init()
pygame.font.init()

"""CONSTANTS and stuff"""
WIDTH, HEIGHT = 1000, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW.fill((30,30,30))
BACKGROUND_PIXEL_VALUE = 40
BOARD_COLOR = (BACKGROUND_PIXEL_VALUE,BACKGROUND_PIXEL_VALUE,BACKGROUND_PIXEL_VALUE)
RESULT_FONT = pygame.font.SysFont('comicsans', 30)
BUTTON_FONT = pygame.font.SysFont('comicsans', 15)
THICKNESS = 10
DY = int(THICKNESS/2)
DWALL = 15
pygame.draw.rect(WINDOW, BOARD_COLOR, (DWALL,DWALL,WIDTH-2*DWALL,HEIGHT*2/3), 0, 10)
BOARD = pygame.draw.rect(WINDOW, BOARD_COLOR, (DWALL+10,DWALL+10,WIDTH-2*DWALL-20,HEIGHT*2/3-20))
calc = False # to show the result on board
##########################################################
"""Buttons"""
CALCULATE_BUTTON = pygame.draw.rect(WINDOW, (30,100,30), (WIDTH-100,HEIGHT*2/3+2*DWALL,100-DWALL,42), 0, 5)
CLEAR_BUTTON = pygame.draw.rect(WINDOW, (100,30,30), (WIDTH-100,HEIGHT*2/3+2*DWALL+48,100-DWALL,42), 0, 5)
##########################################################
"""Functions"""
def segment_objects(ims):
    _, labels = cv2.connectedComponents(ims)
    im_names = []
    for i in np.unique(labels)[1:]:
        im = labels==i
        x_co = int(np.mean(np.where(im)[1])) ; y_co = int(np.mean(np.where(im)[0]))
        dxy = int(max(np.sum(np.sum(im,axis=0)!=0), np.sum(np.sum(im,axis=1)!=0))/2)
        im_cropped = im[int(y_co)-dxy:int(y_co)+dxy , int(x_co)-dxy:int(x_co)+dxy]
        np.save(f'temp/{10000+x_co}.npy', im_cropped)
        im_names.append(f'{10000+x_co}.npy')
    return im_names

def calc_function():
    calc = True
    sub = WINDOW.subsurface(BOARD)
    pygame.image.save(sub, "temp/screenshot.jpeg")
    ims = np.array(Image.open("temp/screenshot.jpeg").convert('LA'))[:,:,0] - BACKGROUND_PIXEL_VALUE
    try: im_names = segment_objects(ims)
    except: pass
    str_number = ''
    files = sorted(glob('temp/*.npy'))
    for file in files:
        if file.split('\\')[-1] not in im_names: continue
        input_im = np.load(file)
        SHAPE = input_im.shape
        new_im = zoom(input_im, (28/SHAPE[0], 28/SHAPE[1]), order=0)
        predicted_number = clf_loaded.predict([new_im.ravel()])[0]
        str_number += str(predicted_number)
    return str_number, calc

def clear_function():
    calc = False
    WINDOW.fill((30,30,30)) 
    pygame.draw.rect(WINDOW, BOARD_COLOR, (DWALL,DWALL,WIDTH-2*DWALL,HEIGHT*2/3), 0, 10)
    pygame.draw.rect(WINDOW, BOARD_COLOR, (DWALL+10,DWALL+10,WIDTH-2*DWALL-20,HEIGHT*2/3-20)) # BOARD
    fs = glob('temp/*')
    for f in fs: os.remove(f)
    return calc
###########################################################

running = True
clock = pygame.time.Clock()
counter = 0
while running:
    clock.tick(120)
    counter = (counter + 1)%6000
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: # clear
                calc = clear_function()
            if event.key == pygame.K_e: # calculate
                str_number, calc  = calc_function()
        if event.type == pygame.MOUSEBUTTONDOWN and CALCULATE_BUTTON.collidepoint(pygame.mouse.get_pos()):
            str_number, calc  = calc_function()
        if event.type == pygame.MOUSEBUTTONDOWN and CLEAR_BUTTON.collidepoint(pygame.mouse.get_pos()):
            calc  = clear_function()
            
    if calc == True: 
        result_text = RESULT_FONT.render(str_number, 1, (255,255,255))
        WINDOW.blit(result_text, (10, HEIGHT*2/3+50))
    ms_l,ms_m,ms_r = pygame.mouse.get_pressed()
    if ms_l==True:
        mp = pygame.mouse.get_pos()
        last_xy = [mp[0], mp[1]-DY]
        pygame.draw.line(WINDOW, (255,255,255), last_xy, [mp[0], mp[1]+DY], THICKNESS)

    if ms_r==True:
        mp = pygame.mouse.get_pos()
        last_xy = [mp[0], mp[1]-DY]
        pygame.draw.line(WINDOW, (BACKGROUND_PIXEL_VALUE,BACKGROUND_PIXEL_VALUE,BACKGROUND_PIXEL_VALUE), last_xy, [mp[0], mp[1]+DY], int(THICKNESS*1.5))

    
    pygame.draw.rect(WINDOW, (30,100,30), (WIDTH-100,HEIGHT*2/3+2*DWALL,100-DWALL,42), 0, 5) # CALCULATE button
    button_text = BUTTON_FONT.render('Equal', 1, (255,255,255))
    WINDOW.blit(button_text, (WIDTH-100+(100-DWALL)/2-button_text.get_rect().width/2,HEIGHT*2/3+2*DWALL+button_text.get_rect().height/2))
    pygame.draw.rect(WINDOW, (100,30,30), (WIDTH-100,HEIGHT*2/3+2*DWALL+48,100-DWALL,42), 0, 5) # CLEAR button
    button_text = BUTTON_FONT.render('Clear', 1, (255,255,255))
    WINDOW.blit(button_text, (WIDTH-100+(100-DWALL)/2-button_text.get_rect().width/2,HEIGHT*2/3+2*DWALL+button_text.get_rect().height/2+48))

    pygame.display.update()

fs = glob('temp/*')
# for f in fs: os.remove(f)
pygame.quit()
