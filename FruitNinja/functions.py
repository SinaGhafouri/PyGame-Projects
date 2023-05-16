import pygame
pygame.init()

def fruit_movement(SCREEN, VEL, fruit_image, fruit_surface, fruit_X_MOVEMENT, fruit_time, fruit_angle):
    fruit_surface.x += fruit_X_MOVEMENT
    fruit_time += 1
    fruit_surface.y -= ((2000/VEL)-fruit_time**2/4)/(60*VEL)/2
    # fruit_angle += 2
    fruit_image_rotated = pygame.transform.rotate(fruit_image, fruit_angle)
    fruit_size = fruit_image_rotated.get_size()
    fruit_surface.width = fruit_size[0]
    fruit_surface.height = fruit_size[1]
    # pygame.draw.rect(SCREEN, (0,0,0), (fruit_surface.center[0], fruit_surface.center[1], fruit_surface.width, fruit_surface.height))
    SCREEN.blit(fruit_image_rotated, (fruit_surface.center[0], fruit_surface.center[1]))
    return fruit_surface, fruit_angle, fruit_time